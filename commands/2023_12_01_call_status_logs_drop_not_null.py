import click

from init import pass_migration
from utils import db
from utils.style import console


def run_migration(connection):
    query = "ALTER TABLE call_status_logs ALTER COLUMN start_talking_at DROP NOT NULL;"
    db.execute_query(connection, query)
    query = "ALTER TABLE call_status_logs ALTER COLUMN end_talking_at DROP NOT NULL;"
    db.execute_query(connection, query)


@click.command()
@pass_migration
def cli(migration):
    for database in migration.databases:
        try:
            console.print(database, style="info")
            conn = db.get_db_connection(migration.config, database)
            run_migration(conn)
        except Exception as e:
            console.print(e, style="error")
