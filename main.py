import click

from init import Config, CommandCLI, pass_config
from utils import db, colors


@click.group()
def cli():
    pass


class Migration(object):
    def __init__(self):
        self.config = Config()
        if self.config.CONNECTION == "prod":
            db.create_ssh_tunnel(**self.config.ssh_tunnel_args())

        self.connection = db.create_connection(**self.config.db_args())
        self.databases = db.get_databases(self.connection)


@cli.command(name="migrate", cls=CommandCLI)
@click.pass_context
def migrate(ctx):
    ctx.obj = Migration()


if __name__ == '__main__':
    try:
        cli()
    except Exception as e:
        colors.error(e)
