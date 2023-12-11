import click

from context import pass_context
from utils import db
from utils.style import console


def run_migration(connection):
    # password = "$2y$10$ecSpCdVW9p4zWQ0El5f6juW9/9WRK9N2EkmuvnviA.hKz0EXQfQ8u" date = datetime.utcnow() query = (
    # 'INSERT INTO employees (email, fname, lname, login, password, active, "group", language, created_at,
    # updated_at) ' f"VALUES ('finance@test.com', 'Finance', 'User', 'finance', ''{password}', 1, 'finance',
    # 'English', '{date}', '{date}');") db.execute_query(connection, query) query = "UPDATE employees SET login =
    # 'finance' WHERE \"group\" = 'finance' and login IS NULL;"
    query = ("UPDATE employees SET created_at = '2023-11-06 08:12:11', updated_at = '2023-11-06 08:12:11' "
             "WHERE login = 'finance';")
    db.execute_query(connection, query)


@click.command()
@pass_context
def cli(context):
    db_args = context.config.db_args()

    for database in context.databases:
        try:
            console.print(database, style="info")
            db_args.update({"db_name": database})
            connection = db.create_connection(**db_args)
            run_migration(connection)
        except Exception as e:
            console.print(e, style="error")
