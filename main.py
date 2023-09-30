import click

from init import Config, CommandCLI, pass_config
from utils import db, colors


@click.group()
@click.pass_context
def cli(ctx):
    ctx.ensure_object(dict)
    ctx.obj["config"] = Config()


class Migration(object):
    def __init__(self, config):
        if config.CONNECTION == "prod":
            db.create_ssh_tunnel(**config.ssh_tunnel_args())

        self.config = config
        self.connection = db.create_connection(**self.config.db_args())
        self.databases = db.get_databases(self.connection)


@cli.command(name="migrate", cls=CommandCLI)
@click.pass_context
def migrate(ctx):
    ctx.obj["migration"] = Migration(ctx.obj["config"])


if __name__ == '__main__':
    try:
        cli()
    except Exception as e:
        colors.error(e)
