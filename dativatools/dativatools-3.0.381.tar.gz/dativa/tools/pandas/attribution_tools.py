"""Attribution methods implemented on pandas dataframes."""
import math
import logging
import multiprocessing
from .columns import get_unique_column_name

logger = logging.getLogger('dativa.attribution.shapley')

try:
    import pandas as pd
except ImportError:
    pd = None


def _get_marginal_score(pop_size,
                        item_label,
                        scores,
                        infer_missing,
                        default_value):
    score = 0
    skipped = 0
    run = 0
    total_scored = 0
    total_skipped = 0

    for label in scores:
        if label & item_label > 0:
            run = run + 1
            subset_label = label - item_label
            superset_score = scores.get(subset_label + item_label, default_value)
            subset_score = scores.get(subset_label, default_value)

            total_scored = total_scored + superset_score

            if subset_label > 0 and infer_missing and (superset_score == 0 or subset_score == 0):
                if superset_score > 0 or subset_score > 0:
                    skipped = skipped + 1
                    total_skipped = total_skipped + superset_score
            else:
                j = len([a for a in bin(subset_label) if a == '1'])
                score = score + (superset_score - subset_score) * math.factorial(j) * math.factorial(
                    pop_size - j - 1)

    return score, skipped, run, total_scored, total_skipped


# Wrapper function for the multithreading to populate the shared results
def _score(results,
           skipped,
           run,
           total_scored,
           total_skipped,
           element,
           pop_size,
           item_label,
           scores,
           infer_missing,
           default_value):
    results[element], skipped[element], run[element], total_scored[element], total_skipped[
        element] = _get_marginal_score(pop_size,
                                       item_label,
                                       scores,
                                       infer_missing,
                                       default_value)


class Shapley:
    """Shapley attribution of scores to members of sets.

    See `medium <https://towardsdatascience.com/one-feature-attribution-method-to-supposedly-rule-them-all-shapley-values-f3e04534983d>`_
    or `wiki <https://en.wikipedia.org/wiki/Shapley_value>`_ for details on the math. The aim is to apportion scores between the members of a set
    responsible for producing that score.

    :param df_impression: impression data to be parsed.
    :param df_conversions: conversion events to score
    :param id_column: column containing the id values of users who viewed impressions / converted.
    :param sets_column: label of the column containing features
    :param default_score: score to assign to any combination that has not been observed, defaults to 0.
    :param infer_missing: {'average', 'regression', 'filter', False} defaults to False. To be implemented
    :param metric: The column used to calculate the Shapley value
    :param normalize_impressions: defaults to True, normalize the score column according to the number of impressions

    :type df_impressions:  pandas.DataFrame
    :type df_conversions:  pandas.DataFrame
    :type id_column: str
    :type sets_column: str
    :type default_score: int or float
    :type infer_missing: bool or str
    """

    def __init__(self,
                 df_impression,
                 df_conversions,
                 id_column,
                 sets_column,
                 default_score=0,
                 infer_missing=False,
                 normalize_impressions=True,
                 metric='conversions'):

        if not pd:
            raise ImportError("pandas must be installed to run Shapley")

        if infer_missing and infer_missing not in ('filter'):  # to be extended
            raise KeyError('{} is not a valid option for infer_missing'.format(infer_missing))

        self.default_value = default_score
        self.infer_missing = (infer_missing == 'filter')
        self.normalize_impressions = normalize_impressions

        if metric in df_conversions.columns.tolist():
            self.conversion_col = metric
        elif metric in ['conversions']:
            # this is redundant because we've already checked if it's in the df, which sort of defeats the purpose?
            # i'll have to think about how anyone would actually use this
            self.conversion_col = get_unique_column_name(df_conversions, metric)
        else:
            raise KeyError('{} is not a valid option for metric'.format(metric))

        if type(default_score) is not int:
            raise TypeError('default_score: {} is not valid - must be numeric'.format(default_score))

        self.sets_column = sets_column

        self.population = df_impression[sets_column].unique()
        self.conversion_dict = self._build_conversion_dict(self.population)

        self._build_scores(df_impression, df_conversions, id_column, default_score)

    def _build_scores(self, df_campaigns, df_conversions, id_column, default_value):

        set_column = get_unique_column_name(df_campaigns, 'set_column')

        # Group by the exposed device and assign the integer label for the set of campaigns viewed...
        lookup = pd.DataFrame.from_dict(self.conversion_dict, orient='index', columns=[set_column])
        g = df_campaigns.drop_duplicates().join(lookup, on=self.sets_column).groupby(id_column, as_index=False)[
            set_column].sum()

        # Add a conversion column if we don't already have it
        if self.conversion_col not in df_conversions.columns:
            df_conversions[self.conversion_col] = 1  # so we can count them
            m = pd.merge(g, df_conversions, on=id_column, how='left')
            df_conversions.drop(columns=self.conversion_col, inplace=True)
        else:
            m = pd.merge(g, df_conversions, on=id_column, how='left')

        # Now group by the set and count the number of conversions on each
        df_scored = m.groupby(set_column, as_index=False).agg({self.conversion_col: sum,
                                                               id_column: pd.Series.nunique})

        # Normalize the impressions by the number of devices that have seen it
        # Note this is not quite conversion rate
        if self.normalize_impressions:
            df_scored[self.conversion_col] = df_scored[self.conversion_col] / df_scored[id_column]

        # Get a set of the number of conversions for each set
        marked = df_scored.set_index(set_column)[self.conversion_col]

        # Reindex to include the missing sets and store in a numpy array
        self.scores = marked.to_dict()

    @staticmethod
    def _build_conversion_dict(population):
        # Convert a subset {x_i} into a unique integer sum( 2 ** i ) for i in [0, n)
        # vastly better performance
        return {member: 2 ** i for i, member in enumerate(population)}

    def _reverse_conversion_dict(self, l):
        return [list(self.conversion_dict.keys())[i] for i in
                [i for i, bit in enumerate(reversed([int(bit) for bit in "{0:b}".format(l)])) if bit == 1]]

    def run(self):

        # get the constant values
        pop_size = len(self.population)

        # Create a multithreading pool to handle the processing

        logger.info("Creating {0} processes".format(multiprocessing.cpu_count() - 1))
        pool = multiprocessing.Pool(multiprocessing.cpu_count() - 1)

        results = multiprocessing.Manager().dict()
        skipped = multiprocessing.Manager().dict()
        run = multiprocessing.Manager().dict()
        total_scored = multiprocessing.Manager().dict()
        total_skipped = multiprocessing.Manager().dict()

        for element in self.population:
            #     pool.apply_async(_score,
            #                      args=(results,
            #                            skipped,
            #                            run,
            #                            total_scored,
            #                            total_skipped,
            #                            element,
            #                            pop_size,
            #                            self.conversion_dict[element],
            #                            self.scores,
            #                            self.infer_missing,
            #                            self.default_value))
            # pool.close()
            # pool.join()

            _score(results,
                   skipped,
                   run,
                   total_scored,
                   total_skipped,
                   element,
                   pop_size,
                   self.conversion_dict[element],
                   self.scores,
                   self.infer_missing,
                   self.default_value)

        # Check the threads have worked - they fail silently if they don't work
        assert (len(results) == pop_size)

        # Finalize the calculation and log out bad results
        for element in self.population:
            results[element] = results[element] * (1 / math.factorial(len(self.population)))
            if skipped[element] > 0:
                logger.warning("Skipped {0}/{1} {3:.0%} for {2}".format(skipped[element], run[element], element,
                                                                        total_skipped[element] / total_scored[element]))
            if results[element] < 0:
                logger.warning("Negative score for {0} = {1}".format(element, results[element]))

        # Prepare the data frame to return
        df = pd.DataFrame.from_dict(results, orient='index')
        df.reset_index(inplace=True)
        df.rename(columns={'index': self.sets_column, 0: 'Shapley_val'}, inplace=True)
        df.sort_values('Shapley_val', ascending=False, inplace=True)
        df.reset_index(inplace=True, drop=True)

        return df
