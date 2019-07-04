# -*- coding: UTF-8 -*-
# !/usr/bin/python
# @time     :2019/5/12 11:24
# @author   :Mo
# @function :
import keras.backend as k_keras
from keras.layers import Bidirectional
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import Flatten
from keras.layers import LSTM
from keras.layers import Lambda
from keras.layers import Multiply
from keras.layers import Permute
from keras.layers import RepeatVector
from keras.models import Model


def attention(inputs, single_attention_vector=False):
    #attention机制
    time_steps = k_keras.int_shape(inputs)[1]
    input_dim = k_keras.int_shape(inputs)[2]
    x = Permute((2, 1))(inputs)
    x = Dense(time_steps, activation='softmax')(x)
    if single_attention_vector:
        x = Lambda(lambda x: k_keras.mean(x, axis=1))(x)
        x = RepeatVector(input_dim)(x)

    a_probs = Permute((2, 1))(x)
    output_attention_mul = Multiply()([inputs, a_probs])
    return output_attention_mul

def bilstm(X_train, y_train,X_test, y_test):
    inputs = Input(shape=(TIME_STEPS, INPUT_DIM))
    drop1 = Dropout(0.3)(inputs)
    lstm_out = Bidirectional(LSTM(lstm_units, return_sequences=True), name='bilstm')(drop1)
    attention_mul = attention(lstm_out)
    attention_flatten = Flatten()(attention_mul)
    drop2 = Dropout(0.25)(attention_flatten)
    output = Dense(10, activation='sigmoid')(drop2)
    model = Model(inputs=inputs, outputs=output)
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    print(model.summary())
    print('Training————')
    model.fit(X_train, y_train, epochs=10, batch_size=10)
    print('Testing————–')
    loss, accuracy = model.evaluate(X_test, y_test)
    print('test loss:', loss)
    print('test accuracy:', accuracy)