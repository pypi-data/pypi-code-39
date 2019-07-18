from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten, BatchNormalization
from keras.layers.convolutional import Conv2D, MaxPooling2D, AveragePooling2D
from keras.regularizers import l2


def small_cnn(num_emotions):
    model = Sequential()

    model.add(Conv2D(64, (5, 5), activation='relu', input_shape=(48, 48, 1)))
    model.add(MaxPooling2D(pool_size=(5, 5), strides=(2, 2)))

    model.add(Conv2D(64, (3, 3), activation='relu'))
    model.add(Conv2D(64, (3, 3), activation='relu'))
    model.add(AveragePooling2D(pool_size=(3, 3), strides=(2, 2)))

    model.add(Conv2D(128, (3, 3), activation='relu'))
    model.add(Conv2D(128, (3, 3), activation='relu'))
    model.add(AveragePooling2D(pool_size=(3, 3), strides=(2, 2)))

    model.add(Flatten())

    model.add(Dense(1024, activation='relu'))
    model.add(Dropout(0.2))
    model.add(Dense(1024, activation='relu'))
    model.add(Dropout(0.2))

    model.add(Dense(num_emotions, activation='softmax'))

    return model


def simple_cnn(num_emotions):
    model = Sequential()
    model.add(Conv2D(filters=16, kernel_size=(7, 7), padding='same',
                     input_shape=(48, 48, 1)))
    model.add(BatchNormalization())
    model.add(Conv2D(filters=16, kernel_size=(7, 7), padding='same',
                     activation='relu'))
    model.add(BatchNormalization())
    model.add(AveragePooling2D(pool_size=(2, 2), padding='same'))
    model.add(Dropout(.5))

    model.add(Conv2D(filters=32, kernel_size=(5, 5), padding='same',
                     activation='relu'))
    model.add(BatchNormalization())
    model.add(Conv2D(filters=32, kernel_size=(5, 5), padding='same',
                     activation='relu'))
    model.add(BatchNormalization())
    model.add(AveragePooling2D(pool_size=(2, 2), padding='same'))
    model.add(Dropout(.5))

    model.add(Conv2D(filters=64, kernel_size=(3, 3), padding='same',
                     activation='relu'))
    model.add(BatchNormalization())
    model.add(Conv2D(filters=64, kernel_size=(3, 3), padding='same',
                     activation='relu'))
    model.add(BatchNormalization())
    model.add(AveragePooling2D(pool_size=(2, 2), padding='same'))
    model.add(Dropout(.5))

    model.add(Conv2D(filters=128, kernel_size=(3, 3), padding='same',
                     activation='relu'))
    model.add(BatchNormalization())
    model.add(Conv2D(filters=128, kernel_size=(3, 3), padding='same',
                     activation='relu'))
    model.add(BatchNormalization())
    model.add(AveragePooling2D(pool_size=(2, 2), padding='same'))
    model.add(Dropout(.5))

    model.add(Conv2D(filters=256, kernel_size=(3, 3), padding='same',
                     activation='relu'))
    model.add(BatchNormalization())
    model.add(Conv2D(filters=num_emotions, kernel_size=(3, 3), padding='same',
                     activation='relu'))

    model.add(Flatten())

    model.add(Dense(1024, activation='relu'))
    model.add(Dropout(0.4))
    model.add(Dense(512, activation='relu'))
    model.add(Dropout(0.4))

    model.add(Dense(num_emotions, activation='softmax'))

    return model


def regularized_cnn(num_emotions):
    model = Sequential()

    model.add(Conv2D(48, kernel_size=(3, 3), activation='relu',
                     input_shape=(48, 48, 1),
                     data_format='channels_last', kernel_regularizer=l2()))
    model.add(Conv2D(48, kernel_size=(3, 3), activation='relu',
                     padding='same'))
    model.add(BatchNormalization())
    model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))
    model.add(Dropout(0.5))

    model.add(Conv2D(2 * 48, kernel_size=(3, 3), activation='relu',
                     padding='same'))
    model.add(BatchNormalization())
    model.add(Conv2D(2 * 48, kernel_size=(3, 3), activation='relu',
                     padding='same'))
    model.add(BatchNormalization())
    model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))
    model.add(Dropout(0.5))

    model.add(
        Conv2D(2 * 2 * 48, kernel_size=(3, 3), activation='relu',
               padding='same'))
    model.add(BatchNormalization())
    model.add(
        Conv2D(2 * 2 * 48, kernel_size=(3, 3), activation='relu',
               padding='same'))
    model.add(BatchNormalization())
    model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))
    model.add(Dropout(0.5))

    model.add(
        Conv2D(2 * 2 * 2 * 48, kernel_size=(3, 3), activation='relu',
               padding='same'))
    model.add(BatchNormalization())
    model.add(
        Conv2D(2 * 2 * 2 * 48, kernel_size=(3, 3), activation='relu',
               padding='same'))
    model.add(BatchNormalization())
    model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))
    model.add(Dropout(0.5))

    model.add(Flatten())

    model.add(Dense(2 * 2 * 2 * 48, activation='relu'))
    model.add(Dropout(0.4))
    model.add(Dense(2 * 2 * 48, activation='relu'))
    model.add(Dropout(0.4))
    model.add(Dense(2 * 48, activation='relu'))
    model.add(Dropout(0.5))

    model.add(Dense(num_emotions, activation='softmax'))

    return model
