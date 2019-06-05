from abc import ABC, abstractmethod


class Transformation(ABC):

    @abstractmethod
    def transform(self, df, *args, **kwargs):
        pass
