from itertools import count

import pandas as pd
import numpy as np
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
    states = df["StateID"].values

    sorted_idx = np.argsort(timestamps)
    timestamps, states = timestamps[sorted_idx], states[sorted_idx]
    possible_split_idx = np.arange(1, timestamps.shape[0])  # all indexes except for 0

    timestamp_diffs = (np.diff(timestamps) <= max_gap)
    state_diffs = (np.diff(states) == 0)

    split_idx = possible_split_idx[~(state_diffs & timestamp_diffs)]  # actual indexes for splitting

    frames, frames_states = np.split(timestamps, split_idx), np.split(states, split_idx)

    intervals = np.ndarray((len(frames), 3))
    for i, times, states in zip(count(), frames, frames_states):
        intervals[i, 0] = times[0]
        intervals[i, 1] = times[-1] + epsilon  # we first expand each timestamp and then connect between them
        intervals[i, 2] = states[0]

    return pd.DataFrame({'start': intervals[:, 0], 'end': intervals[:, 1], 'StateID': intervals[:, 2]})


def time_intervals_to_string(time_intervals_df):
    """
    convert the resulted time-intervals to a string matching the input format of KarmaLego
    :param entities_to_time_intervals:
    :return: string representation of the time intervals in KarmaLego format
    """
    print('parsing time-intervals...')

    intervals_str = time_intervals_df.groupby(by='EntityID'). \
        progress_apply(
        lambda entity_df: ';'.join(map(lambda x: ','.join(x.split()), entity_df.to_string(
            header=False,
            index=False,
            index_names=False,
            columns=['start',
                     'end',
                     'StateID',
                     'TemporalPropertyID']).split('\n')))
    )

    nb_entities = intervals_str.size

    entities_intervals = ''
    for entity_id, entity_intervals in intervals_str.iteritems():
        entities_intervals += '{};\n{};\n'.format(
            entity_id,
            entity_intervals
        )

    intervals_str = 'startToncepts\nnumberOfEntities,{}\n{}'.format(
        nb_entities,
        entities_intervals
    )

    return intervals_str


def create_time_intervals(dataset, states, max_gap):
    """
    convert the discretized dataset to time-intervals sorted by start-time, end-time, state-id
    :param dataset:
    :param states:
    :param max_gap:
    :param nb_class:
    :param entity_class_relations:
    :return:
    """

    print('creating time-intervals...')

    tqdm.pandas()
    time_intervals_df = dataset.drop("TemporalPropertyValue", axis='columns')

    time_intervals_df = time_intervals_df.join(
        states[['StateID',
                'TemporalPropertyID',
                'BinID']].set_index(['TemporalPropertyID', 'BinID']),
        how='left',
        on=['TemporalPropertyID', 'BinID']
    )

    time_intervals_df = time_intervals_df \
        .groupby(["TemporalPropertyID", "EntityID"]) \
        .progress_apply(lambda df: connect_timestamps(df, max_gap))
    time_intervals_df.sort_values(by=['start', 'end', 'StateID'], inplace=True)
    time_intervals_df.reset_index(inplace=True)
    time_intervals_df.drop('level_2', axis=1, inplace=True)

    time_intervals_df.start = time_intervals_df.start.apply(int)
    time_intervals_df.end = time_intervals_df.end.apply(int)
    time_intervals_df.StateID = time_intervals_df.StateID.apply(int)

    return time_intervals_df


def create_classes_time_intervals(dataset, states, max_gap, entity_class_relations):
    dataset_with_classes = dataset.merge(entity_class_relations,
                                         how='left',
                                         on='EntityID')

    intervals_by_class = dataset_with_classes.groupby(by='ClassID').apply(
        lambda class_df: create_time_intervals(class_df,
                                               states, max_gap)
    )

    time_intervals = {}

    for class_idx in entity_class_relations.ClassID.unique():
        class_intervals = intervals_by_class.loc[class_idx]
        time_intervals[class_idx] = class_intervals

    return time_intervals
