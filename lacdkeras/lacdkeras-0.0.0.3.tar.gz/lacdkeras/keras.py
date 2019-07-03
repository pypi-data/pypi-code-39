import keras
import numpy as np
np.random.seed(1337)
import matplotlib.pyplot as plt
from keras.models import Sequential
from keras.layers import Dense
from keras.utils import to_categorical
from keras.utils import np_utils
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.optimizers import SGD
import lacdkeraspackage.DataProcessing as m2
#這邊的資料是用來畫圖的,可以忽略!
class keras_model():

    def __init__(self):
        self.activation = 'relu'
        self.epoch = 20
        self.batch_size = 128

    def set_activation(self,activation_name):
        activation_names = np.array(['relu','sigmoid'])
        if activation_name in activation_names:
            self.activation = activation_name
        else:
            print('目前不支援:'+activation_name)
            print('Activation將會預設為relu')

    def set_epoch(self,epoch):
        self.epoch = epoch

    def set_batch_size(self,batch_size):
        self.batch_size = batch_size

    def set_train_data(self,x_train,y_train):
        self.x_train = x_train
        self.y_train = np_utils.to_categorical(y_train)

    def set_test_data(self,x_test,y_test):
        self.x_test = x_test
        self.y_test = np_utils.to_categorical(y_test)

    def set_model(self,Input_size,output_size,neuron_count):

        self.model = Sequential()#先將模型初始化
        self.model.add(Dense(input_dim = Input_size,units = neuron_count[0],activation= self.activation))
        for level_Index in range(1,len(neuron_count),1):
            self.model.add(Dense(units = neuron_count[level_Index],activation= self.activation))

        self.model.add(Dense(output_dim = 5,activation='softmax'))
        self.model.compile(loss='categorical_crossentropy', optimizer=SGD(lr=0.01, momentum=0.9, nesterov=True), metrics=['accuracy'])
        self.model.summary()#顯示目前建立的模型結構


        self.train_history = self.model.fit(self.x_train, self.y_train,      #輸入 與 輸出
                  nb_epoch = self.epoch,       #子代數
                  batch_size = self.batch_size,#批量大小 一次參考多少的數據 4=> 00 01 10 11一同參考
                  verbose = 1 ,           #是否顯示訓練過程 1=>是  2=>否
                  validation_data=(self.x_test, self.y_test)) #拿來預測的資料  (此使用與輸入相同的資料!)
        #train_history 為紀錄更新的軌跡圖

        #最後輸出測試資料跟訓練資料的正確率!
        score = self.model.evaluate(self.x_train, self.y_train,)
        print ('\nTrain Acc:', score[1])
        score = self.model.evaluate(self.x_test, self.y_test)
        print ('\nTest Acc:', score[1])
        #開始使用修正完的參數做預測，並將"預測"的結果放置在classes裡面
        classes = self.model.predict_classes(self.x_test, batch_size=self.batch_size)
    
    #這邊的資料是用來畫圖的,可以忽略!
    def show_train_history(self):
        plt.plot(self.train_history.history['acc'])
        plt.plot(self.train_history.history['val_acc'])
        plt.title('Train History')
        plt.ylabel('acc')
        plt.xlabel('Epoch')
        plt.legend(['train', 'test'], loc='upper left')
        plt.show()