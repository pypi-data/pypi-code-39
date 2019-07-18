from keras.models import Sequential
from keras.layers import Dense


def regression_model(num_factors):
    model = Sequential()
    model.add(Dense(16, input_dim=num_factors - 1,
                    kernel_initializer='normal',
                    activation='relu'))
    model.add(Dense(6, kernel_initializer='normal',
                    activation='relu'))
    model.add(Dense(6, kernel_initializer='normal',
                    activation='relu'))
    model.add(Dense(1, kernel_initializer='normal'))

    return model
