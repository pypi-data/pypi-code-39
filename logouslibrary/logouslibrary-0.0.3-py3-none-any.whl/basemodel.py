"""
// loadData(dataframe) x
// Train x
// predict x
// hyperparametreleri tutan bi dictionary olacak
// preproces method
// scikit base predictor
"""
from abc import ABC, abstractmethod


class LogousEstimatorBase(ABC):
    def __init__(self, passed_cls=None):
        # Train dataframe
        self.dataframe_X = None

        # Test dataframe
        self.dataframe_y = None

        # Modelin parametrelerini ve diğer gerekli parametreleri tutabileceğimiz dict.
        self.parameters = None

        # Utils sınıfı içinde kullanılacak olan classifier / clustering algoritması refaransı
        self.cls = None

        # Dışarıdan model geçmek için kullanılacak olan classifier / clustering algoritması refaransı
        self.passed_cls = passed_cls

        # Eğer dışarıdan custom model verilirse onu kullanacağız.
        if passed_cls is not None:
            self.cls = passed_cls

    def load_data(self, dataframe_X, dataframe_y=None):
        self.dataframe_X = dataframe_X
        self.dataframe_y = dataframe_y

    def get_train_data(self):
        return self.dataframe_X

    def get_test_data(self):
        return self.dataframe_y

    @abstractmethod
    def fit(self, **kwargs):
        pass

    @abstractmethod
    def predict(self, test_X, **kwargs):
        pass

    @abstractmethod
    def preprocess(self):
        pass

    def set_parameters(self, parameters):
        self.parameters = parameters

    def get_parameters(self):
        return self.parameters

    def get_cls(self):
        return self.cls
