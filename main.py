import traceback

import click

from init import CommandCLI, Migration
from utils import colors


@click.group()
def cli():
    pass


@cli.command(cls=CommandCLI)
@click.pass_context
def migrate(ctx):
    ctx.obj = Migration()


if __name__ == '__main__':
    try:
        cli()
    except Exception as e:
        colors.error(e)
        # traceback.print_exception(e)
