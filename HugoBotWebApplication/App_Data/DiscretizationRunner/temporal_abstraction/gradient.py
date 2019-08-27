import numpy as np

from constants import DatasetColumns, StatesColumns
from temporal_abstraction.temporal_abstraction import TemporalAbstraction
from utils.dataframes_generator import DataframesGenerator


class Gradient(TemporalAbstraction):
    """ In charge of performing the gradient temporal abstraction.
        It takes each sample in the dataset, and calculates its slope
        using linear regression, using the points that are in the window before it.
        The window size can be determined with the window_size parameter.
        Once the slope is calculated, the angel is calculated according to arctan(slope),
        and the value is placed instead of the original sample.
        It uses angels as means of normalization of the data.

        Note: If no samples are found in the window of a sample, the sample is discarded from the data."""

    def __init__(self, window_size, states):
        """
        :param window_size: int
        :param states: Dataframe
        """
        self.__window_size = window_size
        self.__states = states

    @staticmethod
    def derivative(df, gradient_window_size):
        """
        Calculates the derivative for each sample in df according to the window size
        :param df: Dataframe, containing values of a single property
        :param gradient_window_size: int, the size of the gradient window
        :return: Dataframe, containing the derivatives of each sample instead of the original values
        """
        df.sort_values(by=DatasetColumns.TimeStamp)

        def calc_derivative_of_sample(sample):
            samples_in_window = df[
                (df[DatasetColumns.TimeStamp] <= sample[DatasetColumns.TimeStamp]) &
                (df[DatasetColumns.TimeStamp] >= sample[DatasetColumns.TimeStamp] - gradient_window_size)
                ]

            y = samples_in_window[DatasetColumns.TemporalPropertyValue].values
            x = samples_in_window[DatasetColumns.TimeStamp].values
            nb_points = np.size(y)

            mean_x, mean_y = np.mean(x), np.mean(y)

            ss_xy = np.sum(x * y) - mean_x * sum(y) - mean_y * sum(x) + nb_points * mean_x * mean_y
            ss_xx = np.sum(x * x) - 2 * mean_x * np.sum(x) + nb_points * mean_x * mean_x

            if ss_xx != 0:
                b_1 = ss_xy / ss_xx
                return np.degrees(np.arctan(b_1))
            else:
                return

        df[DatasetColumns.TemporalPropertyValue] = df.apply(calc_derivative_of_sample, axis=1)
        return df

    @staticmethod
    def gradient(df, window_size, states):
        """
        :param df: Dataframe, a time-point series
        :param window_size: int
        :param states: Dataframe, contains the states the gradient uses
        :return: Dataframe, a symbolic time series
        """
        time_point_series = df.groupby(by=[DatasetColumns.EntityID, DatasetColumns.TemporalPropertyID]). \
            apply(lambda x: Gradient.derivative(x, window_size)).dropna()

        symbolic_time_series = TemporalAbstraction.create_symbolic_time_series(states, time_point_series)
        return symbolic_time_series

    def discretize_property(self, prop_df):
        if prop_df.empty:
            return self.__states,\
                   DataframesGenerator.generate_empty_symbolic_time_series()

        prop_id = prop_df[DatasetColumns.TemporalPropertyID].values[0]
        return self.__states[self.__states[StatesColumns.TemporalPropertyID] == prop_id], \
               Gradient.gradient(prop_df,
                                 self.__window_size,
                                 self.__states)
