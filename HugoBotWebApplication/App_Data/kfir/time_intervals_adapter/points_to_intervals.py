import numpy as np
import pandas as pd
from tqdm import tqdm


def connect_timestamps(df, max_gap, epsilon=1):
    """
    :param df: a dataframe which contains entities, timestamps, and discretized-values
    :param max_gap: maximum difference of two successor timestamps in the same interval
    :param epsilon: new length for zero time intervals
    :return: numpy array of shape (nb_intervals, 2) of start times and end times
    """
    max_gap += epsilon
    timestamps = df["TimeStamp"].values
    timestamps = np.sort(timestamps)
    timestamp_diffs = (np.diff(timestamps) <= max_gap)
    possible_split_idx = np.arange(1, timestamps.shape[0])  # all indexes except for 0
    split_idx = possible_split_idx[~timestamp_diffs]  # actual indexes for splitting
    frames = np.split(timestamps, split_idx)

    intervals = np.ndarray((len(frames), 2))
    for i, times in enumerate(frames):
        intervals[i, 0] = times[0]
        intervals[i, 1] = times[-1] if times[0] != times[-1] else times[0] + epsilon

    return pd.DataFrame({'start': intervals[:, 0], 'end': intervals[:, 1]})


def create_time_intervals(dataset, states, max_gap, nb_class='', entity_class_relations=None):
    tqdm.pandas()
    new_df = dataset.drop("TemporalPropertyValue", axis='columns')

    new_df = new_df.join(
        states[['StateID',
                'TemporalPropertyID',
                'BinID']].set_index(['TemporalPropertyID', 'BinID']),
        how='left',
        on=['TemporalPropertyID', 'BinID']
    )

    new_df = new_df \
        .groupby(["TemporalPropertyID", "StateID", "EntityID"]) \
        .progress_apply(lambda df: connect_timestamps(df, max_gap))
    new_df.sort_values(by=['start', 'end', 'StateID'], inplace=True)
    new_df.reset_index(inplace=True)
    new_df.drop('level_3', axis=1, inplace=True)

    return new_df
