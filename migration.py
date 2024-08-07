import functools
import os

import click
from click import Command

from context import pass_context
from utils import db
from utils.style import console


class MigrationCLI(click.MultiCommand):
    commands_folder = os.path.join(os.path.dirname(__file__), "migrations")

    @staticmethod
    @pass_context
    def cli(context, name, queries):
        db_args = context.config.db_args()
        queries.append(db.migration_query(name))

        for database in context.databases:
            try:
                console.print(database, style="info")
                conn = db.get_db_connection(context.config, database)
                for query in queries:
                    db.execute_query(conn, query)
            except Exception as e:
                console.print(e, style="error")
                # console.print_exception(show_locals=True)

    def list_commands(self, ctx):
        rv = []
        for filename in os.listdir(self.commands_folder):
            if filename.endswith(".py") and filename != "__init__.py":
                rv.append(filename[:-3])
        rv.sort()
        return rv

    def get_command(self, ctx, name):
        ns = {}
        fn = os.path.join(self.commands_folder, name + ".py")
        with open(fn) as f:
            code = compile(f.read(), fn, "exec")
            eval(code, ns, ns)
        queries = ns["queries"]
        command = Command(
            name=name,
            callback=functools.partial(self.cli, name=name, queries=queries)
        )
        return command
