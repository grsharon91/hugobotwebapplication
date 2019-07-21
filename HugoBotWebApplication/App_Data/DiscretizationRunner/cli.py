import click

from user_interface.results_union import results_union
from user_interface.temporal_abstraction import temporal_abstraction, per_property


@click.group()
def cli():
    pass


cli.add_command(temporal_abstraction)
cli.add_command(results_union)

if __name__ == '__main__':
    cli()
