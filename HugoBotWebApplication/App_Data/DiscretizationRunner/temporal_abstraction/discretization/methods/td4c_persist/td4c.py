import itertools
from abc import abstractmethod

import numpy as np
from scipy.stats import entropy

from constants import EntityClassRelationsColumns, DatasetColumns
from temporal_abstraction.discretization.supervised import Supervised
from temporal_abstraction.discretization.methods.td4c_persist.shared_functions import symmetric_kullback_leibler, \
    candidate_selection

"""
    Temporal Discretization for Classification
    discretization method
"""


class TD4C(Supervised):

    def _generate_cutpoints(self, prop_df):
        prop_df = prop_df.merge(self._entity_class_relations, on=DatasetColumns.EntityID)
        return candidate_selection(
            prop_df,
            self._nb_bins,
            lambda df, cutoffs: self.__DDM_scoring_function(df, cutoffs)
        )

    def __DDM_scoring_function(self, df, cutoffs):
        """
        A template method which uses the _distance_measure method to get the distance between 2
        distributions.
        :param df:
        :param cutoffs:
        :return:
        """
        # we re-map the classes to integers since classes could also be strings
        class_mapping = {id: ind for id, ind in zip(df[EntityClassRelationsColumns.ClassID].unique(),
                                                    itertools.count())}
        nb_classes = len(class_mapping)

        df[EntityClassRelationsColumns.ClassID] = df[EntityClassRelationsColumns.ClassID].map(class_mapping)

        class_distribs = np.zeros((nb_classes, len(cutoffs) + 1))
        for class_id, class_df in df.groupby(EntityClassRelationsColumns.ClassID):
            # if there are several entries with the same EntityID and ClassID
            # it will cause problems because they will be counted more than once
            freq = class_df.Bin.value_counts()
            class_distribs[class_id, freq.index.astype(
                np.int)] = freq.values / class_df.Bin.size  # every entry is worth 1, so the sum of the item frequencies is the same as the number of entries

        score = 0
        for i in range(nb_classes):
            for j in range(i + 1, nb_classes, 1):
                score += self._distance_measure(class_distribs[i], class_distribs[j])
        return score

    @abstractmethod
    def _distance_measure(self, p, q):
        """ This abstract method is shared between TD4C methods.
            Each subclass uses a different distance measure. """


class TD4CKullbackLeibler(TD4C):

    def _distance_measure(self, p, q):
        return symmetric_kullback_leibler(p, q)


class TD4CEntropy(TD4C):
    def _distance_measure(self, p, q):
        return abs(entropy(p) - entropy(q))


class TD4CCosine(TD4C):
    def _distance_measure(self, p, q):
        return np.dot(p, q) / np.sqrt(p.dot(p) * q.dot(q))
