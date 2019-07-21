from abc import abstractmethod
from math import inf, nan

import numpy as np

from constants import DatasetColumns
from temporal_abstraction.temporal_abstraction import TemporalAbstraction
from utils.dataframes_generator import DataframesGenerator


class Discretization(TemporalAbstraction):
    """
        Super class for all the discretization methods
    """
    def __init__(self, nb_bins):
        self._nb_bins = nb_bins

    @abstractmethod
    def _generate_cutpoints(self, prop_df):
        """ this is an abstract method """

    def discretize_property(self, prop_df):
        """
        A template method in which the only change between algorithms is the _generate_cutpoints method
        which is common to all child classes.
        Each discretization method creates cutpoints in a different way
        :param prop_df: Dataframe, A time-point series of a single property
        :return: Tuple, (Dataframe , Dataframe) - states, , and the symbolic-point-series created from prop_df
        """
        if prop_df.empty:
            return DataframesGenerator.generate_empty_states(), DataframesGenerator.generate_empty_symbolic_time_series()

        cutpoints = self._generate_cutpoints(prop_df)

        # in case it is td4c or persist, they also return a list of bins scores
        if len(cutpoints) == 2 and type(cutpoints[0]) is list:
            cutpoints, scores = cutpoints
        else:
            scores = np.full(len(cutpoints), nan)

        states = Discretization.create_prop_states(prop_df[DatasetColumns.TemporalPropertyID].values[0],
                                                   cutpoints, scores)
        symbolic_point_series = TemporalAbstraction.create_symbolic_time_series(states, prop_df)

        return states, symbolic_point_series

    @staticmethod
    def create_prop_states(prop_id, cutpoints, scores=None):
        """
        Creates a states dataframe for a single property, containing the cutpoints and scores given as parameter
        :param prop_id: int, the property id
        :param cutpoints: List, a list of cutpoints
        :param scores: List, a list of scores, one for each cut-point
        :return: Dataframe, a states dataframe
        """
        nb_states = len(cutpoints) + 1
        bin_low = [-inf] + cutpoints
        bin_high = cutpoints + [inf]

        if scores is None:
            scores = np.full(nb_states - 1, np.nan)

        states = DataframesGenerator.generate_states(
            np.arange(1, nb_states + 1),
            np.full(nb_states, prop_id),
            np.arange(nb_states),
            bin_low,
            bin_high,
            np.append([nan], scores)
        )
        return states
