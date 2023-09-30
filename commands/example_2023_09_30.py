import click

from utils import db, colors


def select_employees(connection):
    select_employees = ("SELECT id, login, fname, lname "
                        "FROM employees "
                        "WHERE \"group\" = 'root';")
    employees = db.execute_read_query(connection, select_employees)
    for employee in employees:
        colors.line(employee)


@click.command()
@click.pass_context
def cli(ctx):
    migration = ctx.obj

    db_args = migration.config.db_args()

    for database in migration.databases:
        try:
            colors.info(database)
            db_args.update({"db_name": database})
            connection = db.create_connection(**db_args)
            select_employees(connection)
        except Exception as e:
            colors.error(e)

    colors.success("Done")
