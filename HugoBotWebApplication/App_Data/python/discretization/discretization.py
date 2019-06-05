from functools import reduce
import pandas as pd
from abc import ABC, abstractmethod
from math import inf
import numpy as np
from tqdm import tqdm


class Discretization(ABC):

    @abstractmethod
    def generate_cutpoints(self, prop_df, nb_bins, *args, **kwargs):
        pass

    @staticmethod
    def discretize_prop(cutpoints, prop_raw_data):
        bins = [-inf] + cutpoints + [inf]
        discrete_values = pd.cut(prop_raw_data, bins=bins, labels=False)
        return discrete_values

    def discretize_dataset(self, dataset, nb_bins, entity_class_relations, use_dask=False):
        tqdm.pandas()
        print('performing discretization...')
        if use_dask:
            cutpoints = dataset.groupby(by='TemporalPropertyID'). \
                apply(lambda prop_df:
                      self.generate_cutpoints(prop_df,
                                              nb_bins,
                                              class_relations=entity_class_relations),
                      meta=list).compute()
            dataset = dataset.compute()
        else:
            cutpoints = dataset.groupby(by='TemporalPropertyID'). \
                progress_apply(lambda prop_df:
                               self.generate_cutpoints(prop_df,
                                                       nb_bins,
                                                       class_relations=entity_class_relations))

        # in case it is td4c or persist, they also return a list of bins scores
        scores = cutpoints.apply(lambda x: x[1] if type(x) is tuple else None)
        scores = None if pd.isnull(scores).any() else scores.to_dict()

        cutpoints = cutpoints.apply(lambda x: x[0] if type(x) is tuple else x)
        cutpoints = cutpoints.to_dict()

        discretized_df = Discretization.discretize_df_knowledge_based(cutpoints, dataset)

        return Discretization.create_states(cutpoints, scores), discretized_df

    @staticmethod
    def create_states(cutpoints, scores=None):
        nb_states = reduce(lambda acc, new: acc + len(cutpoints[new]) + 1, [*cutpoints], 0)
        bin_low = reduce(lambda x, y: x + [-inf] + cutpoints[y], cutpoints.keys(), [])
        bin_high = reduce(lambda x, y: x + cutpoints[y] + [inf], cutpoints.keys(), [])

        states_file_values = {
            'StateID': np.arange(1, nb_states + 1, 1),
            'TemporalPropertyID': reduce(lambda acc, new: acc + [new] * (len(cutpoints[new]) + 1),
                                         cutpoints, []),
            'BinID': reduce(lambda acc, new: acc + [i for i in range(len(cutpoints[new]) + 1)],
                            cutpoints, []),
            'BinLow': bin_low,
            'BinHigh': bin_high
        }

        if scores is not None:
            states_file_values['BinLowScore'] = reduce(lambda x, y: x + ['None'] + scores[y], scores.keys(), [])

        states_df = pd.DataFrame.from_dict(states_file_values)
        return states_df

    @staticmethod
    def discretize_df_knowledge_based(cutpoints, df):
        dataset_df = df.copy()

        for prop_id, cutoffs in cutpoints.items():
            df_prop_idx = (dataset_df.TemporalPropertyID == prop_id)
            dataset_df.loc[df_prop_idx, 'BinID'] = \
                Discretization.discretize_prop(cutpoints[prop_id], dataset_df[df_prop_idx].TemporalPropertyValue)

        return dataset_df

    @staticmethod
    def extract_cutpoints_from_states(states):
        print('extracting cutpoints from states file...')
        cutpoints = {}

        for prop_id, prop_df in states.groupby(by='TemporalPropertyID'):
            cutpoints[prop_id] = list(prop_df.BinHigh[:-1])

        return cutpoints
