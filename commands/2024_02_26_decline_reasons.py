import os
import csv
import click

from context import pass_context
from utils import db
from utils.style import console


def add_decline_reasons(connection):
    query = '''
    SELECT setval('configurations_id_seq', COALESCE((SELECT MAX(id) + 1 FROM configurations), 1), false);
    '''
    db.execute_query(connection, query)

    for name in ("Expired document", "Insufficient documents", "Name mismatch", "Black and white"):
        query = f'''
        INSERT INTO "public"."configurations" 
        ("group", "name", "type", "value", "comment", "created_at", "updated_at", "meta") 
        VALUES (\'Decline reasons\', \'Decline Reason\', \'text\', \'{name}\', \'Decline Reason that seeded\', 
        \'2024-02-26 18:35:00\', \'2024-02-26 18:35:00\', NULL);
        '''
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
            add_decline_reasons(conn)
        except Exception as e:
            console.print(e, style="error")
            # console.print_exception(show_locals=True)
