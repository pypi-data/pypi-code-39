from logous.basemodel import LogousEstimatorBase
from xgboost import XGBClassifier


class LogousChurnUtils(LogousEstimatorBase):
    def __init__(self, passed_cls=None):
        LogousEstimatorBase.__init__(self, passed_cls)

    def fit(self, **kwargs):
        # Churn problemi için en iyi sonucu veren modellerden birisi XGBoost olduğu için
        # default olarak kullanabiliriz.

        if self.passed_cls is None:
            # Default parametreler
            xgc = XGBClassifier(base_score=0.5, booster='gbtree', colsample_bylevel=1,
                                colsample_bytree=1, gamma=0, learning_rate=0.9, max_delta_step=0,
                                max_depth=7, min_child_weight=1, missing=None, n_estimators=100,
                                n_jobs=1, objective='binary:logistic', random_state=0,
                                reg_alpha=0, reg_lambda=1, scale_pos_weight=1,
                                silent=True, subsample=1)
            xgc.fit(self.dataframe_X, self.dataframe_y)
            self.cls = xgc
        else:
            self.cls.fit(self.dataframe_X, self.dataframe_y, **kwargs)

    def predict(self, test_X, **kwargs):
        return self.cls.predict(test_X, **kwargs)

    def preprocess(self):
        # task'a özel preprocess işlemleri burda yapılabilir.
        return self.dataframe_X
