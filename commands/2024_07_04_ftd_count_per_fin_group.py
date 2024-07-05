import os
import click

from context import pass_context
from utils import db
from utils.style import console


def get_ftd_count(connection):
    query = ("select to_char(created_at, 'YYYY-MM') as month, count(id) as ftd_count "
             "from tickets "
             "where type = 'Deposit' "
             "and status = '1' "
             # "and mt5_type = 2 "
             "and is_ftd = 1 "
             "and method not in ('Manual', 'Bonus', 'Qiwi', 'Credit') "
             "and deleted_at is null "
             "and created_at >= '2023-07-01 00:00:00' and created_at < '2024-07-01 00:00:00' "
             "group by 1 "
             "order by 1 "
             ";")
    return db.execute_read_query(connection, query)


@click.command()
@pass_context
def cli(context):
    os.system("clear")

    db_args = context.config.db_args()
    existed_db_names = []
    fin_groups = set()
    fin_groups_monthly_ftd_counts = dict()

    for name, hosts, db_name, status, fin_group in context.brands:
        if fin_group:
            fin_groups.add(fin_group)

    for fin_group in fin_groups:
        fin_groups_monthly_ftd_counts[fin_group] = dict()

    for name, hosts, db_name, status, fin_group in context.brands:
        try:
            if status == "Dead" or db_name in existed_db_names:
                continue
            else:
                console.print(name, style="info")
                existed_db_names.append(db_name)

            conn = db.get_db_connection(context.config, db_name)
            monthly_ftd_count = get_ftd_count(conn)
            for month, count in monthly_ftd_count:
                console.print(f"{month} {count}", style="info")
                if month in fin_groups_monthly_ftd_counts[fin_group]:
                    fin_groups_monthly_ftd_counts[fin_group][month] += count
                else:
                    fin_groups_monthly_ftd_counts[fin_group][month] = 0
        except Exception as e:
            console.print(e, style="error")
            # console.print_exception(show_locals=True)

    fin_groups_monthly_ftd_counts = sorted(fin_groups_monthly_ftd_counts.items())
    for fin_group, monthly_ftd_count in fin_groups_monthly_ftd_counts:
        console.print(fin_group, style="info")

        monthly_ftd_count = sorted(monthly_ftd_count.items())
        for month, count in monthly_ftd_count:
            console.print(f"{month} {count}", style="info")
