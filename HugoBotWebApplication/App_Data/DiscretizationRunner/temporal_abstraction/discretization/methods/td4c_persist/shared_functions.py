import numpy as np
import pandas as pd
from scipy.stats import entropy

from temporal_abstraction.discretization.discretization import Discretization
from temporal_abstraction.discretization.methods.equal_frequency import EqualFrequency
from temporal_abstraction.discretization.errors import DataTooDenseError
from temporal_abstraction.discretization.methods.td4c_persist.exceptions import NotEnoughCandidatesError
from temporal_abstraction.temporal_abstraction import TemporalAbstraction

"""
    A file containing shared functions between TD4C and Persist.
"""

CANDIDATE_NB_BINS = 100
NOT_ENOUGH_CANDIDATES_ERROR_MSG_FMT = 'number of generated candidates {} is lower than the number of chosen bins {}'


def candidate_selection(df, nb_bins, scoring_function):
    """
    An algorithm for choosing cutpoints from a bag of pre-determined cutpoints.
    The cutpoints are chosen according to a score given to each one by the scoring function parameter.
    In each iteration a single cut-point is chosen according to the cut-point with the maximum score.
    :param df:
    :param nb_bins:
    :param scoring_function:
        A function which takes a time-point series and a list of cutpoints and returns the score
        of the list of cutpoints for the given time-point series
    :return: chosen candidates, and list of scores
    """
    cutpoint_candidates = generate_candidate_cutpoints(df, CANDIDATE_NB_BINS)

    chosen_cutpoints = np.ndarray((0,))
    chosen_scores = np.ndarray((0,))
    for _ in range(1, nb_bins, 1):
        scores = np.full((len(cutpoint_candidates),), -1.0)
        for i, c in enumerate(cutpoint_candidates):
            suggested_cutpoints = list(np.sort(np.append(chosen_cutpoints, [c])))

            df = df.assign(Bin=TemporalAbstraction.discretize_to_bins(suggested_cutpoints, df.TemporalPropertyValue))
            scores[i] = scoring_function(df, suggested_cutpoints)
        # end of for

        if len(scores) == 0:
            continue

        chosen_candidate_idx = np.argmax(scores)
        chosen_cutpoints = np.append(chosen_cutpoints, [cutpoint_candidates[chosen_candidate_idx]])
        chosen_scores = np.append(chosen_scores, [scores[chosen_candidate_idx]])

        sorting = np.argsort(chosen_cutpoints)
        chosen_cutpoints = chosen_cutpoints[sorting]
        chosen_scores = chosen_scores[sorting]

        del cutpoint_candidates[chosen_candidate_idx]
    # end of for
    return list(chosen_cutpoints), list(chosen_scores)


def generate_candidate_cutpoints(prop_vals, nb_candidates):
    try:
        states, _ = EqualFrequency(nb_candidates).discretize_property(prop_vals)
        return list(Discretization.extract_cutpoints_from_states(states).values())[0]
        # return EqualFrequency(nb_candidates)._generate_cutpoints(prop_vals)
    except DataTooDenseError as e:
        raise NotEnoughCandidatesError(e)


def symmetric_kullback_leibler(p, q):
    if sum(p) == 0 or sum(q) == 0:
        return 0
    return 0.5 * (entropy(p, q) + entropy(q, p))
