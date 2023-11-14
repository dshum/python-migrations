import os
import click
from dotenv import load_dotenv

from utils import db

load_dotenv()


class Config(object):
    CONNECTION = os.getenv("CONNECTION", "prod")
    PREFIX = "LOCAL_" if CONNECTION == "local" else ""

    DB_NAME = os.getenv(PREFIX + "DB_NAME", "postgres")
    DB_USER = os.getenv(PREFIX + "DB_USER", "postgres")
    DB_PASSWORD = os.getenv(PREFIX + "DB_PASSWORD", "password")
    DB_HOST = os.getenv(PREFIX + "DB_HOST", "127.0.0.1")
    DB_PORT = os.getenv(PREFIX + "DB_PORT", "5432")

    BRANDS_DB_NAME = "brands"

    SSH_HOST = os.getenv("SSH_HOST")
    REMOTE_DB_HOST = os.getenv("REMOTE_DB_HOST")
    REMOTE_DB_PORT = os.getenv("REMOTE_DB_PORT")
    SSH_KEY = os.getenv("SSH_KEY")

    def db_args(self):
        return {
            "db_name": self.DB_NAME,
            "db_user": self.DB_USER,
            "db_password": self.DB_PASSWORD,
            "db_host": self.DB_HOST,
            "db_port": self.DB_PORT,
        }

    def brands_db_args(self):
        return {
            "db_name": self.BRANDS_DB_NAME,
            "db_user": self.DB_USER,
            "db_password": self.DB_PASSWORD,
            "db_host": self.DB_HOST,
            "db_port": self.DB_PORT,
        }

    def ssh_tunnel_args(self):
        return {
            "ssh_host": self.SSH_HOST,
            "remote_db_host": self.REMOTE_DB_HOST,
            "remote_db_port": self.REMOTE_DB_PORT,
            "ssh_key": self.SSH_KEY
        }


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
