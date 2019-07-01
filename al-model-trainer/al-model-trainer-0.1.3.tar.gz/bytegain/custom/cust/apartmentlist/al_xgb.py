import pyximport
pyximport.install()
import os
import sys
import numpy
import importlib
import bytegain.custom.nn_tools.xgb_classifier as xgb
import bytegain.custom.nn_tools.model_utils as model_utils
import bytegain.custom.model_data.feature_analysis as feature_analysis
import bytegain.nn_tools.auc_plot as auc_plot
from bytegain.custom.nn_tools.prod_classifier import ProdXgbClassifier
from bytegain.custom.nn_tools.xgb_classifier import XgbClassifier
import bytegain.custom.model_data.read_from_db as read_from_db
from bytegain.custom.model_data.row_handler import RowHandler
from bytegain.custom.model_data.bucket import ValueBucket
from bytegain.custom.model_data.extractor import RowExtractor
from bytegain.custom.cust.apartmentlist.feature_filter import FeatureFilter

"""
import bytegain.cust.apartmentlist.al_xgb as al_xgb
import bytegain.nn_tools.model_utils as model_utils
import bytegain.nn_tools.xgb_classifier as xgb
rh, datasets = al_xgb.create_rh_and_dataset('al_handler_test.json')
results = xgb.cv(datasets, xgb.XgbClassifier, 401, parallel=True)

import bytegain.cust.apartmentlist.al_xgb as al_xgb
import bytegain.nn_tools.xgb_classifier as xgb
rh, datasets = al_xgb.create_rh_and_dataset('al_features_20161214.json')
model = xgb.XgbClassifier()
model.train(datasets)


import bytegain.nn_tools.knock_out as knock_out
import bytegain.cust.apartmentlist.leads_from_redshift as tfl
import bytegain.nn_tools.xgb_classifier as xgb

features = al_handler_from_features.read_al_features('al_handler1.json')
rh = al_handler_from_features.create_row_handler(features)
datasets = tfl.create_datasets_from_row_handler(rh, test_fraction = 0.2)
results = xgb_classifier.cv(datasets, xgb_classifier.XgbClassifier, 601)


"""

def output_feature_scores(model, rh, output):
    features = model.feature_scores(rh)

    for feature in features:
        output.write("%25s: %4.1f\n" % (feature[0], feature[1]));


def train_from_dataset(config, rh, dataset):
    model = xgb.XgbClassifier()
    model.train(dataset, min_child_weight=config['min_child_weight'], max_rounds=config['max_rounds'],
                max_depth=config['max_depth'], l2_norm = config['l2_norm'], train_step_size = config['train_step_size'])
    control_results = model.get_sorted_results(dataset.get_test_control())
    print("Control AUC: %5.3f" % auc_plot.compute_auc(control_results))

    output_feature_scores(model, rh, sys.stdout)
    return model

def create_rh_and_dataset(config):
    rh = create_row_handler(config)
    datasets = create_datasets_from_row_handler(rh, config, test_fraction = 0.2)
    return rh, datasets

def train_and_push(config):
    model_name = config['model_name']
    if not os.path.isdir(model_name):
        print "Creating %s" % model_name
        os.mkdir(model_name)

    rh, datasets = create_rh_and_dataset(config)
    classifier = train_from_dataset(config, rh, datasets)
    results = classifier.get_sorted_results(datasets.test)

    if not os.path.isdir(model_name):
        os.mkdir(model_name)
    os.chdir(model_name)
    model_name = "%s_%s" % (config['model_name'], config['model_version'])
    try:
        auc_plot.plot_predicted_vs_actual2('%s_p_vs_a.png' % model_name, results, points=20)
        auc_plot.plot_auc('%s_roc.png' % model_name, results)

        spec = model_utils.XgbModelSpec(model_name, ".")
        spec.save(classifier, datasets._row_handler, results)
        model_utils.save_results_as_csv(model_name + '.csv', 'id', 'pred', results)
        spec.upload()
    finally:
        os.chdir('..')


def get_selector(config):
    where = "%s between  '%s' and '%s'" % (config['interest_date_column'], config['start_date'], config['end_date'])
    if config['downsample']:
        where += ' and (%s = true or mod(STRTOL(LEFT(MD5(%s),15), 16), 20) < 1)' % (config['outcome_field'], config['id_field'])
    return read_from_db.Selector(config['table'], where,
                                 config['outcome_field'],
                                 config['id_field'],
                                 None,
                                 config.get('positive_outcome_rate_field'))

def create_datasets_from_row_handler(row_handler, config, test_fraction = 0.2, rows = None):
    selector = get_selector(config)
    numpy.random.seed(config['random_seed'])
    read_from_db.generate_row_handler_stats(selector, row_handler)
    return read_from_db.create_datasets(selector, row_handler, test_fraction, rows)

def get_feature_json_file(config):
    model_name = config['model_name']
    if not os.path.isdir(model_name):
        os.mkdir(model_name)
    return "%s/%s" % (model_name, config['feature_json'])

def run_feature_analysis(config):
    data_info = feature_analysis.DataInfo(get_selector(config))
    features = feature_analysis.process_features(data_info)
    feature_analysis.save_features(config['feature_json'], features)
    return features


def create_row_handler(config, load_from = None):
    if isinstance(config['filter'], FeatureFilter):
        filter = config['filter']
    else:
        # For backwards compatibility let the filter be in another file loaded by name.
        module = importlib.import_module('bytegain.custom.cust.apartmentlist.%s' % config['filter'])
        filter = getattr(module, 'filter')

    features = feature_analysis.read_features(config['feature_json'])

    # Set this to experiment with weighting.
    if config['control_field']:
        print("Using '%s' as control.  Weight: %d" % (config['control_field'], config['control_weight']))
        weight_extractor = ControlWeightExtractor(config['control_field'], config['control_weight'])
        control_extractor = RowExtractor(config['control_field'])
    else:
        weight_extractor = None
        control_extractor = None

    row_handler = RowHandler(label_bucket = ValueBucket("leased", RowExtractor(config['outcome_field']), has_null = False),
                             id_extractor = RowExtractor(config['id_field']),
                             weight_extractor = weight_extractor,
                             control_extractor = control_extractor,
                             load_from = load_from,
                             extra_fields = [config['interest_date_column']])
    if load_from is None:
        # print "Excluded features: %s" % str(EXCLUDED_FEATURES)
        buckets = filter.create_buckets(features)
        for bucket in buckets:
            row_handler.add_bucket(bucket)

    return row_handler


class ControlWeightExtractor(object):
    def __init__(self, control_field, control_weight = 1.0):
        self._control_weight = control_weight
        self._control_field = control_field
        self._field = None

    def get_fields(self):
        return [self._control_field]

    def update_fields_by_id(self, cursor_header):
        self._field = cursor_header.index(self._control_field)

    def extract(self, row):
        if self._field is not None:
            return self._control_weight if row[self._field] else 1.0
        else:
            return self._control_weight if row[self._control_field] else 1.0

    def description(self):
        return "Control weighting: %f" % self._control_weight
