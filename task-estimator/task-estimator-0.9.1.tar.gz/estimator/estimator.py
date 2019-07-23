#!/usr/bin/env python
import sys
import os
import argparse
import csv
import re
import pickle
import random
import time
from pprint import pprint

import yaml

from jira import JIRA

import pandas as pd
# import numpy as np
# from scipy.spatial import distance
from nltk.stem.snowball import SnowballStemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import cross_val_predict
from sklearn.metrics import mean_squared_error, mean_absolute_error
# from sklearn.pipeline import Pipeline
# from sklearn.preprocessing import StandardScaler, MinMaxScaler, MaxAbsScaler
from sklearn.feature_extraction.text import TfidfTransformer

from sklearn.linear_model import LogisticRegression # note, not included in all_estimators?
# from sklearn.linear_model.bayes import ARDRegression
from sklearn.ensemble.weight_boosting import AdaBoostRegressor
from sklearn.ensemble.bagging import BaggingRegressor
# from sklearn.linear_model.bayes import BayesianRidge
# from sklearn.cross_decomposition.cca_ import CCA
from sklearn.tree.tree import DecisionTreeRegressor
# from sklearn.linear_model.coordinate_descent import ElasticNet
# from sklearn.linear_model.coordinate_descent import ElasticNetCV
from sklearn.tree.tree import ExtraTreeRegressor
from sklearn.ensemble.forest import ExtraTreesRegressor
# from sklearn.gaussian_process.gpr import GaussianProcessRegressor
from sklearn.ensemble.gradient_boosting import GradientBoostingRegressor
from sklearn.linear_model.huber import HuberRegressor
# from sklearn.neighbors.regression import KNeighborsRegressor
from sklearn.kernel_ridge import KernelRidge
# from sklearn.linear_model.least_angle import Lars
# from sklearn.linear_model.least_angle import LarsCV
# from sklearn.linear_model.coordinate_descent import Lasso
# from sklearn.linear_model.coordinate_descent import LassoCV
# from sklearn.linear_model.least_angle import LassoLars
# from sklearn.linear_model.least_angle import LassoLarsCV
# from sklearn.linear_model.least_angle import LassoLarsIC
from sklearn.linear_model.base import LinearRegression
from sklearn.svm.classes import LinearSVR
from sklearn.neural_network.multilayer_perceptron import MLPRegressor
# from sklearn.linear_model.coordinate_descent import MultiTaskElasticNet
# from sklearn.linear_model.coordinate_descent import MultiTaskElasticNetCV
# from sklearn.linear_model.coordinate_descent import MultiTaskLasso
# from sklearn.linear_model.coordinate_descent import MultiTaskLassoCV
from sklearn.svm.classes import NuSVR
# from sklearn.linear_model.omp import OrthogonalMatchingPursuit
# from sklearn.linear_model.omp import OrthogonalMatchingPursuitCV
# from sklearn.cross_decomposition.pls_ import PLSCanonical
# from sklearn.cross_decomposition.pls_ import PLSRegression
from sklearn.linear_model.passive_aggressive import PassiveAggressiveRegressor
from sklearn.linear_model.ransac import RANSACRegressor
# from sklearn.neighbors.regression import RadiusNeighborsRegressor
from sklearn.ensemble.forest import RandomForestRegressor
from sklearn.linear_model.ridge import Ridge
from sklearn.linear_model.ridge import RidgeCV
from sklearn.linear_model.stochastic_gradient import SGDRegressor
from sklearn.svm.classes import SVR
# from sklearn.linear_model.theil_sen import TheilSenRegressor
from sklearn.compose._target import TransformedTargetRegressor


SOURCE_JIRA = 'jira'
SOURCE_FIXTURE = 'fixture'
SOURCES = (
    SOURCE_JIRA,
    SOURCE_FIXTURE,
)

JIRA_DONE_STATUSES = 'Closed, Deployed, "Ready For Deployment", Resolved'
JIRA_OPEN_STATUSES = 'Open, "Ready For Development"'

ACTION_RETRIEVE = 'retrieve'
ACTION_TRAIN = 'train'
ACTION_TEST = 'test'
ACTION_APPLY = 'apply'
ACTION_GENERATE_COMBINATIONS = 'generate-combinations'
ACTION_TEST_COMBINATIONS = 'test-combinations'
ACTION_LIST_REGRESSORS = 'list-regressors'
ACTIONS = (
    ACTION_RETRIEVE,
    ACTION_TRAIN,
    ACTION_TEST,
    ACTION_APPLY,
    ACTION_GENERATE_COMBINATIONS,
    ACTION_TEST_COMBINATIONS,
    ACTION_LIST_REGRESSORS,
)

stemmer = SnowballStemmer('english')


# Custom class that adapts sklearn's CountVectorizer to include a stemmer
# http://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.CountVectorizer.html
class StemmedCountVectorizer(CountVectorizer):
    def build_analyzer(self):
        analyzer = super(StemmedCountVectorizer, self).build_analyzer()
        return lambda doc: ([stemmer.stem(w) for w in analyzer(doc)])


def iter_search_issues(j, jql):
    block_size = 100
    block_num = 0
    while True:
        start_idx = block_num * block_size
        issues = j.search_issues(jql, start_idx, block_size)
        if not issues:
            # Retrieve issues until there are no more to come
            break
        block_num += 1
        for issue in issues:
            yield issue


ISSUE_FIELD = 'issue'
TITLE_FIELD = 'title'
TEXT_FIELD = 'text'
HOURS_FIELD = 'hours'
ESTIMATED_HOURS_FIELD = 'estimated_hours'

DATA_TRAINING = 'training'
DATA_TESTING = 'testing'
DATA_HUMAN = 'human'

class Estimator:

    def __init__(self, name, source, verbose=False, **kwargs):
        self.verbose = verbose
        self.name = name
        self.source = source
        self.data_dir = kwargs.pop('data_dir', 'data')
        self.fixture = kwargs.pop('fixture', '')
        self.regressor_params = kwargs.pop('regressor', {})
        self.extra_sql = kwargs.pop('extra_sql', '').strip()
        self.minimum_estimate_minutes = int(kwargs.pop('minimum_estimate_minutes', '30'))
        # These fields will be updated with the hourly estimate.
        self.hour_update_fields = kwargs.pop('hour_update_fields', [])
        self._training_fn = None
        self._label_to_field = None
        if source == SOURCE_JIRA:
            self.server = kwargs.pop('server')
            self.username = kwargs.pop('username')
            self.password = kwargs.pop('password')
            self.projects = kwargs.pop('projects')
            options = {'server': self.server}
            self.jira = JIRA(options=options, basic_auth=(self.username, self.password))
        elif source == SOURCE_FIXTURE:
            self.projects = kwargs.pop('projects')
        else:
            raise NotImplementedError('Unknown source: %s' % source)

    @classmethod
    def from_configuration_file(cls, fn, verbose=False):
        with open(fn, 'r') as fin:
            config = yaml.load(fin)
        return cls(os.path.splitext(os.path.split(fn)[-1])[0], verbose=verbose, **config)

    @property
    def training_fn(self):
        """
        Filename to use for storing tagged sample records, suitable for training.
        """
        return self._training_fn or ('%s/%s-training.csv' % (self.data_dir, self.name))

    @property
    def untagged_fn(self):
        """
        Filename to use for storing untagged sample records, sutiable for application of a trained regressor.
        """
        return self._training_fn or ('%s/%s-untagged.csv' % (self.data_dir, self.name))

    @property
    def classifier_fn(self):
        return '%s/%s-classifier.pkl' % (self.data_dir, self.name)

    @property
    def vectorizer_fn(self):
        return '%s/%s-vectorizer.pkl' % (self.data_dir, self.name)

    @property
    def tfidf_fn(self):
        return '%s/%s-tfidf.pkl' % (self.data_dir, self.name)

    @property
    def label_to_field(self):
        """
        Returns a dictionary mapping the user friendly name into the system's internal name used for doing database updates.
        """
        if not self._label_to_field:
            if self.source == SOURCE_JIRA:
                self._label_to_field = {field['name']: field['id'] for field in self.jira.fields()}
            else:
                raise NotImplementedError
        return self._label_to_field

    def retrieve(self, training=True, key=None, human=False):

        # Set filename for saving data.
        if training:
            fn = self.training_fn
        else:
            fn = self.untagged_fn

        if self.source == SOURCE_JIRA:
            if key:
                jql = 'key = {key}'.format(key=key)
            else:
                jql = 'project IN ({projects})'
                if training:
                    # If we're looking for training data, then ensure all issues have logged time.
                    jql += ' AND timeSpent IS NOT EMPTY AND status IN ({done_statuses})'
                    if human:
                        # Only look at values where someone has left logged hours.
                        jql += ' AND originalEstimate IS NOT EMPTY'
                        # jql += ' AND (originalEstimate IS EMPTY OR "Story Points" IS EMPTY)'
                else:
                    # If we're NOT looking for training data, then ensure all issues have no original time estimate.
                    jql += ' AND originalEstimate IS EMPTY AND status IN ({open_statuses})'
                jql = jql.format(projects=self.projects, done_statuses=JIRA_DONE_STATUSES, open_statuses=JIRA_OPEN_STATUSES)
                if self.extra_sql:
                    jql += ' AND %s' % self.extra_sql

            allfields = self.jira.fields()
            label_to_field = {field['name']: field['id'] for field in allfields}
            if self.verbose:
                print('Jira fields:')
                pprint(label_to_field, indent=4)

            if self.verbose:
                print('Jira query:', jql)

            fieldnames = [ISSUE_FIELD, TITLE_FIELD, TEXT_FIELD, HOURS_FIELD, ESTIMATED_HOURS_FIELD]
            writer = csv.DictWriter(open(fn, 'w'), fieldnames=fieldnames)
            writer.writerow(dict(zip(fieldnames, fieldnames)))
            for i, issue in enumerate(iter_search_issues(self.jira, jql)):
                print('Retrieving data for issue %s...' % issue)

                if training:
                    hours = issue.fields.timespent * 1/60. * 1/60.
                else:
                    hours = None

                estimated_hours = None
                if issue.fields.timeoriginalestimate:
                    estimated_hours = issue.fields.timeoriginalestimate * 1/60. * 1/60.

                text = re.sub(r'[\n\t\r, ]+', ' ', issue.fields.description or '').strip()
                title = (issue.fields.summary or '').strip()
                data = {
                    ISSUE_FIELD: str(issue),
                    TITLE_FIELD: title,
                    TEXT_FIELD: text,
                    HOURS_FIELD: hours,
                    ESTIMATED_HOURS_FIELD: estimated_hours
                }
                writer.writerow(data)
        elif self.source == SOURCE_FIXTURE:
            self._training_fn = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'fixtures/%s.csv' % self.fixture)
            assert os.path.isfile(self._training_fn), 'File %s does not exist.' % self._training_fn
        else:
            raise NotImplementedError

    def get_training_dataframe(self):
        reader = list(csv.DictReader(open(self.training_fn)))
        for row in reader:
            try:
                row[HOURS_FIELD] = float(row[HOURS_FIELD])
            except ValueError:
                print('Warning: Ignoring bad hours value: %s' % row[HOURS_FIELD], file=sys.stderr)
            try:
                row[ESTIMATED_HOURS_FIELD] = float(row[ESTIMATED_HOURS_FIELD])
            except ValueError:
                print('Warning: Ignoring bad estimated_hours value: %s' % row[ESTIMATED_HOURS_FIELD], file=sys.stderr)
        df = pd.DataFrame(reader)
        return df

    def get_untagged_dataframe(self):
        reader = list(csv.DictReader(open(self.untagged_fn)))
        df = pd.DataFrame(reader)
        return df

    def list_regressors(self):
        """
        Lists all regressors available.
        """
        from sklearn.utils.testing import all_estimators
        lst = all_estimators(type_filter='regressor')
        regressors = []
        for name, cls in sorted(lst, key=lambda o: o[0]):
            regressors.append(name)
            path = re.findall(r'\'([^\']+)\'', str(cls))[0].split('.')
            from_part = '.'.join(path[:-1])
            module_part = path[-1]
            print('from %s import %s' % (from_part, module_part))
        print()
        for r in sorted(regressors):
            print('%s,' % r)

    def generate_combinations(self):
        """
        Generates all parameter combinations for training regressors.
        """
        from itertools import product
        cls = [
            LogisticRegression, # not included by all_estimators by default?

            # ARDRegression, # does not support sparse data
            AdaBoostRegressor,
            BaggingRegressor,
            # BayesianRidge, # does not support sparse data
            # CCA, # does not support sparse data
            DecisionTreeRegressor,
            # ElasticNet, # works, but takes forever to train and accuracy is poor
            # ElasticNetCV, # works, but takes forever to train and accuracy is poor
            ExtraTreeRegressor,
            ExtraTreesRegressor,
            # GaussianProcessRegressor, # does not support sparse data
            GradientBoostingRegressor,
            HuberRegressor,
            # KNeighborsRegressor, # does not support sparse data
            KernelRidge,
            # Lars, # does not support sparse data
            # LarsCV, # does not support sparse data
            # Lasso, # redundant with LassoCV
            # LassoCV, # takes ~10 hours to train but has mediocre accuracy
            # LassoLars, # does not support sparse data
            # LassoLarsCV, # does not support sparse data
            # LassoLarsIC, # does not support sparse data
            LinearRegression,
            LinearSVR,
            MLPRegressor,
            # MultiTaskElasticNet, # does not support sparse data
            # MultiTaskElasticNetCV, # does not support sparse data
            # MultiTaskLasso, # does not support sparse data
            # MultiTaskLassoCV, # does not support sparse data
            NuSVR,
            # OrthogonalMatchingPursuit, # does not support sparse data
            # OrthogonalMatchingPursuitCV, # does not support sparse data
            # PLSCanonical, # does not support sparse data
            # PLSRegression, # does not support sparse data
            PassiveAggressiveRegressor,
            RANSACRegressor,
            # RadiusNeighborsRegressor, # does not support sparse data
            RandomForestRegressor,
            Ridge,
            RidgeCV,
            SGDRegressor,
            SVR,
            # TheilSenRegressor, # does not support sparse data
            TransformedTargetRegressor,
        ]
        stop_words = ['english', None]
        min_df = [
            0,
            0.25,
            0.5,
            # 0.75,
            # 1.0
        ]
        analyzer = ['word', 'char', 'char_wb']
        ngram_range = [
            # (1, 1),
            (1, 2),
            (1, 3),
            (1, 4),
            (1, 5),
            (1, 6),
            (2, 2),
            # (2, 3),
            # (2, 4),
            # (2, 5),
            # (2, 6),
            # (3, 3),
            # (3, 4),
            # (3, 5),
            # (3, 6),
        ]
        fieldnames = ['cls', 'stop_words', 'min_df', 'analyzer', 'ngram_min', 'ngram_max']
        writer = csv.DictWriter(open(self.combinations_fn, 'w'), fieldnames=fieldnames)
        writer.writerow(dict(zip(fieldnames, fieldnames)))
        all_combos = list(product(cls, stop_words, min_df, analyzer, ngram_range))
        random.shuffle(all_combos)
        for _cls, _stop_words, _min_df, _analyzer, _ngram_range in all_combos:
            writer.writerow({
                'cls': _cls.__name__,
                'stop_words': _stop_words,
                'min_df': _min_df,
                'analyzer': _analyzer,
                'ngram_min': _ngram_range[0],
                'ngram_max': _ngram_range[1]
            })

    @property
    def combinations_fn(self):
        return '%s/%s-combinations.csv' % (self.data_dir, self.name)

    @property
    def priors_fn(self):
        return '%s/%s-combinations-priors.txt' % (self.data_dir, self.name)

    @property
    def scores_fn(self):
        return '%s/%s-combinations-scores.csv' % (self.data_dir, self.name)

    def test_combinations(self):
        """
        Iterates through all combinations, trains a regressor and records its error rate.
        """
        reader = csv.DictReader(open(self.combinations_fn, 'r'))
        try:
            priors = set(l.strip() for l in open(self.priors_fn, 'r').readlines())
        except FileNotFoundError:
            priors = set()
        print('%i priors found.' % len(priors))
        write_headers = not os.path.isfile(self.scores_fn)
        with open(self.scores_fn, 'a') as fout, open(self.priors_fn, 'a') as prior_out:
            fieldnames = ['cls', 'stop_words', 'min_df', 'analyzer', 'ngram_min', 'ngram_max', 'mse', 'time']
            writer = csv.DictWriter(fout, fieldnames=fieldnames)

            # Write header.
            if write_headers:
                writer.writerow(dict(zip(fieldnames, fieldnames)))

            # Check every combination.
            combos = list(reader)
            total = len(combos)
            i = 0
            for combo in combos:
                i += 1
                sys.stdout.write('Checking combo %i of %i: %.02f%% %s...\n' % (i, total, i/float(total)*100, combo))
                sys.stdout.flush()

                # Skip combinations that we've already tested.
                combo_hash = str(tuple(sorted(combo.items())))
                if combo_hash in priors:
                    continue

                # Convert combo values.
                cls = eval(combo['cls']) # pylint: disable=eval-used
                stop_words = combo['stop_words']
                if not stop_words or stop_words == 'None':
                    stop_words = None
                ngram_range = (int(combo['ngram_min']), int(combo['ngram_max']))
                min_df = float(combo['min_df'])
                analyzer = combo['analyzer']

                # Find combo MSE.
                td = None
                try:
                    t0 = time.time()
                    clf, count_vect, tfidf_transformer = self.train(
                        cls=cls,
                        stop_words=stop_words,
                        ngram_range=ngram_range,
                        analyzer=analyzer,
                        min_df=min_df,
                        save=False
                    )
                    td = time.time() - t0
                    error = self.test(clf=clf, count_vect=count_vect, tfidf_transformer=tfidf_transformer)
                except Exception as exc:
                    error = str(exc)
                    print('error:', error)

                # Save results.
                writer.writerow({
                    'cls': cls.__name__,
                    'stop_words': stop_words,
                    'min_df': min_df,
                    'analyzer': analyzer,
                    'ngram_min': ngram_range[0],
                    'ngram_max': ngram_range[1],
                    'mse': error,
                    'time': td,
                })
                fout.flush()
                print('TD:', td)
                print(combo_hash, file=prior_out)
                prior_out.flush()

    def train(self, cls=None, stop_words=-1, ngram_range=None, analyzer=None, min_df=None, save=True):
        """
        Trains a regressor using the given parameters.
        """

        if cls is None:
            cls = self.regressor_params.get('cls', LinearRegression)
            if isinstance(cls, str):
                cls = globals()[cls]
        if stop_words == -1:
            stop_words = self.regressor_params.get('stop_words', 'english')
            if not stop_words:
                stop_words = None
        if ngram_range is None:
            ngram_range = tuple(self.regressor_params.get('ngram_range', (1, 3)))
        if analyzer is None:
            analyzer = self.regressor_params.get('analyzer', 'word')
        if min_df is None:
            min_df = float(self.regressor_params.get('min_df', 0.0))

        print('Training using:', cls, stop_words, ngram_range, analyzer, min_df)

        print('Loading training dataframe...')
        t0 = time.time()
        df = self.get_training_dataframe()
        td = time.time() - t0
        print('Training dataframe loaded in %s seconds.' % td)

        # https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.CountVectorizer.html#sklearn.feature_extraction.text.CountVectorizer
        print('Training vectorizer...')
        t0 = time.time()
        count_vect = StemmedCountVectorizer(stop_words=stop_words, ngram_range=ngram_range, analyzer=analyzer, min_df=min_df)
        # X_train_counts = count_vect.fit_transform(df[TEXT_FIELD])
        X_train_counts = count_vect.fit_transform(df[TITLE_FIELD] + ' ' + df[TEXT_FIELD])
        td = time.time() - t0
        print('Trained vectorizer in %s seconds.' % td)

        print('Training tfidf...')
        t0 = time.time()
        tfidf_transformer = TfidfTransformer()
        X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
        td = time.time() - t0
        print('Trained tfidf in %s seconds.' % td)

        print('Training classifier...')
        t0 = time.time()
        clf = cls()
        clf.fit(X_train_tfidf, df[HOURS_FIELD])
        td = time.time() - t0
        print('Trained classifier in %s seconds.' % td)

        def make_dirs(fn):
            try:
                d, f = os.path.split(fn)
                if d:
                    os.makedirs(d)
            except Exception as exc:
                print('Unable to make directory %s: %s' % (d, exc))

        if save:

            print('Saving classifier...')
            make_dirs(self.classifier_fn)
            with open(self.classifier_fn, 'wb') as fout:
                pickle.dump(clf, fout)

            # Dump the trained vectorizer with Pickle
            print('Saving vectorizer...')
            make_dirs(self.vectorizer_fn)
            with open(self.vectorizer_fn, 'wb') as fout:
                pickle.dump(count_vect, fout)

            # Dump the trained tfidf with Pickle
            print('Saving tfidf...')
            make_dirs(self.tfidf_fn)
            with open(self.tfidf_fn, 'wb') as fout:
                pickle.dump(tfidf_transformer, fout)

        return clf, count_vect, tfidf_transformer

    def test(self, clf=None, count_vect=None, tfidf_transformer=None, human=False, retrain=False):
        """
        Calculates the mean squared error of the last trained regressor.
        """
        if human:
            print('Calculating the error rate in human provided estimates...')
            self.retrieve(training=True, human=True)
            df = self.get_training_dataframe()
            y_true = []
            y_pred = []
            for index, row in df.iterrows():
                if bool(row['hours']) and bool(row['estimated_hours']):
                    y_true.append(float(row['hours']))
                    y_pred.append(float(row['estimated_hours']))
            print("Test Samples: {}".format(len(y_pred)))
            mse = mean_squared_error(y_true, y_pred)
            print("MSE: {}".format(mse))
            mae = mean_absolute_error(y_true, y_pred)
            print("MAE: {}".format(mae))
            return mse, mae
        else:
            print('Calculating the error rate in our machine learning tagged estimates...')
            if retrain:
                self.retrieve(training=True, human=False)
                self.train()

            print('Loading data...')
            df = self.get_training_dataframe()

            if clf is None:
                print('Loading regressor...')
                clf = pickle.load(open(self.classifier_fn, 'rb'))
            if count_vect is None:
                print('Loading vectorizer...')
                count_vect = pickle.load(open(self.vectorizer_fn, 'rb'))
            if tfidf_transformer is None:
                print('Loading transformer...')
                tfidf_transformer = pickle.load(open(self.tfidf_fn, 'rb'))

            print('Vectorizing data...')
            t0 = time.time()
            # X_train_counts = count_vect.fit_transform(df[TEXT_FIELD])
            X_train_counts = count_vect.fit_transform(df[TITLE_FIELD] + ' ' + df[TEXT_FIELD])
            td = time.time() - t0
            print('Vectorized in %s seconds.' % td)

            print('Transforming data...')
            t0 = time.time()
            X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
            td = time.time() - t0
            print('Transformed in %s seconds.' % td)

            print('Running cross validation...')
            t0 = time.time()
            predictions = cross_val_predict(clf, X_train_tfidf, df[HOURS_FIELD])
            td = time.time() - t0
            print('Ran cross validation in %s seconds.' % td)
            print("Test Samples: {}".format(len(predictions)))
            mse = mean_squared_error(df[HOURS_FIELD], predictions)
            print("MSE: {}".format(mse))
            mae = mean_absolute_error(df[HOURS_FIELD], predictions)
            print("MAE: {}".format(mae))
            return mse, mae

    def apply(self, retrain=False, key=None, save=False):
        """
        Uses the last trained regressor and tags all untagged samples.

        retrain := If true, runs retrieve() and train() beforehand.
        key := specific ticket key to be tagged
        save := If true, updates the time estimate at the source
        """

        self.retrieve(training=False, key=key, human=False)

        df = self.get_untagged_dataframe()

        if retrain:
            self.retrieve()
            print('Re-training regressor...')
            clf, count_vect, tfidf_transformer = self.train()
        else:
            clf = pickle.load(open(self.classifier_fn, 'rb'))
            count_vect = pickle.load(open(self.vectorizer_fn, 'rb'))
            tfidf_transformer = pickle.load(open(self.tfidf_fn, 'rb'))

        ret = []
        if df.empty:
            print('\nNo untagged records found.')
        else:
            for index, row in df.iterrows():
                # new_counts = count_vect.transform([row['text']])
                new_counts = count_vect.transform([row['title'] + ' ' + row['text']])
                X_new_tfidf = tfidf_transformer.transform(new_counts)
                prediction = clf.predict(X_new_tfidf)
                hours = prediction[0]
                if hours >= 1:
                    unit = 'h'
                    time_value = hours = int(round(hours, 0))
                elif hours <= 0:
                    # Assume a minimum of 15 minutes.
                    unit = 'm'
                    time_value = hours = 15
                else:
                    # Convert all hour fractions to minutes.
                    unit = 'm'
                    time_value = int(max(round(hours * 60, 0), self.minimum_estimate_minutes))

                print('Key:', row['issue'], '%s%s' % (time_value, unit))
                ret.append((row['issue'], time_value, unit))
                if save:
                    if self.source == SOURCE_JIRA:
                        print('Updating Jira ticket...')
                        issue = self.jira.issue(row['issue'])
                        issue.update(fields={"timetracking":{"originalEstimate": "%s%s" % (time_value, unit)}})
                        for field_name in self.hour_update_fields:
                            field_id = self.label_to_field[field_name]
                            issue.update(fields={field_id: hours})
                        print('Jira ticket updated!')
                    else:
                        raise NotImplementedError('Unknown source: %s' % self.source)

        return ret


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('config', default=None, help='Filename of the configuration file to use.')
    parser.add_argument('--verbose', default=False, action='store_true', help='Filename of the configuration file to use.')

    subparsers = parser.add_subparsers(
        dest="command",
    )

    retrieve_parser = subparsers.add_parser(ACTION_RETRIEVE, help='Retrieves data.')

    train_parser = subparsers.add_parser(ACTION_TRAIN, help='Trains classifier on data.')

    test_parser = subparsers.add_parser(ACTION_TEST, help='Calculates the classifier\'s accuracy.')
    test_parser.add_argument('--retrain', default=False, action='store_true', help='If given, forces a retraining before tagging.')
    test_parser.add_argument('--human', default=False, action='store_true', help='If given, tests accuracy of human tagging.')

    apply_parser = subparsers.add_parser(ACTION_APPLY, help='Uses the trained classifier to tag untagged data.')
    apply_parser.add_argument('--retrain', default=False, action='store_true', help='If given, forces a retraining before tagging.')
    apply_parser.add_argument('--key', default='', help='Specific ticket key to tag.')
    apply_parser.add_argument('--save', default=False, action='store_true', help='If given, saves the estimate in the source.')

    gc_parser = subparsers.add_parser(ACTION_GENERATE_COMBINATIONS, help='Generates base file of all classifier combinations to test.')

    tc_parser = subparsers.add_parser(ACTION_TEST_COMBINATIONS, help='Tests all classifier combinations.')

    lr_parser = subparsers.add_parser(ACTION_LIST_REGRESSORS, help='Lists all available regression algorithms.')

    args = vars(parser.parse_args())
    # print('args:', args)

    config_fn = args.pop('config')
    verbose = args.pop('verbose')
    if not config_fn:
        raise Exception('No config specified.')
    estimator = Estimator.from_configuration_file(config_fn, verbose=verbose)

    cmd = args.pop('command')
    if not cmd:
        raise Exception('No command specified.')
    if cmd not in ACTIONS:
        raise Exception('Invalid command: %s' % cmd)
    getattr(estimator, cmd.replace('-', '_'))(**args)


if __name__ == '__main__':
    main()
