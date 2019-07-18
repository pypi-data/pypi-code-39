import numpy as np
from collections import Counter
import pandas as pd


class CategoricalTransformer:
    dictionary = {}

    def __init__(self, unknown_fill=np.nan, min_freq=0, low_freq_fill=-1, nan_fill=np.nan):
        self.unknown_fill = unknown_fill
        self.min_freq = min_freq
        self.low_freq_fill = low_freq_fill
        self.nan_fill = nan_fill

    def fit(self, l):
        value_counts = Counter(l)
        high_freq = []
        low_freq = []
        for v, c in value_counts.items():
            if c >= self.min_freq:
                high_freq.append(v)
            else:
                low_freq.append(v)
        for i, u in enumerate(high_freq):
            self.dictionary[u] = i
        for u in low_freq:
            self.dictionary[u] = self.low_freq_fill

    def transform(self, l):
        transformed = []
        for elem in l:
            if pd.isnull(elem):
                transformed.append(self.nan_fill)
            elif elem in self.dictionary:
                transformed.append(self.dictionary[elem])
            else:
                transformed.append(self.unknown_fill)
        return transformed

    def fit_transform(self, l):
        self.fit(l)
        return self.transform(l)