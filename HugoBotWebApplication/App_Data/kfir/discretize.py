import click

from discretization.equal_frequency import EqualFrequency
from discretization.equal_width import EqualWidth
from discretization.kmeans import KMeans
from discretization.sax import SAX
from discretization.td4c_persist.persist import Persist
from discretization.td4c_persist.td4c import TD4CKullbackLeibler, TD4CEntropy, TD4CCosine
from files_manager.files_manager import FilesManager
from preprocessing.gradient import Gradient
from preprocessing.paa import paa
from time_intervals_adapter.time_intervals_adapter import create_time_intervals, time_intervals_to_string, \
    create_classes_time_intervals

dispatch_dict = {
    'sax': SAX,
    'kmeans': KMeans,
    'equal-width': EqualWidth,
    'equal-frequency': EqualFrequency,
    'td4c-skl': TD4CKullbackLeibler,
    'td4c-entropy': TD4CEntropy,
    'td4c-cosine': TD4CCosine,
    'persist': Persist,
}


def create_discretization(method_name):
    if method_name not in dispatch_dict:
        raise Exception('ERROR: Invalid method name')
    return dispatch_dict[method_name]()


def get_methods_names():
    return list(dispatch_dict.keys())


def create_files_per_class(files_manager, dataset, states, max_gap, entity_class_relations):
    print('creating time-intervals file for each class...')
    classes_to_time_intervals = \
        create_classes_time_intervals(dataset,
                                      states,
                                      max_gap,
                                      entity_class_relations)
    for class_id in classes_to_time_intervals:
        class_intervals_str = time_intervals_to_string(
            classes_to_time_intervals[class_id]
        )
        files_manager.create_time_intervals_file(class_intervals_str, class_id)

    return


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
@click.option(
    '--use-dask',
    '-dask',
    help='A flag indicating whether to use dask for the discretization process or not',
    is_flag=True,
    show_default=True,
    default=False
)
@click.option(
    '--block-size',
    help='In case of using dask, determines the block-size for each partition when reading the dataset',
    type=int,
    default=None
)
@click.argument(
    'dataset-name',
    type=str
)
@click.argument(
    'method',
    type=click.Choice(get_methods_names())
)
@click.argument(
    'nb-bins',
    type=int
)
def discretize(dataset_name, method, nb_bins, paa_window_size, max_gap,
               gradient_window_size, use_dask, block_size, dataset_path, output_path):
    print(f"""Parameters:
    dataset_path:       {dataset_path}
    output_path:        {output_path}
    dataset_name:       {dataset_name}
    nb_bins:            {nb_bins}
    method_name:        {method}
    paa_window_size:    {paa_window_size}
    max_gap:            {max_gap}
    use_dask:           {use_dask}
    block_size:         {block_size}
        """)

    files_manager = FilesManager(
        dataset_name,
        method,
        nb_bins,
        paa_window_size=paa_window_size,
        max_gap=max_gap,
        block_size=block_size,
        use_dask=use_dask,
        dataset_path=dataset_path,
        output_path=output_path,
    )
    dataset = files_manager.read_dataset()
    entity_class_relations = files_manager.read_entity_class_relations()

    dataset = paa(dataset, paa_window_size)

    if gradient_window_size is not None:
        grad = Gradient()
        dataset = grad.transform(dataset, window_size=gradient_window_size)

    disc = create_discretization(method)
    states, dataset = disc.discretize_dataset(dataset, nb_bins, entity_class_relations, use_dask)
    # files_manager.create_discretized_file(dataset)
    files_manager.create_states_file(states)

    entities_to_time_intervals = create_time_intervals(dataset, states, max_gap)
    time_intervals_str = time_intervals_to_string(entities_to_time_intervals)
    files_manager.create_time_intervals_file(time_intervals_str)

    create_files_per_class(files_manager, dataset, states, max_gap, entity_class_relations)

    return
