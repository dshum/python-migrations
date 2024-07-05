import os
import click

from context import pass_context
from utils import db
from utils.style import console


def get_ftd_sum(connection):
    query = ("select SUM(usd_value) as ftd_sum "
             "from tickets "
             "where type = 'Deposit' "
             "and status = '1' "
             "and mt5_type = 2 "
             "and is_ftd = 1 "
             "and method not in ('Manual', 'Bonus', 'Qiwi', 'Credit') "
             "and deleted_at is null "
             "and created_at >= '2024-06-01 00:00:00' and created_at < '2024-08-01 00:00:00'"
             ";")
    return db.execute_read_query(connection, query)


@click.command()
@pass_context
def cli(context):
    os.system("clear")

    db_args = context.config.db_args()
    existed_db_names = []
    total: float = 0

    for name, hosts, db_name, status, fin_group in context.brands:
        try:
            if fin_group != "pixel" or status == "Dead" or db_name in existed_db_names:
                continue
            else:
                console.print(name, style="info")
                existed_db_names.append(db_name)

            conn = db.get_db_connection(context.config, db_name)
            ftd_sum = float(get_ftd_sum(conn)[0][0] or 0) / float(1e10)
            total += ftd_sum
            console.print("{:.2f} USD".format(ftd_sum), style="info")
        except Exception as e:
            console.print(e, style="error")
            # console.print_exception(show_locals=True)

    console.print("{:.2f} USD".format(total), style="info")
