from math import nan, inf

import click
import numpy as np

from constants import DatasetColumns, get_discretization_methods_names
from system_flow import system_flow
from utils.dataframes_generator import DataframesGenerator


@click.group()
@click.option(
    '--paa-window-size',
    '-paa',
    type=int,
    default=1,
    show_default=True
)
@click.option(
    '--std-coef',
    '-std',
    type=int,
    default=2,
    show_default=True
)
@click.argument(
    'max-gap',
    type=int
)
def per_dataset(paa_window_size, std_coef, max_gap):
    ctx = click.get_current_context()
    properties = np.sort(ctx.meta['dataset'][DatasetColumns.TemporalPropertyID].unique())
    ctx.meta['properties'] = properties

    preprocessing_params_df = DataframesGenerator.generate_preprocessing_params(
        properties,
        np.full(len(properties), paa_window_size),
        np.full(len(properties), std_coef),
        np.full(len(properties), max_gap)
    )

    ctx.meta['preprocessing_params_df'] = preprocessing_params_df


class OptionRequiredIf(click.Option):

    def full_process_value(self, ctx, value):
        value = super(OptionRequiredIf, self).full_process_value(ctx, value)

        if value is None and ctx.params['states_path'] is None:
            msg = 'You need to either give a states file path or a states list'
            raise click.MissingParameter(ctx=ctx, param=self, message=msg)
        return value


@click.command()
@click.argument(
    'window-size',
    type=int
)
@click.option(
    '--states-path',
    '-sp',
    type=click.Path(exists=True),
    default=None
)
@click.option(
    '--states-list',
    '-sl',
    type=click.STRING,
    default=None,
    cls=OptionRequiredIf
)
def gradient(window_size, states_path, states_list):
    ctx = click.get_current_context()
    properties = ctx.meta['properties']

    if states_path:
        states = ctx.meta['files_manager'].read_csv(states_path)
    else:
        bins = [-inf] + [float(x) for x in states_list.split(' ')] + [inf]
        bins_lows_per_property = bins[:-1]
        bins_highs_per_property = bins[1:]

        bins_lows = np.tile(bins_lows_per_property, len(properties))
        bins_highs = np.tile(bins_highs_per_property, len(properties))

        states = DataframesGenerator.generate_states(
            np.arange(1, len(bins_lows) + 1),
            np.repeat(properties, len(bins_lows_per_property)),
            np.tile(np.arange(len(bins_lows_per_property)), len(properties)),
            bins_lows,
            bins_highs,
            np.full(len(bins_lows), np.nan)
        )

    params_df = DataframesGenerator.generate_temporal_abstraction_params(
        properties,
        ['gradient'] * len(properties),
        np.full(len(properties), nan),
        np.full(len(properties), window_size)
    )

    system_flow(ctx.meta['files_manager'],
                ctx.meta['preprocessing_params_df'],
                params_df,
                states,
                kfold=ctx.meta['kfold'])


@click.command()
@click.argument(
    'states-path',
    type=click.Path(exists=True)
)
def knowledge_based(states_path):
    ctx = click.get_current_context()
    properties = ctx.meta['properties']
    states = ctx.meta['files_manager'].read_csv(states_path)

    params_df = DataframesGenerator.generate_temporal_abstraction_params(
        properties,
        ['knowledge-based'] * len(properties),
        np.full(len(properties), nan),
        np.full(len(properties), nan),
    )

    system_flow(ctx.meta['files_manager'],
                ctx.meta['preprocessing_params_df'],
                params_df,
                states,
                kfold=ctx.meta['kfold'])


@click.command()
@click.argument(
    'method',
    type=click.Choice(get_discretization_methods_names())
)
@click.argument(
    'nb-bins',
    type=int
)
def discretization(method, nb_bins):
    ctx = click.get_current_context()
    properties = ctx.meta['properties']

    params_df = DataframesGenerator.generate_temporal_abstraction_params(
        properties,
        [method] * len(properties),
        np.full(len(properties), nb_bins),
        np.full(len(properties), nan)
    )

    system_flow(ctx.meta['files_manager'],
                ctx.meta['preprocessing_params_df'],
                params_df,
                kfold=ctx.meta['kfold'])


per_dataset.add_command(gradient)
per_dataset.add_command(knowledge_based)
per_dataset.add_command(discretization)
