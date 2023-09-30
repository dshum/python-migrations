import click

from init import pass_migration
from utils import db, colors


def run_migration(connection):
    queries = (
        # "ALTER TABLE table ADD COLUMN column VARCHAR NULL;",
        # db.migration_query("2023_09_26_093000_add_column_to_table"),
    )
    for query in queries:
        db.execute_query(connection, query)


@click.command()
@pass_migration
def cli(migration):
    db_args = migration.config.db_args()

    for database in migration.databases:
        try:
            colors.info(database)
            db_args.update({"db_name": database})
            connection = db.create_connection(**db_args)
            run_migration(connection)
        except Exception as e:
            colors.error(e)

    colors.success("Done")
