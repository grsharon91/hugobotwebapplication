import os

import click

from constants import StatesColumns, TimeIntervalsColumns
from files_manager.files_manager import FilesManager


@click.command()
@click.argument(
    'states-file1',
    type=click.Path(exists=True)
)
@click.argument(
    'time-intervals-file1',
    type=click.Path(exists=True)
)
@click.argument(
    'states-file2',
    type=click.Path(exists=True)
)
@click.argument(
    'time-intervals-file2',
    type=click.Path(exists=True)
)
@click.argument(
    'output-dir',
    type=click.Path(exists=True)
)
def results_union(states_file1, time_intervals_file1, states_file2, time_intervals_file2, output_dir):
    states_file1 = FilesManager.read_csv(states_file1)

    max_state1 = states_file1[StatesColumns.StateID].max()

    states_file2 = FilesManager.read_csv(states_file2)

    states_file2[StatesColumns.StateID] = states_file2[StatesColumns.StateID].apply(lambda x: x + max_state1)

    columns_order = [StatesColumns.StateID,
                     StatesColumns.TemporalPropertyID,
                     StatesColumns.BinID,
                     StatesColumns.BinLow,
                     StatesColumns.BinHigh]

    new_states = states_file1.append(states_file2, ignore_index=True, sort=False)

    if StatesColumns.BinLowScore in new_states.columns:
        columns_order.append(StatesColumns.BinLowScore)

    new_states = new_states[columns_order]
    new_states.to_csv(os.path.join(output_dir, 'states.csv'), index=False)

    time_intervals2 = FilesManager.parse_KL_to_time_intervals(FilesManager.read_file(time_intervals_file2))
    time_intervals2[TimeIntervalsColumns.StateID] = time_intervals2[TimeIntervalsColumns.StateID].apply(
        lambda x: int(x) + max_state1)

    time_intervals = \
        FilesManager.parse_KL_to_time_intervals(FilesManager.read_file(time_intervals_file1)).append(time_intervals2,
                                                                                                     ignore_index=True,
                                                                                                     sort=False)

    with open(os.path.join(output_dir, 'time_intervals.csv'), 'w') as f:
        f.write(FilesManager.parse_time_intervals_to_KL(time_intervals))
