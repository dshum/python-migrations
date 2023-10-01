import traceback

import click

from init import CommandCLI, Migration
from utils.style import console


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
        console.print("Done", style="success")
    except Exception:
        console.print_exception(show_locals=True)
