import numpy as np
from sklearn.linear_model import LinearRegression
import pandas as pd


def building_regressor():
    return LinearRegression()


def building_train(regressor, data, value):
    # data.dropna(inplace=True)
    # value.dropna(inplace=True)
    # if not(type(data) == type(value)):
    #     raise TypeError('Was waiting from dataframes from pandas\' library')
    regressor.fit(data, value)


def building_prediction (regressor, data_df):
    result = regressor.predict(data_df)
    return result


if __name__ == '__main__':

    # Generate data
    X = np.array([[1, 1], [1, 2], [2, 2], [2, 3]])
    # y = 1 * x_0 + 2 * x_1 + 3
    y = np.dot(X, np.array([1, 2])) + 3

    my_reg = building_regressor()
    my_reg.fit(X, y)
    my_reg.score(X, y)
    my_reg.coef_
    my_reg.intercept_
    my_reg.predict(np.array([[3, 5]]))
