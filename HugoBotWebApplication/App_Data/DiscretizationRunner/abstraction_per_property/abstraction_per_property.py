from functools import reduce

import numpy as np
import pandas as pd

from constants import DatasetColumns, PreprocessingParamsColumns, TemporalAbstractionParamsColumns, StatesColumns, \
    SymbolicTimeSeriesColumns, get_supervised_methods_names, get_unsupervised_methods_names, MethodsNames
from preprocessing.outliers_remover import OutliersRemover
from preprocessing.paa import PAA
from temporal_abstraction.discretization.methods.equal_frequency import EqualFrequency
from temporal_abstraction.discretization.methods.equal_width import EqualWidth
from temporal_abstraction.discretization.methods.kmeans import KMeans
from temporal_abstraction.discretization.methods.sax import SAX
from temporal_abstraction.discretization.methods.td4c_persist.persist import Persist
from temporal_abstraction.discretization.methods.td4c_persist.td4c import TD4CKullbackLeibler, TD4CEntropy, TD4CCosine
from temporal_abstraction.gradient import Gradient
from temporal_abstraction.knowledge_based import KnowledgeBased
from time_intervals_adapter.time_intervals_adapter import TimeIntervalsAdapter
from utils.dataframes_generator import DataframesGenerator


class AbstractionPerProperty:

    def __init__(self, preprocessing_params_df, temporal_abstraction_params_df):
        self.__preprocessing_params_df = preprocessing_params_df
        self.__temporal_abstraction_params_df = temporal_abstraction_params_df

    def preprocessing_per_property(self, dataset):
        if dataset.empty:
            return dataset

        # for each row in params_df, it starts with the values of the given property in the dataset,
        # and then performs transform for each pre-processing requested in the params
        preprocessed_props = [
            reduce(lambda acc, new: new.transform(acc), AbstractionPerProperty.__generate_preprocessing_by_name(row[1]),
                   dataset[dataset[DatasetColumns.TemporalPropertyID] == row[1][
                       PreprocessingParamsColumns.TemporalPropertyID]])
            for row in self.__preprocessing_params_df.iterrows()]

        # after getting a list of the transformed parameters, concatenates them into a single dataframe
        return pd.concat(preprocessed_props, ignore_index=True)

    def temporal_abstraction_per_property(self, dataset, entity_class_relations=None,
                                          states=None):
        if dataset.empty:
            return DataframesGenerator.generate_empty_states(), DataframesGenerator.generate_empty_symbolic_time_series()

        symbolic_time_series = [AbstractionPerProperty.__generate_abstraction_by_name(row[1],
                                                                                      entity_class_relations,
                                                                                      states).discretize_property(
            dataset[
                dataset[DatasetColumns.TemporalPropertyID] == row[1][
                    TemporalAbstractionParamsColumns.TemporalPropertyID]])
            for row in self.__temporal_abstraction_params_df.iterrows()]

        """ It counts the number of states and accumulates them to re-index the StateID column """
        state_ids_ctr = reduce(lambda acc, new: acc + [acc[-1] + new[0].shape[0]],
                               symbolic_time_series,
                               [0])

        """ For each given states df, it re-indexes the StateID to start from the last max StateID + 1
            to avoid collisions between states ids """

        def reindex_states(tmp_states, states_ctr):
            return {
                StatesColumns.StateID: tmp_states[StatesColumns.StateID] + states_ctr - (
                        tmp_states[StatesColumns.StateID].min() - 1)
            }

        """ Just a map to update and re-assign the StateID column """
        symbolic_time_series = [(tmp_states.assign(**reindex_states(tmp_states, states_ctr)),
                                 sts.assign(**reindex_states(sts, states_ctr))) for ((tmp_states, sts), states_ctr) in
                                zip(symbolic_time_series, state_ids_ctr)]

        """ Concatenating the data-frames one after the other """
        combined_symbolic_time_series = pd.concat([p[1] for p in symbolic_time_series], ignore_index=True)
        combined_states = pd.concat([p[0] for p in symbolic_time_series], ignore_index=True)
        return combined_states, combined_symbolic_time_series

    def intervalization_per_property(self, symbolic_time_series):
        if symbolic_time_series.empty:
            return DataframesGenerator.generate_empty_symbolic_time_intervals()
        intervalized_props = [
            TimeIntervalsAdapter(row[1][PreprocessingParamsColumns.MaxGap]).create_time_intervals(
                symbolic_time_series[
                    symbolic_time_series[SymbolicTimeSeriesColumns.TemporalPropertyID] ==
                    row[1][PreprocessingParamsColumns.TemporalPropertyID]
                    ]
            )
            for row in self.__preprocessing_params_df.iterrows()]

        return pd.concat(intervalized_props, ignore_index=True)

    @staticmethod
    def __generate_preprocessing_by_name(params_row):
        """
        given a single row of parameters, returns the instances of the pre-processing classes
        that are relevant to the parameters
        :param params_row: Dataframe, a single row of pre-processing parameters (according to the pre-processing parameters file format
        :return: List, a list containing the pre-processing objects to run
        """
        res = []
        if not np.isnan(params_row[PreprocessingParamsColumns.PAAWindowSize]):
            res.append(PAA(params_row[PreprocessingParamsColumns.PAAWindowSize]))
        if not np.isnan(params_row[PreprocessingParamsColumns.StdCoef]):
            res.append(OutliersRemover(params_row[PreprocessingParamsColumns.StdCoef]))

        return res

    @staticmethod
    def __generate_abstraction_by_name(params_row, entity_class_relations=None, states=None):
        """
        :param params_row: pd.Series, a row of parameters from the temporal_abstraction_params_df
        :param entity_class_relations: Dataframe
        :param states: Dataframe
        :return: a TemporalAbstraction object
        """
        supervised_methods = get_supervised_methods_names()

        unsupervised_methods = get_unsupervised_methods_names()

        name = params_row[TemporalAbstractionParamsColumns.Method]

        if name in supervised_methods:
            get_params = lambda params: \
                [int(params[TemporalAbstractionParamsColumns.NbBins]), entity_class_relations]
        elif name in unsupervised_methods:
            get_params = lambda params: \
                [int(params[TemporalAbstractionParamsColumns.NbBins])]
        elif name == MethodsNames.KnowledgeBased:
            get_params = lambda params: \
                [states]
        elif name == MethodsNames.Gradient:
            get_params = lambda params: \
                [int(params[TemporalAbstractionParamsColumns.GradientWindowSize]), states]
        else:
            raise Exception(f'ERROR: Invalid abstraction name "{name}"')

        dispatch = {
            MethodsNames.EqualWidth: EqualWidth,
            MethodsNames.EqualFrequency: EqualFrequency,
            MethodsNames.SAX: SAX,
            MethodsNames.KMeans: KMeans,
            MethodsNames.Persist: Persist,
            MethodsNames.TD4CCosine: TD4CCosine,
            MethodsNames.TD4CEntropy: TD4CEntropy,
            MethodsNames.TD4CKullbackLeibler: TD4CKullbackLeibler,
            MethodsNames.Gradient: Gradient,
            MethodsNames.KnowledgeBased: KnowledgeBased
        }

        return dispatch[name](*get_params(params_row))
