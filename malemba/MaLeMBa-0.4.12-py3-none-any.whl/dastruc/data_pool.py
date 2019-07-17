# malemba.ModelBase methods can input DataPool object or any other supported data structure.
# If an input for a model method is not DataPool object (but supported structure)
# it is to be converted to DataPool inside the method.
# DataPool features, labels, feature_types should be similar to the same attributes of model (inherited from ModelBase).
# DataPool can store a shape of the data (speeds up data preparation for generators).
# DataPool may store a scheme of the data and optionally check if X corresponds to the scheme.
# Analogy: DataPool - pandas.DataFrame, DataLevel - pandas.Series, FeatureVector - tree leaf


class DataPool(object):
    # Multilevel structures consist of DataLevel objects inclusions

    def __init__(self, data, data_level=1, shape=None, scheme=None):
        self.data = data
        self.data_level = data_level
        self.shape = shape
        self.scheme = scheme

        self.prepared = False

    def __iter__(self):
        for data_part in self.data:
            yield self._get_sub(data_part)

    def __getitem__(self, item):
        return self._get_sub(self.data[item])

    def _get_sub(self, data_part):
        # defines what structure to return: DataLevel or FeatureVector
        return

    def __setitem__(self, key, value):
        pass

    def check_scheme(self):
        return

    def dump(self, dump_path, prepared=False):
        """
        method for DataPool object dump to the disk
        :param dump_path: the path to ...
        :param prepared: set it True if the data are fully prepared and ready directly for learning
        :return: dump_path
        """
        self.prepared = prepared

        return dump_path

    @classmethod
    def load(cls, load_path):
        return


class DataLevel(list):  # list can be not good solution for base class
    pass


class FeatureVector(dict):  # dict can be not good solution for base class
    pass
