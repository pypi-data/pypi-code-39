from logous.basemodel import LogousEstimatorBase
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf
import pandas as pd


class LogousLSTMUtils(LogousEstimatorBase):
    scaler = MinMaxScaler()

    def __init__(self, passed_cls=None):
        LogousEstimatorBase.__init__(self, passed_cls)

    def fit(self, **kwargs):
        if self.passed_cls is None:
            # Default parametreler
            data = self.preprocess()
            X = data.iloc[:, :-1].values
            y = data.iloc[:, -1].values
            X = X.reshape((X.shape[0], 1, X.shape[1]))

            model = tf.keras.models.Sequential()
            model.add(
                tf.keras.layers.LSTM(32, dropout=0.3, input_shape=(X.shape[1], X.shape[2]), return_sequences=True))
            model.add(tf.keras.layers.LSTM(32, dropout=0.3))
            model.add(tf.keras.layers.Dense(1, activation="tanh"))
            model.compile(loss="mse", optimizer="adam")

            model.fit(X,
                      y,
                      epochs=100,
                      batch_size=128,
                      verbose=0,
                      callbacks=[tf.keras.callbacks.EarlyStopping(monitor="val_loss", patience=10),
                                 tf.keras.callbacks.ReduceLROnPlateau()],
                      validation_split=0.2)
            self.cls = model
        else:
            self.cls.fit(self.dataframe_X, self.dataframe_y, **kwargs)

    def predict(self, test_X, **kwargs):
        if self.passed_cls is None:
            test_size = 120

            data = self.preprocess()
            X = data.iloc[:, :-1].values
            X = X.reshape((X.shape[0], 1, X.shape[1]))

            test_X = X[-test_size:]

            predictions = self.cls.predict(test_X).flatten()
            inv_pred = self.scaler.inverse_transform(predictions.reshape(-1, 1))
            return inv_pred
        else:
            return self.cls.predict(test_X, **kwargs)

    def preprocess(self):
        # task'a özel preprocess işlemleri burda yapılabilir.
        data = self.dataframe_X.copy()
        data['YAKILAN_KONTOR'] = self.scaler.fit_transform(data['YAKILAN_KONTOR'].values.reshape(-1, 1))
        return LogousLSTMUtils.timeseries_to_supervised(data, 120)

    @staticmethod
    def timeseries_to_supervised(data, lag=1):
        df = pd.DataFrame(data)
        columns = [df.shift(i) for i in range(1, lag + 1)]
        columns.append(df)
        df = pd.concat(columns, axis=1)
        df.fillna(0, inplace=True)
        return df
