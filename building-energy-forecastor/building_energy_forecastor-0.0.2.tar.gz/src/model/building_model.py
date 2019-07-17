import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_log_error
import matplotlib.pyplot as plt
import sklearn.model_selection as xval
import preprocess.building_preprocess as bp
import forestci as fci
import pandas as pd


def building_regressor():
    """
    Returns a model, here a RandomForestRegressor.

    :return: RandomForestRegressor()
    """
    return RandomForestRegressor(n_estimators=100, random_state=42)


def clusterisation(data, targetindex='Value'):
    """
    Split the data into training part and test part to compute an error and
    a confidence interval.

    :param data: data to split
    :return: (x_train, x_test, y_train, y_test) explicitly what they are.
    """

    data.dropna(inplace=True)
    try:
        return xval.train_test_split(data.drop(columns=[targetindex]), data[targetindex])
    except KeyError:
        targetindex = input('What\'s the column\'s name where the objective values are stored ?\n Enter the name: ')
        return xval.train_test_split(data.drop(columns=[targetindex]), data[targetindex])


def building_train(regressor, x_train, y_train):
    """
    Trains the model. Does not return anything.
    In preprocessing: drop columns with values not convertible in float64.

    :param regressor: model
    :param data: data to train on
    :param targetindex: column's name of the target (y_train)
    :return: None
    """
    bool_lol = True
    for col in x_train.columns:
        try:
            int(x_train.loc[0, col])
        except TypeError:
            print('Is that the columns containing the date/time: {} ?'.format(col))
            answer = input('Enter (y/n):  ')
            while answer != 'y' or 'n':
                print('Write y or n !')
                answer = input('Enter (y/n):  ')
            if answer == 'y'and bool_lol==True:
                x_train = bp.set_time_index(x_train, timeindex=col)
                bool_lol = False
            else:
                x_train.drop(columns=[col], inplace=True)

    regressor.fit(x_train, y_train)


def building_prediction(regressor, data_df):
    """
    Gives a pandas.DataFrame showing the prediction of the model on the data_df.
    Indexed with the timestamp from the data input.

    :param regressor: trained model
    :param data_df: data on which to make the prediction
    :return: the prediction
    """
    data_df.dropna(inplace=True)
    data_df = bp.set_time_index(data_df)
    result_array = regressor.predict(data_df)
    result_df = pd.DataFrame(data=result_array, index=data_df.index)
    return result_df


def error_computation(y_true, y_hat):
    """
    Returns the error calculated by mean_squared_log_error.

    :param y_true: the truth
    :param y_hat: the prediction
    :return: le mean_squared_log_error
    """

    return mean_squared_log_error(y_true, y_hat)


def intervalle_confiance(reg, x_train, x_test):
    """
    Estimate the "intervalle de confiance" of the model.

    :return:
    """

    return fci.random_forest_error(reg, x_train, x_test)


def visualisation(data, reg, valueindex='Value', timeindex='Timestamp'):
    """
    Takes a csv file and plot it. Need to identify the columns ? OF COURSE !
    How ? Just a plot ?

    :param result:
    :param x_test:
    :param timeindex:
    :return:
    """
    try:
        data.drop(columns=[timeindex], inplace=True)
        data.dropna(inplace=True)
    except KeyError:
        print("LOOOOOOOOOOOOOOOOOOOOOL")
    x_train, x_test, y_train, y_test = xval.train_test_split(data.drop(columns=[valueindex]), data[valueindex])
    building_train(reg, x_train, y_train)
    unbiased = intervalle_confiance(reg, x_train, x_test)
    y_hat = building_prediction(reg, x_test)
    plt.errorbar(y_test, y_hat, yerr=np.sqrt(unbiased), fmt='o')
    plt.plot([5, 45], [5, 45], 'k--')
    plt.xlabel('Reported MPG')
    plt.ylabel('Predicted MPG')
    plt.show()



if __name__ == '__main__':

    # Generate data
    X = np.array([[1, 1], [1, 2], [2, 2], [2, 3]])
    # y = 1 * x_0 + 2 * x_1 + 3in
    y = np.dot(X, np.array([1, 2])) + 3
    print(y)
    my_reg = building_regressor()
    my_reg.fit(X, y)
    my_reg.score(X, y)
    my_reg.coef_
    my_reg.intercept_
    print(my_reg.predict(np.array([[3, 5]])))
