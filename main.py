import traceback

import click

from command import CommandCLI
from context import pass_context, Context
from migration import MigrationCLI
from utils.style import console


@click.group()
def cli():
    pass


@cli.command(cls=MigrationCLI)
@click.pass_context
def migrate(ctx):
    ctx.obj = Context()


@cli.command(cls=CommandCLI)
@click.pass_context
def run(ctx):
    ctx.obj = Context()


if __name__ == '__main__':
    try:
        cli()
        console.print("Done", style="success")
    except Exception:
        console.print_exception(show_locals=True)
