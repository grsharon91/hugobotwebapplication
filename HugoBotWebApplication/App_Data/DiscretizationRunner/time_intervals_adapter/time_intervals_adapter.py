from itertools import count

import numpy as np
import pandas as pd
from pandas._libs.parsers import is_float_dtype

from constants import DatasetColumns, StatesColumns, TimeIntervalsColumns
from utils.dataframes_generator import DataframesGenerator


class TimeIntervalsAdapter:
    """ Handles the connection of symbolic time points to intervals
        according to a max_gap parameter that is given to it """

    def __init__(self, max_gap):
        """
        :param max_gap: int, the maximum difference of two successor timestamps in the same interval
        """
        self.max_gap = max_gap

    def __connect_timestamps(self, df, minimum_duration=1):
        """
        There cannot be a different symbol of the same property between
        the symbols being connected:

        yes ----state:x propoid:y----<<<<<max-gap>>>>
                                                ---state:x propoid:y----
        no ----state:x propoid:y----<<<<<max-gap>>>>
                                                ---state:x propoid:y----
                                        --state:z propoid:y----


        :param df: Dataframe, a dataframe which contains entities, timestamps, and discretized-values
        :param minimum_duration: int, new length for zero time intervals
        :return: numpy array of shape (nb_intervals, 2) of start times and end times
        """
        e_max_gap = self.max_gap + minimum_duration
        timestamps = df[DatasetColumns.TimeStamp].values
        states = df[StatesColumns.StateID].values

        sorted_idx = np.argsort(timestamps)
        timestamps, states = timestamps[sorted_idx], states[sorted_idx]
        possible_split_idx = np.arange(1, timestamps.shape[0])  # all indexes except for 0

        timestamp_diffs = (np.diff(timestamps) <= e_max_gap)
        state_diffs = (np.diff(states) == 0)

        split_idx = possible_split_idx[~(state_diffs & timestamp_diffs)]  # actual indexes for splitting

        frames, frames_states = np.split(timestamps, split_idx), np.split(states, split_idx)

        intervals = np.ndarray((len(frames), 3))
        for i, times, states in zip(count(), frames, frames_states):
            intervals[i, 0] = times[0]
            intervals[i, 1] = times[-1] + minimum_duration  # we first expand each timestamp and then connect between them
            intervals[i, 2] = states[0]

        return pd.DataFrame({TimeIntervalsColumns.Start: intervals[:, 0], TimeIntervalsColumns.End: intervals[:, 1],
                             TimeIntervalsColumns.StateID: intervals[:, 2]})

    def create_time_intervals(self, symbolic_time_series):
        """
        convert the discretized dataset to time-intervals sorted by start-time, end-time, state-id
        :param symbolic_time_series: Dataframe
        :return: Dataframe, symbolic time intervals
        """

        if symbolic_time_series.empty:
            return DataframesGenerator.generate_empty_symbolic_time_intervals()

        time_intervals_df = symbolic_time_series \
            .groupby(by=[TimeIntervalsColumns.TemporalPropertyID, TimeIntervalsColumns.EntityID]) \
            .apply(lambda df: self.__connect_timestamps(df))

        time_intervals_df.sort_values(
            by=[TimeIntervalsColumns.Start, TimeIntervalsColumns.End, TimeIntervalsColumns.StateID],
            inplace=True)

        time_intervals_df.reset_index(inplace=True)
        time_intervals_df.drop('level_2', axis=1, inplace=True)

        time_intervals_df = time_intervals_df[[
            TimeIntervalsColumns.EntityID,
            TimeIntervalsColumns.TemporalPropertyID,
            TimeIntervalsColumns.StateID,
            TimeIntervalsColumns.Start,
            TimeIntervalsColumns.End
        ]]

        return time_intervals_df

    @staticmethod
    def set_columns_types(time_intervals_df):
        """
        set the columns types of a time intervals dataframe
        :param time_intervals_df: Dataframe
        :return: Dataframe
        """
        if is_float_dtype(time_intervals_df[TimeIntervalsColumns.EntityID]):
            time_intervals_df[TimeIntervalsColumns.EntityID] = \
                time_intervals_df[TimeIntervalsColumns.EntityID].apply(int)

        time_intervals_df[TimeIntervalsColumns.StateID] = time_intervals_df[TimeIntervalsColumns.StateID].apply(int)
        time_intervals_df[TimeIntervalsColumns.Start] = time_intervals_df[TimeIntervalsColumns.Start].apply(int)
        time_intervals_df[TimeIntervalsColumns.End] = time_intervals_df[TimeIntervalsColumns.End].apply(int)
        time_intervals_df[TimeIntervalsColumns.TemporalPropertyID] = time_intervals_df[
            TimeIntervalsColumns.TemporalPropertyID].apply(int)

        return time_intervals_df
