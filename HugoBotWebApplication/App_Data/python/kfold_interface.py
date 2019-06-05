import click

from discretize import get_methods_names
from kfold.kfold import KFoldTest


@click.command()
@click.option(
    '--paa-window-size',
    '-w',
    help='PAA window size',
    default=1,
    show_default=True
)
@click.option(
    '--max-gap',
    '-g',
    help='Maximum interpolation gap between two points in a time interval',
    default=1,
    show_default=True
)
@click.argument(
    'dataset-name',
    type=str
)
@click.argument(
    'nb-folds',
    type=int
)
@click.argument(
    'method',
    type=click.Choice(get_methods_names())
)
@click.argument(
    'nb-bins',
    type=int
)
def kfold(dataset_name, nb_folds, method, nb_bins, paa_window_size, max_gap):
    kf = KFoldTest(nb_folds, dataset_name, method, nb_bins, paa_window_size, max_gap)
    kf.divide_dataset()
    kf.discretize_folds()
