import pandas as pd
import numpy as np

from keras.optimizers import Adam
from sklearn.preprocessing import MinMaxScaler
from .model import regression_model
from ...application import Application

class DataRegression(Application):
    def __init__(self, weights_path=None, factors_path=None):
        super().__init__()

        self.model = None
        self.factors_info = None

        if weights_path is not None and factors_path is not None:
            self.load(weights_path, factors_path)

    def train(self,
              data_path,
              epochs=1,
              batch_size=1,
              learning_rate=1e-3,
              verbose=0):
        data_frame = pd.read_csv(data_path, delim_whitespace=True)
        self.factors_info = self.get_factors_info(data_frame)
        num_factor = len(self.factors_info)
        normalized_dataset = self.normalize_train_dataset(data_frame)
        x = normalized_dataset[:, :num_factor - 1]
        y = normalized_dataset[:, num_factor - 1]

        if self.model is None:
            self.model = self.create_model(num_factor)

        optimizer = Adam(lr=learning_rate, decay=1e-6)
        self.model.compile(loss='mean_squared_error', optimizer=optimizer)

        self.model.fit(x, y,
                       epochs=epochs,
                       batch_size=batch_size,
                       verbose=verbose)

    def predict(self, data_array):
        num_factors_without_result = len(self.factors_info) - 1
        min_array = self.factors_info[:num_factors_without_result, 1]
        min_array = min_array.astype('float64')
        max_array = self.factors_info[:num_factors_without_result, 2]
        max_array = max_array.astype('float64')
        max_minus_min_array = max_array - min_array
        data_minus_min_array = data_array - min_array
        normalized_array = data_minus_min_array / max_minus_min_array

        normalized_results = self.model.predict(normalized_array)
        min_results = self.factors_info[num_factors_without_result, 1]
        min_results = min_results.astype('float64')
        max_results = self.factors_info[num_factors_without_result, 2]
        max_results = max_results.astype('float64')
        max_minus_min_results = max_results - min_results
        results = min_results + max_minus_min_results * normalized_results
        return results

    def load(self, weights_path, factors_path):
        factors_info = []
        with open(factors_path, 'r') as f:
            while True:
                line = f.readline()
                if not line:
                    break
                factor = line.split(' ')
                factors_info.append(np.asarray(factor))

        self.factors_info = np.asarray(factors_info)
        num_factor = len(self.factors_info)
        self.model = self.create_model(num_factor)
        self.model.load_weights(weights_path)

    def save(self, weights_path, factors_path):
        self.model.save_weights(weights_path)

        with open(factors_path, 'w') as f:
            for i in range(len(self.factors_info)):
                factor = self.factors_info[i]
                f.write(str(factor[0]) + " ")
                f.write(str(factor[1]) + " ")
                f.write(str(factor[2]))
                if i != len(self.factors_info):
                    f.write('\n')

    def create_model(self, num_factor):
        return regression_model(num_factor)

    def normalize_train_dataset(self, data_frame):
        dataset = data_frame.values
        normalized_dataset = MinMaxScaler().fit_transform(dataset)

        return normalized_dataset

    def get_factors_info(self, data_frame):
        num_factor = len(data_frame.columns)
        factors = data_frame.columns.values[:num_factor].reshape(-1, 1)
        maxs = data_frame.max().to_frame().T.values[0][:num_factor].reshape(-1,
                                                                            1)
        mins = data_frame.min().to_frame().T.values[0][:num_factor].reshape(-1,
                                                                            1)
        return np.hstack((factors, mins, maxs))
