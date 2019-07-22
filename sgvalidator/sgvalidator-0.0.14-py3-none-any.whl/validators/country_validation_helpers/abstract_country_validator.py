from abc import ABC, abstractmethod


class AbstractCountryValidator(ABC):
    @abstractmethod
    def validate(self, row):
        pass

    @abstractmethod
    def validateState(self, row):
        pass

    @abstractmethod
    def validateZip(self, row):
        pass

    @abstractmethod
    def validatePhone(self, row):
        pass
