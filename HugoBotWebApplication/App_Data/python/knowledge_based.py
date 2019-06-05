import click

from discretization.discretization import Discretization
from discretize import create_files_per_class, get_methods_names
from files_manager.files_manager import FilesManager
from preprocessing.gradient import Gradient
from preprocessing.paa import paa
from time_intervals_adapter.time_intervals_adapter import time_intervals_to_string, create_time_intervals


@click.command()
@click.option(
    '--output-path',
    '-o',
    help='a full path of a directory into which all the output files will be saved',
    type=click.Path(exists=True, file_okay=False),
    default=None,
    show_default=True
)
@click.option(
    '--dataset-path',
    '-i',
    help='a full path to a dataset file',
    type=click.Path(exists=True),
    default=None,
    show_default=True
)
@click.option(
    '--gradient-window-size',
    '-gw',
    help='Gradient window size',
    type=int,
    default=None,
    show_default=True
)
@click.option(
    '--paa-window-size',
    '-pw',
    help='PAA window size',
    type=int,
    default=1,
    show_default=True
)
@click.option(
    '--max-gap',
    '-g',
    help='Maximum interpolation gap between two points in a time interval',
    type=int,
    default=1,
    show_default=True
)
@click.argument(
    'dataset-name',
    type=str
)
@click.argument(
    'nb-bins',
    type=int
)
@click.argument(
    'states-file-path',
    type=click.Path(exists=True)
)
def knowledge_based(dataset_name, nb_bins, states_file_path, paa_window_size,
                    max_gap, gradient_window_size, dataset_path, output_path):
    method = 'knowledge-based'

    print(f"""Parameters:
    dataset_path:       {dataset_path}
    output_path:        {output_path}
    dataset_name:       {dataset_name}
    nb_bins:            {nb_bins}
    method_name:        {method}
    paa_window_size:    {paa_window_size}
    max_gap:            {max_gap}
        """)

    files_manager = FilesManager(
        dataset_name,
        method,
        nb_bins,
        paa_window_size=paa_window_size,
        max_gap=max_gap,
        gradient_window_size=gradient_window_size,
        dataset_path=dataset_path,
        output_path=output_path,
    )

    states = files_manager.read_states_file(states_file_path)

    files_manager.create_states_file(states)

    cutpoints = Discretization.extract_cutpoints_from_states(states)

    dataset = files_manager.read_dataset()
    entity_class_relations = files_manager.read_entity_class_relations()

    dataset = paa(dataset, paa_window_size)
    if gradient_window_size is not None:
        grad = Gradient()
        dataset = grad.transform(dataset, window_size=gradient_window_size)

    dataset = Discretization.discretize_df_knowledge_based(cutpoints, dataset)

    entities_to_time_intervals = create_time_intervals(dataset, states, max_gap)
    time_intervals_str = time_intervals_to_string(entities_to_time_intervals)
    files_manager.create_time_intervals_file(time_intervals_str)

    create_files_per_class(files_manager, dataset, states, max_gap, entity_class_relations)

    return
