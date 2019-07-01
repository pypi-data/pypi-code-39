import time
import numpy
import tempfile
import copy
import xgboost as xgb
import bytegain.nn_tools.auc_plot as auc_plot
from threading import Thread

def _create_dmatrix(dataset, group_function = None):
    x = dataset._data
    y = dataset._labels
    assert len(x) > 0
    weights = dataset._weights
    matrix = xgb.DMatrix(x, label=y, weight=weights)
    if group_function is not None:
        matrix.set_group(group_function(dataset))
    # Request feature names to fix XGB bug
    names = matrix.feature_names
    return matrix

class XgbClassifier(object):
    def __init__(self, outcomes = 2, threads = 16, loaded_bst = None, group_function = None):
        """

        :param outcomes:
        :param threads:
        :param loaded_bst:
        :param group_function: If set then groups are computed and pairwise ranking is used
        """
        self._outcomes = outcomes
        self._group_function = group_function
        if group_function == None:
            # TODO(jjs) - add support for non-binary outcomes
            self._param = {'silent': True, 'objective':'binary:logistic'}
            self._param['eval_metric'] = 'auc'
        else:
            self._param = {'silent': True, 'objective':'rank:pairwise'}
            self._param['eval_metric'] = 'ndcg'

        if threads is not None:
            self._param['nthread'] = threads
        self._bst = loaded_bst

    def train(self, datasets, max_rounds = 401, min_increase_rounds = 40, l2_norm = 1000, gamma = 1, train_step_size = 0.40, 
        subsample = 0.8, max_depth = 2, min_child_weight = 1, max_delta_step = 0 ):
        dtrain = _create_dmatrix(datasets.train, self._group_function)
        dtest = _create_dmatrix(datasets.test, self._group_function)
        base_rate = numpy.sum(datasets.train.labels) / len(datasets.train.labels)
        print ('train base rate: %5.3f%%' % (base_rate * 100))
        evallist  = [(dtest,'eval'), (dtrain,'train')]
        self._param["base_score"] = base_rate
        self._param["early_stopping_rounds"] = min_increase_rounds
        self._param["gamma"] = gamma
        self._param["subsample"] = subsample
        self._param['lambda'] = l2_norm
        self._param['eta'] = train_step_size
        self._param['tree_method'] = 'exact'
        self._param['max_depth'] = max_depth
        self._param['min_child_weight'] = min_child_weight
        self._param['max_delta_step'] = max_delta_step
        self._bst = xgb.train(self._param, dtrain, max_rounds, evallist, xgb_model=self._bst, verbose_eval = 100)

    def get_sorted_results(self, dataset):
        dtest = _create_dmatrix(dataset, self._group_function)
        preds = self._bst.predict(dtest)
        results = []
        if self._group_function is None:
            for entry in zip(preds, dataset._labels, dataset._ids):
                results.append({"probability" : entry[0], "label" : entry[1], "id" : entry[2]})
            auc_plot.sort_results(results)
        else:
            index = 0
            for group_size in self._group_function(dataset):
                end = index + group_size
                group =[]
                for i in range(index, end):
                    group.append({"probability" : preds[i], "label" : dataset._labels[i], "id" : dataset._ids[i]})
                index = end
                auc_plot.sort_results(group)
                results.append(group)

        return results

    def dump_model(self, row_handler, filename):
        fmap = filename + ".fmap"
        create_feature_map(row_handler, fmap)
        self._bst.dump_model(filename, fmap, True)

    def feature_scores(self, row_handler):
        with tempfile.NamedTemporaryFile(delete = False, suffix=".fmap") as fmap:
            create_feature_map(row_handler, fmap.name)
            feature_dict = self._bst.get_score(fmap.name, 'gain')
            sum = 0
            for k,v in feature_dict.iteritems():
                sum += v
            features = [(k, v * 100.0/sum) for k,v in feature_dict.iteritems()]
            features = sorted(features, key = lambda x: x[1], reverse = True)
            return features

    # def feature_scores2(self, row_handler):
    #     return xgb_stats.compute_feature_importance(self, row_handler)

    def save(self, filename):
        self._bst.save_model(filename)

def create_feature_map(row_handler, filename):
    with open(filename, "w") as f:
        for i, bucket in enumerate(row_handler._buckets):
            f.write("%d %s q\n " % (i, bucket._name))

def get_params(params):
    k, v = params.iteritems().next()
    new_params = copy.copy(params)
    del new_params[k]
    if type(v) not in (tuple, list):
        v = [v]
    total_runs = []
    if len(new_params) > 0: 
        runs = get_params(new_params)
        for value in v:            
            new_runs = copy.deepcopy(runs)  
            for new_run in new_runs:
                new_run[k] = value
            total_runs.extend(new_runs)
    else:
        for value in v:
            total_runs.append({k : value})
    return total_runs

def run_hyper_param(dataset, params):
    runs = get_params(params)
    print ("Total runs: %d" % len(runs))
    outcomes = []
    for run in runs:
        net = XgbClassifier()
        net.train(dataset, **run)
        results = net.get_sorted_results(dataset.test)
        auc = auc_plot.compute_auc(results)
        outcomes.append((auc, run))
        print "AUC: %6.4f %s" % (auc, str(run))

    outcomes = sorted(outcomes, key = lambda x: x[0], reverse = True)

    for run in outcomes:
        print "AUC: %6.4f %s" % (run[0], str(run[1]))

class CvRunner(Thread):
    def __init__(self, fold, dataset, net, training_cycles, train_args):
        super(CvRunner, self).__init__()
        self._net = net
        self._fold = fold
        self._dataset = dataset
        self._training_cycles = training_cycles
        self._train_args = train_args

    def run(self):
        print ("Running CV fold: %d" % self._fold)

        self._net.train(datasets=self._dataset, max_rounds = self._training_cycles, **self._train_args)
        self._sorted_test = self._net.get_sorted_results(self._dataset.test)

class ClonedDatasets(object):
    def __init__(self, datasets):
        self.train = datasets.train.copy()
        self.test = datasets.test.copy()

def cv(dataset, create_net, training_cycles = 361, runs = 5, parallel = False, **train_args):
    start_time = time.time()
    auc_sum = 0
    aucs = []
    test_results = []
    runners = []
    for run in range(runs):
        clone_dataset = ClonedDatasets(dataset) if parallel else dataset
        net = create_net(threads = 3) if parallel else create_net()
        runner = CvRunner(run, clone_dataset, net, training_cycles, train_args)
        runners.append(runner)
        if parallel:
            runner.start()
        else:
            runner.run()

        if run < runs - 1:
            dataset.repartition()

    if parallel:
        for thread in runners:
            thread.join()

    for runner in runners:
        sorted_test = runner._sorted_test
        aucs.append(auc_plot.compute_auc(sorted_test))
        test_results.extend(sorted_test)

    auc_plot.sort_results(test_results)
    auc = auc_plot.compute_auc(test_results)
    print ("CV time: %5.3fs" % (time.time() - start_time))
    print "Total Auc: %5.3f %s" % (auc, str([("%5.3f" % a) for a in aucs]))
    return test_results
