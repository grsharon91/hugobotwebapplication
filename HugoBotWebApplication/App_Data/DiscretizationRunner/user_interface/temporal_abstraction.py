import click

from files_manager.files_manager import FilesManager
from system_flow import system_flow
from user_interface.temporal_abstraction_per_dataset import per_dataset


@click.group()
@click.option(
    '--name',
    '-n',
    type=str,
    default=''
)
@click.option(
    '--kfold',
    '-kf',
    type=int,
    default=None
)
@click.argument(
    'input-path',
    type=click.Path(exists=True)
)
@click.argument(
    'output-path',
    type=click.Path(exists=True, file_okay=False)
)
def temporal_abstraction(input_path, output_path, kfold, name):
    ctx = click.get_current_context()

    files_manager = FilesManager(
        input_path,
        output_path,
        name
    )

    ctx.meta['files_manager'] = files_manager
    ctx.meta['dataset'] = files_manager.read_dataset()
    ctx.meta['kfold'] = kfold


@click.command()
@click.option(
    '--states-file',
    '-s',
    type=click.Path(exists=True)
)
@click.argument(
    'preprocessing-params-file',
    type=click.Path(exists=True)
)
@click.argument(
    'temporal-abstraction-params-file',
    type=click.Path(exists=True)
)
def per_property(preprocessing_params_file, temporal_abstraction_params_file, states_file):
    ctx = click.get_current_context()
    temporal_abstraction_params_df = FilesManager.read_csv(temporal_abstraction_params_file)
    preprocessing_params_df = FilesManager.read_csv(preprocessing_params_file)
    if states_file is not None:
        states = FilesManager.read_csv(states_file)
    else:
        states = None
    files_manager = ctx.meta['files_manager']

    system_flow(files_manager,
                preprocessing_params_df,
                temporal_abstraction_params_df,
                states)


temporal_abstraction.add_command(per_property)
temporal_abstraction.add_command(per_dataset)
