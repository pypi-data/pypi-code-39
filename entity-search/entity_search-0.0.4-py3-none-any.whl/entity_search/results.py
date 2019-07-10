import numpy as np
import pandas as pd
import re
import os
from operator import itemgetter
from itertools import groupby
from .evaluation import *

class Attributes(object):
    def __init__(self, name):
        parameters = name.split("-")
        self.name = parameters[0]
        self.parameters = [parameters[i] for i in range(1,len(parameters))]

    def __str__(self):
        params = "-".join(self.parameters)
        return "{}-{}".format(self.name, params) if len(self.parameters) > 0 else self.name

class Result(object):
    ats = [10, 100]
    query_classification = [
            ('SemSearch_ES', ['SemSearch_ES']),
            ('INEX_LD', ['INEX_LD']),
            ('ListSearch', ['SemSearch_LS','INEX_XER', 'TREC_Entity']),
            ('QALD-2', ['QALD2_te', 'QALD2_tr'])
        ]

    def __init__(self, _file, name):
        self._file = _file
        attributes = name.split(".run")[0].split("_")
        self.experiment = Attributes(attributes[0])
        self.adjacency = Attributes(attributes[1])
        self.algorithm = Attributes(attributes[2])
        if self.algorithm.name != 'text':
            self.implementation = Attributes(attributes[3])
            if self.implementation.name == 'pi':
                self.kernel = Attributes(attributes[4])
                self.lazy = Attributes(attributes[5])

    def compute_ndcg(self, ground_file):
        """Compute ndcg for the result against the provided ground_truth file
        using the @n defined in ats.
        Args:
            ground_file: the ground-truth file
        """
        ndcg = evaluate_ndcg(ground_file, self._file, self.ats)
        # expand query categories in ndcg and add it to the output
        query_category = ndcg.index.get_level_values(0).to_series().str.\
            split('-', expand = True)[0]
        query_category = query_category.rename('category')
        self.ndcg = ndcg.join(query_category)

    def get_mean(self, at, filters):
        """ Compute the mean of the data frame df at the property 'at'. If the
        property 'at' has a category, it creates a new df with necessary information
        Args:
            df: dataframe
            at: property
            category: if the property has a category
        Response:
            the mean of property at.
        """
        if filters != None:
            df_g = self.ndcg.groupby(['category'])
            # Get dataset names for the query type
            m_datasets = None
            for query, datasets in self.query_classification:
                if query == filters:
                    m_datasets = datasets
                    break
            if m_datasets == None:
                raise RuntimeError('query type "{}" not found'.format(filters))
            selection = []
            for dataset in m_datasets:
                try:
                    selection.append(df_g.get_group(dataset))
                except KeyError as e:
                    # if category is not present, it will generate a key error
                    continue
            try:
                ss = pd.concat(selection)
                mean = ss.mean().values[at]
            except ValueError as e:
                # selection is empty. Mean should be zero
                mean = 0.0
        else:
            mean = self.ndcg.mean().values[at]
        return mean

    def __str__(self):
        mystr = "{}_{}_{}".format(self.experiment, self.adjacency, self.algorithm)
        if self.algorithm.name != 'text':
            mystr = "{}_{}".format(mystr, self.implementation)
            if self.implementation.name == 'pi':
                mystr = "{}_{}_{}".format(mystr, self.kernel, self.lazy)
        return mystr

class TrecResults(object):
    def __init__(self, base_path, prefix, ground_file):
        """Read any trec file in base_path that match the given prefix
        Args:
            base_path: path to search for.
            prefix: the prefix to match in base_path
            ground_file: the path to the ground truth file
        """
        ## Create regex and find files
        r = re.compile(prefix + "*")
        selected = list(filter(r.match, os.listdir(base_path)))
        # With files found, parse parameters
        self.selected = list(map(lambda x: Result(base_path + '/' + x, x), selected))
        # Determine unique diffusion algorithms
        self.unique_algorithms = set([ selec.algorithm.name for selec in self.selected])
        # Compute ndcg
        for result in self.selected:
            result.compute_ndcg(ground_file)
        # Determine unique query types
        self.unique_query_types = set([ class_ for class_, _ in Result.query_classification])

    def classify_by_algorithm(self):
        """ Classify selected results according to their algorithms.
        Response:
             a map with the classification
        """
        # sort results by algorithm
        sorted_selected = sorted(self.selected, key = lambda x:x.algorithm.name)
        classified = {}
        for algorithm, group in groupby(sorted_selected, key = lambda x:x.algorithm.name):
            classified[algorithm] = list(group)
        return classified

    def get_ndcg_lazy_vs_kernel_table(self, classified, diffusion, at, filters = None):
        """ Generate a dataframe for the model defined in diffusion, containing the ndcg
        where the raws are the lazy parameters  and the columns the kernel parameters
        Args:
            classified: a map of the classified models
            diffusion: name of the diffusion to generate table
            at: property of the table to extract, 0 or 1
            filters: if the property to extract has a category
        Response:
            a tuple containing the dataframe and its caption
        """
        values = []
        category = classified[diffusion]
        # For categories that do not have lazy or kernel parameter, print one value
        if diffusion in ['text']:
            new_group = { 'value' : category[0].get_mean(at, filters),
                    'index' : str(category[0].algorithm) }
            values.append(new_group)
        else:
            # Sort and group by according to lazy parameter
            sorted_classified = sorted(category, key = lambda x:x.lazy.parameters[0])
            for lazy, group in groupby(sorted_classified, key = lambda x: str(x.lazy)):
                # compute average ndcg for each group
                new_group = {
                    str(result.kernel) : result.get_mean(at, filters)
                    for result in group }
                new_group['index'] = str(lazy)
                values.append(new_group)
        df = pd.DataFrame(values)
        df.set_index('index')
        return (df, get_caption(diffusion, filters))

    def find_best_by_diffusion(self, classified, at, filters = None):
        """ For given model, show it best performance
        Args:
            classified: a map of the classified models
            at: property
            filters: filters
        """
        # For all diffusions, find maximum and print
        output = []
        for algorithm in self.unique_algorithms:
            table, _ = self.get_ndcg_lazy_vs_kernel_table(classified, algorithm, at, filters)
            # Find maximum
            table_max = (0.0, "", "", "")
            for column in list(table.columns.values):
                if column == "index":
                    continue
                max_ = table[column].max()
                if max_ > table_max[0]:
                    idx = table[column].idxmax()
                    index = table['index'].loc[idx]
                    table_max = (max_, index, column, algorithm)
            output.append(table_max)
        return output

    def find_best_by_query_type(self, classified, at):
        """ Show best configuration according to the query type
        Args:
            classified: a map of the classified models
            at: property
        """
        output = []
        for query_type in self.unique_query_types:
            best = self.find_best_by_diffusion( classified, at, query_type )
            table_max = (0, "", "", "", "")
            for max_, index, column, algorithm in best:
                if max_ > table_max[0]:
                    table_max = (max_, index, column, algorithm, query_type)
            if table_max[0] > 0.0:
                # only include if value is greater than zero
                output.append(table_max)
        return output

def display_table(df):
    """ Display table df using a customised style
    Args:
        df: Dataframe to display
    """
    (df, caption) = df
    s = df.style.background_gradient(cmap = "Reds", low = 0.0, high = 1.0).\
        set_caption(caption)
    display(s)

def get_caption(diffusion, query):
    """ Generate caption for model
    Args:
        model: name of the model
        diffusion: name of the diffusion
        query: name of the query type
    """
    if query == None:
        query = 'all'
    return "DIFFUSION: {}, QUERY_TYPE: {} ".format(diffusion, query)

def display_table_by_diffusion(results, classified, at):
    """ For all diffusion in diffusions, show ndcg table
    Args:
        classified: a map of the classified models
        model: name of the model.
        diffusions: name of the diffusions
        at: property
    """
    for diffusion in classified.keys():
        display_table(results.get_ndcg_lazy_vs_kernel_table(classified, diffusion, at))

def display_tables_by_query_types(classified, model, diffusion, queries, at):
    """ Show tables by query types.
    """
    for query in queries:
        display_table(get_table_ndcg(classified, model, diffusion, at, query))
