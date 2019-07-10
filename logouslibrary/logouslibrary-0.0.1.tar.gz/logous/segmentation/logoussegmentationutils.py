from logous.basemodel import LogousEstimatorBase
from sklearn.cluster import KMeans


class LogousSegmentationUtils(LogousEstimatorBase):
    def __init__(self, passed_cls=None):
        LogousEstimatorBase.__init__(self, passed_cls)

    def fit(self, **kwargs):
        if self.passed_cls is None:
            # Default parametreler
            kmeans = KMeans(n_clusters=4)
            kmeans.fit(self.dataframe_X)
            self.cls = kmeans
        else:
            self.cls.fit(self.dataframe_X, **kwargs)

    def predict(self, test_X, **kwargs):
        return self.cls.predict(test_X, **kwargs)

    def preprocess(self):
        # task'a özel preprocess işlemleri burda yapılabilir.
        return self.dataframe_X
