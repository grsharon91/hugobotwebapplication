from abc import ABC, abstractmethod
from math import inf

import pandas as pd

from constants import DatasetColumns, StatesColumns
from utils.dataframes_generator import DataframesGenerator


class TemporalAbstraction(ABC):

    @staticmethod
    @abstractmethod
    def discretize_property(prop_df):
        """ this is an abstract method """

    @staticmethod
    def discretize_to_bins(cutpoints, values):
        """
        making the values given as parameter discrete according to the cutpoints given
        :param cutpoints: List, a list of cutpoints to discretize by
        :param values: List, a list of values to discretize
        :return: List, a list of discrete values
        """
        bins = [-inf] + cutpoints + [inf]
        discrete_values = pd.cut(values, bins=bins, labels=False)
        return discrete_values

    @staticmethod
    def create_symbolic_time_series(states, time_point_series):
        """
        Creates a symbolic time series from a given states dataframe and a time point series
        :param states: Dataframe, a states dataframe
        :param time_point_series: Dataframe, a time point series
        :return:
            Dataframe, a symbolic time series so that each TemporalPropertyValue was replaced with
            its corresponding StateID
        """
        if states.empty or time_point_series.empty:
            return DataframesGenerator.generate_empty_symbolic_time_series()

        dataset_df = time_point_series.copy()

        cutpoints = TemporalAbstraction.extract_cutpoints_from_states(states)

        for prop_id, cutoffs in cutpoints.items():
            df_prop_idx = (dataset_df.TemporalPropertyID == prop_id)
            dataset_df.loc[df_prop_idx, StatesColumns.BinID] = \
                TemporalAbstraction.discretize_to_bins(cutpoints[prop_id],
                                                       dataset_df[df_prop_idx].TemporalPropertyValue)

        symbolic_time_series = dataset_df.drop(DatasetColumns.TemporalPropertyValue, axis='columns')

        symbolic_time_series = symbolic_time_series.join(
            states[[StatesColumns.StateID,
                    StatesColumns.TemporalPropertyID,
                    StatesColumns.BinID]].set_index([StatesColumns.TemporalPropertyID, StatesColumns.BinID]),
            how='left',
            on=[StatesColumns.TemporalPropertyID, StatesColumns.BinID]
        )

        return symbolic_time_series.drop(StatesColumns.BinID, axis='columns')

    @staticmethod
    def extract_cutpoints_from_states(states):
        """
        Extracts a list of cutpoints from the states dataframe for each property
        :param states: Dataframe, a dataframe containing states
        :return: Dict, a dictionary mapping each property-id to its list of cutpoints
        """
        cutpoints = {}

        for prop_id, prop_df in states.groupby(by=DatasetColumns.TemporalPropertyID):
            cutpoints[prop_id] = list(prop_df.BinHigh[:-1])

        return cutpoints

