import os
import random
import string

import click

from context import pass_context
from utils import db
from utils.style import console

users = [
    "tech_ol",
    "michael",
    "ivan",
    "andrey",
    "gustavo",
    "oleg",
    "andrei",
    "pavel",
    "stepan",
    "maxim",
    "denis",
    "alex",
    "ramil",
    "roman",
    "devops",
    "manuk",
    "anton",
    "yosef",
    "mikhail",
    "sergey",
    "bogdan",
    "dimo",
]


def update_passwords(connection, passwords):
    for user, password in passwords:
        query = f"""
        UPDATE employees set password='{password}' where login = '{user}';
        """
        db.execute_query(connection, query)


@click.command()
@pass_context
def cli(context):
    os.system("clear")

    passwords = {}
    password_hashes = {}

    for user in users:
        password = "".join(random.choices(string.ascii_lowercase + string.digits, k=8))
        passwords[user] = password
        # password_hashes[user] = bcrypt.hashpw(b"{password}", bcrypt.gensalt())
        # console.print(f"{user} {passwords[user]} {password_hashes[user]}")

    console.print(passwords)

    # for name, hosts, db_name, fin_group in context.brands:
    #     try:
    #         conn = db.get_db_connection(context.config, db_name)
    #         # update_passwords(conn, passwords)
    #         console.print(f"{name}, {hosts}, {db_name} - passwords updated", style="info")
    #
    #     except Exception as e:
    #         console.print(e, style="error")
    #         # console.print_exception(show_locals=True)
