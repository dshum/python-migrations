import click

from command import CommandCLI
from config import Config
from utils import db


class Context(object):
    def __init__(self):
        self.config = Config()
        if self.config.CONNECTION == "prod":
            db.create_ssh_connection(**self.config.ssh_tunnel_args())

        self.connection = db.create_connection(**self.config.db_args())
        self.databases = db.get_databases(self.connection)

        brands_connection = db.create_connection(**self.config.brands_db_args())
        self.brands = db.get_brands(brands_connection)


pass_context = click.make_pass_decorator(Context)
