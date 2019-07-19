from logous.basemodel import LogousEstimatorBase
import pandas as pd
from pyramid.arima import auto_arima


class LogousArimaUtils(LogousEstimatorBase):
    def __init__(self, passed_cls=None):
        LogousEstimatorBase.__init__(self, passed_cls)

    def fit(self, **kwargs):
        if self.passed_cls is None:
            # Default parametreler
            data = self.preprocess()
            model = auto_arima(data, start_p=1, start_q=1,
                               max_p=3, max_q=3, m=7,
                               start_P=0, seasonal=True,
                               d=1, D=1, trace=False,
                               error_action='ignore',
                               suppress_warnings=True,
                               stepwise=True)
            self.cls = model
        else:
            self.cls.fit(self.dataframe_X, **kwargs)

    def predict(self, test_X, **kwargs):
        if self.passed_cls is None:
            predictions = self.cls.predict(n_periods=len(test_X))
            return predictions
        else:
            predictions = self.cls.predict(n_periods=len(test_X), **kwargs)
            return predictions

    def preprocess(self):
        data = self.dataframe_X.copy()
        data['KONTOR_TARIHI'] = pd.to_datetime(data['KONTOR_TARIHI'])
        data = data[['KONTOR_TARIHI', 'YAKILAN_KONTOR']]
        data.set_index('KONTOR_TARIHI', inplace=True)
        data.sort_index(inplace=True)
        data = data.resample('W-MON', base=0).sum()
        return data
