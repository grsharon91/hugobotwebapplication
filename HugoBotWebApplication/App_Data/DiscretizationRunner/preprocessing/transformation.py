from abc import ABC, abstractmethod


class Transformation(ABC):
    """
        An interface class for performing pre-processing on a dataset before moving on
        to temporal abstraction. The transform function is given a dataset as a parameter,
        and it returns a transformed dataset.
    """

    @abstractmethod
    def transform(self, df):
        """
        :param df: Dataframe, a time-point series
        :return: Dataframe, a time-point Series
        """
