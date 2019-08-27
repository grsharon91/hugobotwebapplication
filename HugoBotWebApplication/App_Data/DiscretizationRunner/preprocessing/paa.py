import numpy as np
import pandas as pd

from constants import DatasetColumns
from preprocessing.transformation import Transformation


class PAA(Transformation):
    """
        Given a dataset, performs Piecewise Aggregate Approximation, which is a method of lowering
        the resolution of the data in addition to reduce noise in it.
        The PAA is performed for each entity and for each property. The values in each window are accumulated,
        and the mean is calculated. Afterwards, all the accumulated values are discarded from the dataset,
        and a new row is placed at the **beginning** of the window with the mean value
    """

    def __init__(self, window_size=1):
        """
        :param window_size: int
        """
        self.paa_window_size = window_size

    def transform(self, df):
        return PAA.paa(df, self.paa_window_size)

    @staticmethod
    def paa(df, window_size):
        """
        :param df: Dataframe
        :param window_size: int, the PAA window size
        :return: Dataframe, the df after PAA
        """
        if window_size < 1:
            raise Exception('ERROR: Invalid window size parameter')
        elif window_size == 1:  # it is meaningless to perform PAA with window size of 1
            return df
        elif df.empty:
            return df

        # each row's timestamp value is assigned to a bin representing the window to which it belongs
        df[DatasetColumns.TimeStamp] = \
            pd.cut(df[DatasetColumns.TimeStamp],
                   bins=np.arange(0, df[DatasetColumns.TimeStamp].max() + window_size + 1,
                                  step=window_size), include_lowest=True, right=False)

        # each timestamp value is assigned the window's start time (left)
        # the condition of >= 0 is because the values of the windows when including lowest are floats
        # close to the int values - for example the first window is (-0.00000001, window_size), so it needs conversion
        # to an int
        df[DatasetColumns.TimeStamp] = df[DatasetColumns.TimeStamp].apply(lambda x:
                                                                          x.left if x.left >= 0 else 0).astype('float')

        # now all the original timestamps of the same window has the same value (the window's start time),
        # so a group-by is performed and then a mean is applied
        df = df.groupby(
            by=[DatasetColumns.EntityID, DatasetColumns.TemporalPropertyID, DatasetColumns.TimeStamp]).apply(
            lambda x: x[DatasetColumns.TemporalPropertyValue].mean()
        ).reset_index()

        # re-arranging columns order
        df.columns = [
            DatasetColumns.EntityID,
            DatasetColumns.TemporalPropertyID,
            DatasetColumns.TimeStamp,
            DatasetColumns.TemporalPropertyValue
        ]

        return df
