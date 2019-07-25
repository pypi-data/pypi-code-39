from logous.basemodel import LogousEstimatorBase
import pandas as pd
from statsmodels.tsa.api import ExponentialSmoothing


class LogousHoltAndWinterUtils(LogousEstimatorBase):
    def __init__(self, passed_cls=None):
        LogousEstimatorBase.__init__(self, passed_cls)

    def fit(self, **kwargs):
        if self.passed_cls is None:
            # Default parametreler
            data = self.preprocess()
            model = ExponentialSmoothing(data, seasonal='add', seasonal_periods=10).fit()
            self.cls = model
        else:
            self.cls.fit(self.dataframe_X, **kwargs)

    def predict(self, test_X, **kwargs):
        if self.passed_cls is None:
            predictions = self.cls.predict(start=test_X.index[0], end=test_X.index[-1])
            return predictions
        else:
            predictions = self.cls.predict(start=test_X.index[0], end=test_X.index[-1], **kwargs)
            return predictions

    def preprocess(self):
        data = self.dataframe_X.copy()
        data['KONTOR_TARIHI'] = pd.to_datetime(data['KONTOR_TARIHI'])
        data = data[['KONTOR_TARIHI', 'YAKILAN_KONTOR']]
        data.set_index('KONTOR_TARIHI', inplace=True)
        data.sort_index(inplace=True)
        data = data.resample('W-MON', base=0).sum()
        return data
