import numpy as np

from constants import DatasetColumns
from preprocessing.transformation import Transformation


class OutliersRemover(Transformation):
    """
        Given a dataset, drops all rows which their TemporalPropertyValue is considered an "outlier".
        An outlier is determined by measuring the distance between the value and the mean. The std_coefficient
        is used to allow a certain amount of flexibility to the removal of rows
    """
    def __init__(self, std_coefficient=2):
        self.__std_coefficient = std_coefficient

    @staticmethod
    def remove_outliers(df, std_coefficient):
        """
        Given a dataframe, drops all rows so that: | row.TemporalPropertyValue - mean | > std * std_coefficient
        :param df: Dataframe, a dataframe
        :param std_coefficient: int, the coefficient of the std
        :return: Dataframe, a dataframe matching the given format, after all rows containing an outlier value have been dropped
        """
        mean = df[DatasetColumns.TemporalPropertyValue].mean()
        std = df[DatasetColumns.TemporalPropertyValue].std()

        if np.isnan(std):
            std = 0

        df = df[
            (mean - (std_coefficient * std) <= df[DatasetColumns.TemporalPropertyValue]) &
            (df[DatasetColumns.TemporalPropertyValue] <= mean + (std_coefficient * std))
        ]

        return df

    def transform(self, df):
        if df.empty:
            return df
        df = df.groupby(by=DatasetColumns.TemporalPropertyID). \
            apply(OutliersRemover.remove_outliers, std_coefficient=self.__std_coefficient).reset_index(drop=True)
        return df
