import itertools
from abc import abstractmethod

import numpy as np
import pandas as pd
from scipy.stats import entropy

from discretization.supervised import Supervised
from discretization.td4c_persist.shared_functions import symmetric_kullback_leibler, candidate_selection


class TD4C(Supervised):
    def generate_cutpoints_supervised(self, prop_df, nb_bins, class_relations):
        prop_df = prop_df.merge(class_relations, on='EntityID')
        return candidate_selection(
            prop_df,
            nb_bins,
            lambda df, cutoffs: self.__DDM_scoring_function(df, cutoffs)
        )

    def __DDM_scoring_function(self, df, cutoffs):
        class_mapping = {id: ind for id, ind in zip(df.ClassID.unique(),
                                                    itertools.count())}
        nb_classes = len(class_mapping)

        df['ClassID'] = df['ClassID'].map(class_mapping)

        class_distribs = np.zeros((nb_classes, len(cutoffs) + 1))
        for class_id, class_df in df.groupby('ClassID'):
            # if there are several entries with the same EntityID and ClassID
            # it will cause problems because they will be counted more than once
            freq = class_df.Bin.value_counts()
            class_distribs[class_id, freq.index.astype(np.int)] = freq.values / class_df.Bin.size  # every entry is worth 1, so the sum of the item frequencies is the same as the number of entries

        score = 0
        for i in range(nb_classes):
            for j in range(i + 1, nb_classes, 1):
                score += self._distance_measure(class_distribs[i], class_distribs[j])
        return score

    @abstractmethod
    def _distance_measure(self, p, q):
        pass


class TD4CKullbackLeibler(TD4C):
    def _distance_measure(self, p, q):
        return symmetric_kullback_leibler(p, q)


class TD4CEntropy(TD4C):
    def _distance_measure(self, p, q):
        return abs(entropy(p) - entropy(q))


class TD4CCosine(TD4C):
    def _distance_measure(self, p, q):
        return np.dot(p, q) / np.sqrt(p.dot(p) * q.dot(q))
