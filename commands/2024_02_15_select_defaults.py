import os
import csv
import click

from context import pass_context
from utils import db
from utils.style import console


def select_defaults(connection):
    query = (
        'select id, "group", name, comment, created_at, updated_at from configurations '
        'where "group" = \'Defaults\''
        'order by "id";'
    )
    defaults = db.execute_read_query(connection, query)
    for row in defaults:
        for column in row:
            console.print(column, end=" ")
        console.print("")
    console.print("")


def update_defaults(connection):
    query = (
        'update configurations '
        'set created_at = date_trunc(\'second\', created_at), updated_at = date_trunc(\'second\', updated_at) '
        'where "group" = \'Defaults\';'
    )
    db.execute_query(connection, query)


@click.command()
@pass_context
def cli(context):
    os.system("clear")

    db_args = context.config.db_args()
    existed_db_names = []

    for name, hosts, db_name, fin_group in context.brands:
        try:
            console.print(f"{name}, {hosts}, {db_name}", style="info")
            conn = db.get_db_connection(context.config, db_name)
            select_defaults(conn)
            # update_defaults(conn)
        except Exception as e:
            console.print(e, style="error")
            # console.print_exception(show_locals=True)
