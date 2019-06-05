import click
from discretize import discretize
from knowledge_based import knowledge_based
from kfold_interface import kfold


@click.group()
def cli():
    pass


cli.add_command(discretize)
cli.add_command(knowledge_based)
cli.add_command(kfold)

if __name__ == '__main__':
    cli()
