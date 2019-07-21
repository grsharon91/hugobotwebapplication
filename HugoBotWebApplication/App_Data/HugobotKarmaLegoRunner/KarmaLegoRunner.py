import click

from KarmaLego_Framework.RunKarmaLego import runKarmaLego
import os


@click.command()
@click.argument(
    'input-path',
    type=click.Path(exists=True)
)
@click.argument(
    'output-path',
    type=click.Path(exists=True, file_okay=False)
)
@click.argument(
    'epsilon',
    type=float
)
@click.argument(
    'min-vertical-support',
    type=float
)
@click.argument(
    'max-gap',
    type=int
)
def karma_lego_runner(input_path, epsilon, min_vertical_support, max_gap, output_path):
    lego, karma = runKarmaLego(input_path, min_vertical_support, 7, max_gap, 0, epsilon, output_path,
                               semicolon_end=True)
    lego.print_frequent_tirps(os.path.join(output_path, 'kl-result.txt'))


if __name__ == '__main__':
    karma_lego_runner()
