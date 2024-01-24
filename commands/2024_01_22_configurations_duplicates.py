import os
import csv
import click

from context import pass_context
from utils import db
from utils.style import console


def find_duplicates(connection):
    query = (
        'select "group", "name", "value", count(id) from configurations '
        'group by "group", "name", "value" having count(id) > 1 '
        'order by "group", "name";'
    )
    duplicates = db.execute_read_query(connection, query)
    for duplicate in duplicates:
        console.print(duplicate[0], end=" ", style="yellow")
        console.out(duplicate[1], end=" ", style="green")
        if duplicate[2]:
            console.out(duplicate[2][0:25], end=" ", style="grey37")
        console.out(duplicate[3], end="\n", style="blue")


def clean_duplicates(connection):
    query = ('delete from configurations c1 using configurations c2 '
             'where c1."group" = c2."group" and c1."name" = c2."name" and c1."value" = c2."value" '
             'and c1.id > c2.id;')
    return db.execute_query(connection, query)


def create_index(connection):
    query = 'CREATE UNIQUE INDEX group_name_value_unique_idx ON configurations ("group", "name", MD5("value"));'
    return db.execute_query(connection, query)


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
            find_duplicates(conn)
            # result = clean_duplicates(conn)
            # result = create_index(conn)
            # console.print(result, end="\n\n")
        except Exception as e:
            console.print(e, style="error")
            # console.print_exception(show_locals=True)
