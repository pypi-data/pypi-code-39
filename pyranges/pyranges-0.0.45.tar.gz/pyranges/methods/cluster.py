
import pandas as pd

from sorted_nearest import annotate_clusters


def _cluster(df, kwargs):

    if df.empty:
        return None


    slack = kwargs.get("slack", 0)

    cdf = df.sort_values("Start")

    ids = annotate_clusters(cdf.Start.values, cdf.End.values, slack)

    cdf.insert(df.shape[1], "Cluster", ids)
    return cdf
