import numpy as np
import pandas as pd
from scipy.stats import entropy

from discretization.discretization import Discretization
from discretization.equal_width import EqualWidth
from discretization.errors import DataTooDenseError
from discretization.td4c_persist.exceptions import NotEnoughCandidatesError

CANDIDATE_NB_BINS = 100
NOT_ENOUGH_CANDIDATES_ERROR_MSG_FMT = 'number of generated candidates {} is lower than the number of chosen bins {}'


def candidate_selection(df: pd.DataFrame, nb_bins, scoring_function):
    cutpoint_candidates = generate_candidate_cutpoints(df, CANDIDATE_NB_BINS)

    chosen_cutpoints = np.ndarray((0,))
    chosen_scores = np.ndarray((0,))
    for _ in range(1, nb_bins, 1):
        scores = np.full((len(cutpoint_candidates),), -1.0)
        for i, c in enumerate(cutpoint_candidates):
            suggested_cutpoints = list(np.sort(np.append(chosen_cutpoints, [c])))

            df = df.assign(Bin=Discretization.discretize_prop(suggested_cutpoints, df.TemporalPropertyValue))
            scores[i] = scoring_function(df, suggested_cutpoints)
        # end of for

        if len(scores) == 0:  # TODO: Kfir added this, need to check that it doesn't screw up anything
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
        # return EqualFrequency().generate_cutpoints(prop_vals, nb_candidates)
        return EqualWidth().generate_cutpoints(prop_vals, nb_candidates)
    except DataTooDenseError as e:
        raise NotEnoughCandidatesError(e)


def symmetric_kullback_leibler(p, q):
    if sum(p) == 0 or sum(q) == 0:
        # TODO: should return 0 or something else?
        return 0
    return 0.5 * (entropy(p, q) + entropy(q, p))
