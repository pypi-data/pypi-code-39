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

#這邊的資料是用來畫圖的,可以忽略!
class keras_model():

    def __init__(self):
        self.activation = 'relu'
        self.epoch = 20
        self.batch_size = 128
        print('--函式說明--')
        print('函式1: set_activation(變數名稱)               　=>用於設定活化函數為何\n')
        print('函式2: set_epoch(代數)                         =>用於設定要訓練幾代\n')
        print('函式3: set_train_data(變項資料,分類為何)        =>用於設定要訓練的資料為何\n')
        print('函式4: set_test_data(變項資料,分類為何)         =>用於設定批量大小為何\n')
        print('函式5: set_model(神經元個數的陣列)              =>用於設定隱藏層數量及層數為何\n')
        print('函式6: predict_data()                          =>用於預測新的數據\n')
        print('函式7: get_acc()                               =>用於得到此模型的正確率,回傳(訓練正確率,測試正確率)\n')
        print('函式8: show_history()                          =>用於顯示訓練過程\n')
        print('-----------')

    def set_activation(self,activation_name):
        activation_names = np.array(['relu','sigmoid'])
        if activation_name in activation_names:
            self.activation = activation_name
            print('Activation設定為:'+activation_name)
        else:
            print('目前不支援:'+activation_name)
            print('Activation將會預設為relu')

    def set_epoch(self,epoch):
        
        if epoch >10000:
            print('epoch請勿設定超過10000代，以避免系統當機!')
            return 
        elif epoch <1 :
            print('epoch請勿設定小於1代，以避免系統當機!')
            return

        self.epoch = epoch
        print('epoch設定為:'+str(epoch))

    def set_batch_size(self,batch_size):

        if batch_size >1000:
            print('batch_size請勿設定超過1000，以避免系統當機!')
            return 
        elif batch_size <1 :
            print('batch_size請勿設定小於1，以避免系統當機!')
            return

        self.batch_size = batch_size
        print('batch_size設定為:'+str(batch_size))

    def set_train_data(self,x_train,y_train):
        try:
            self.x_train = x_train
            self.Input_size = len(self.x_train[0])

            self.y_train = np_utils.to_categorical(y_train)
            self.Output_size = len(self.y_train[0])
            print('訓練資料設定成功')
        except:
            print('訓練資料輸入錯誤，請重新確認輸入資料的格式!')
        

    def set_test_data(self,x_test,y_test):
        try:
            self.x_test = x_test
            self.y_test = np_utils.to_categorical(y_test)
            print('測試資料設定成功')
        except:
            print('測試資料輸入錯誤，請重新確認輸入資料的格式!')
        
    def set_model(self,neuron_count):
        #check neuron_count correct
        for neuron in neuron_count:
            if neuron <=0:
                print('neuron 設定錯誤，不可小於等於0')
            elif neuron>10000:
                print('neuron 設定錯誤，不可大於10000')
        #check End
        self.model = Sequential()#先將模型初始化
        if len(neuron_count)>0:
            self.model.add(Dense(units = neuron_count[0],activation= self.activation,input_shape = (self.Input_size,)))
            for level_Index in range(1,len(neuron_count),1):
                self.model.add(Dense(units = neuron_count[level_Index],activation= self.activation))

            self.model.add(Dense(output_dim = self.Output_size,activation='softmax'))
        else:
            print('Linear Regression model')
            self.model.add(Dense(output_dim = self.Output_size,activation= 'softmax',input_shape = (self.Input_size,)))
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
        self.train_acc = score[1]
        print ('\nTrain Acc:', score[1])
        score = self.model.evaluate(self.x_test, self.y_test)
        self.test_acc = score[1]
        print ('\nTest Acc:', score[1])
        #開始使用修正完的參數做預測，並將"預測"的結果放置在classes裡面
        classes = self.model.predict_classes(self.x_test, batch_size=self.batch_size)
    
    def predict_data(self,predict_data):
        classes = self.model.predict_classes(predict_data, batch_size=self.batch_size)
        print('類別\t輸入')
        for dataindex in range(0,len(predict_data),1):
            print(classes[dataindex]+'\t'+str(predict_data))

    #用於獲得正確率
    def get_acc(self):
        return self.train_acc,self.test_acc

    #這邊的資料是用來畫圖的,可以忽略!
    def show_history(self):
        plt.subplot(211)
        plt.plot(self.train_history.history['acc'])
        plt.plot(self.train_history.history['val_acc'])
        plt.title('Train_Test History')
        plt.ylabel('acc')
        plt.legend(['train_acc', 'test_acc'], loc='upper left')
        

        plt.subplot(212)
        plt.plot(self.train_history.history['loss'])
        plt.plot(self.train_history.history['val_loss'])
        plt.ylabel('loss')
        plt.xlabel('Epoch')
        plt.legend(['train_loss', 'test_loss'], loc='upper left')
        plt.show()
def question():
    print('--函式說明--')
    print('函式1: set_activation(變數名稱)               　=>用於設定活化函數為何\n')
    print('函式2: set_epoch(代數)                         =>用於設定要訓練幾代\n')
    print('函式3: set_train_data(變項資料,分類為何)        =>用於設定要訓練的資料為何\n')
    print('函式4: set_test_data(變項資料,分類為何)         =>用於設定批量大小為何\n')
    print('函式5: set_model(神經元個數的陣列)              =>用於設定隱藏層數量及層數為何\n')
    print('函式6: predict_data()                          =>用於預測新的數據\n')
    print('函式7: get_acc()                               =>用於得到此模型的正確率,回傳(訓練正確率,測試正確率)\n')
    print('函式8: show_history()                          =>用於顯示訓練過程\n')
    print('-----------')
