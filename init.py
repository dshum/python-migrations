import os

import click

from config import Config
from utils import db


class Migration(object):
    def __init__(self):
        self.config = Config()
        if self.config.CONNECTION == "prod":
            db.create_ssh_tunnel(**self.config.ssh_tunnel_args())

        self.connection = db.create_connection(**self.config.db_args())
        self.databases = db.get_databases(self.connection)

        brands_connection = db.create_connection(**self.config.brands_db_args())
        self.brands = db.get_brands(brands_connection)


class CommandCLI(click.MultiCommand):
    commands_folder = os.path.join(os.path.dirname(__file__), 'commands')

    def list_commands(self, ctx):
        rv = []
        for filename in os.listdir(self.commands_folder):
            if filename.endswith('.py') and filename != '__init__.py':
                rv.append(filename[:-3])
        rv.sort()
        return rv

    def get_command(self, ctx, name):
        ns = {}
        fn = os.path.join(self.commands_folder, name + '.py')
        with open(fn) as f:
            code = compile(f.read(), fn, 'exec')
            eval(code, ns, ns)
        return ns['cli']


pass_config = click.make_pass_decorator(Config)
pass_migration = click.make_pass_decorator(Migration)
command_cli = CommandCLI(help="This tool's subcommands are loaded from a plugin folder dynamically.")
