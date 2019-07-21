from constants import StatesColumns, DatasetColumns
from temporal_abstraction.temporal_abstraction import TemporalAbstraction
from utils.dataframes_generator import DataframesGenerator


class KnowledgeBased(TemporalAbstraction):
    """
        Handles knowledge-based temporal abstraction
    """
    def __init__(self, states):
        self.__states = states

    @staticmethod
    def knowledge_based(states, prop_df):
        """
        :param states: Dataframe
        :param prop_df: Dataframe
        :return:
        """
        return TemporalAbstraction.create_symbolic_time_series(states, prop_df)

    def discretize_property(self, prop_df):
        if prop_df.empty:
            return DataframesGenerator.generate_empty_states(), DataframesGenerator.generate_empty_symbolic_time_series()
        prop_id = prop_df[DatasetColumns.TemporalPropertyID].values[0]
        return self.__states[self.__states[StatesColumns.TemporalPropertyID] == prop_id], \
               KnowledgeBased.knowledge_based(self.__states, prop_df)
