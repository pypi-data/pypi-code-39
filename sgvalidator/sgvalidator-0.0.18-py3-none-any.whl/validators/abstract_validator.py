from abc import ABC, abstractmethod


class AbstractValidator(ABC):
    @abstractmethod
    def validate(self):
        pass

    @abstractmethod
    def announce(self):
        pass
