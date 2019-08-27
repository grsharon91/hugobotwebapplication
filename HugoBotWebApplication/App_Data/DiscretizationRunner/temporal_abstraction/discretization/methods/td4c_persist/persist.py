from collections import Counter
from math import inf

import numpy as np

from temporal_abstraction.discretization.methods.td4c_persist.shared_functions import symmetric_kullback_leibler, \
    candidate_selection
from temporal_abstraction.discretization.unsupervised import Unsupervised

"""
Persist Discretization
paper url: http://www.mybytes.de/papers/moerchen05optimizing.pdf
"""


class Persist(Unsupervised):
    """
        The private functions are implementation of the equations given in the Persist paper
    """

    def _generate_cutpoints(self, prop_df):
        return Persist.persist(prop_df, self._nb_bins)

    @staticmethod
    def persist(prop_values, nb_bins):
        def scoring_function(df, cutoffs):
            return Persist.__all_states_persistance(
                df.Bin.values,
                len(cutoffs) + 1  # = bins number for (old_cutoffs U {new_cutoff})
            )

        return candidate_selection(prop_values, nb_bins, scoring_function)

    @staticmethod
    def __all_states_persistance(discrete_vals, nb_bins):
        state_probs = Persist.__calc_state_probabilities(discrete_vals, nb_bins)
        marginal_probs = Persist.__calc_marginal_probabilities(discrete_vals, nb_bins)
        single_state_scores = [Persist.__single_state_persistence(i, state_probs, marginal_probs)
                               for i in range(nb_bins)]

        if inf in single_state_scores:
            return inf  # otherwise it will be 'nan'

        return np.mean([Persist.__single_state_persistence(i, state_probs, marginal_probs) for i in range(nb_bins)])

    @staticmethod
    def __single_state_persistence(bin_idx, state_probs, marginal_probs):
        m = marginal_probs[bin_idx, bin_idx]
        s = state_probs[bin_idx]
        return np.sign(m - s) * symmetric_kullback_leibler([m, 1 - m], [s, 1 - s])

    @staticmethod
    def __calc_state_probabilities(discrete_values, nb_bins):
        c = Counter(discrete_values)
        probs = np.array([c.get(bin_idx) if bin_idx in c else 0 for bin_idx in range(nb_bins)])
        probs = probs / discrete_values.shape[0]
        return probs

    @staticmethod
    def __calc_marginal_probabilities(discrete_values, nb_bins):
        marginal_probabilities = np.zeros((nb_bins, nb_bins))
        nb_transitions = discrete_values.shape[0] - 1

        for si, sj in zip(discrete_values, discrete_values[1:]):
            marginal_probabilities[si, sj] += 1

        marginal_probabilities = marginal_probabilities / nb_transitions
        return marginal_probabilities
