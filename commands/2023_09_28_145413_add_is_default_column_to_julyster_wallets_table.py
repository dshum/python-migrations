import click

from init import pass_migration
from utils import db
from utils.style import console


def run_migration(connection):
    queries = (
        "ALTER TABLE julyster_wallets ADD is_default boolean default false not null;",
        db.migration_query("2023_09_28_145413_add_is_default_column_to_julyster_wallets_table"),
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
