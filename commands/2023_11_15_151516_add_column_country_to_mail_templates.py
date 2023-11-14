import click

from init import pass_migration
from utils import db
from utils.style import console


def run_migration(connection):
    queries = (
        "ALTER TABLE mail_templates ADD country VARCHAR(255);",
        db.migration_query("2023_11_15_151516_add_column_country_to_mail_templates"),
    )
    for query in queries:
        db.execute_query(connection, query)


@click.command()
@pass_migration
def cli(migration):
    db_args = migration.config.db_args()

    for database in migration.databases:
        try:
            console.print(database, style="info")
            db_args.update({"db_name": database})
            connection = db.create_connection(**db_args)
            run_migration(connection)
        except Exception as e:
            console.print(e, style="error")