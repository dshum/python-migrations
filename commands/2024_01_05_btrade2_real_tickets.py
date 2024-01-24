import os
import csv
import click

from context import pass_context
from utils import db
from utils.style import console

CSV_FILE_NAME = "btrade_december_tickets.csv"


def get_tickets(connection):
    query = ("select tickets.id, tickets.type, tickets.status, "
             "tickets.value / 1e10, tickets.usd_value / 1e10, tickets.method, "
             "tickets.mt5_login, tickets.mt5_currency, "
             "tickets.is_ftd, tickets.created_at "
             "from tickets "
             "inner join customers on (customers.id = tickets.customer_id "
             "and customers.fname not ilike '%test%' "
             "and customers.lname not ilike '%test%' "
             "and customers.email not ilike '%test%') "
             "where tickets.status = '1' "
             "and tickets.method not in ('Manual', 'Bonus', 'Credit', 'Qiwi') "
             "and tickets.mt5_type not in (3, 6) "
             "and tickets.usd_value > 0 and tickets.usd_value < 1e16 "
             "and tickets.created_at >= '2023-12-01' and tickets.created_at < '2024-01-01' "
             "and tickets.deleted_at IS NULL "
             "order by tickets.id desc;")
    return db.execute_read_query(connection, query)


def get_tickets_v1(connection):
    query = ("select tickets.id, tickets.type, tickets.status, "
             "tickets.value / 1e10, tickets.usd_value / 1e10, tickets.method, "
             "'' as mt5_login, '' as mt5_currency, "
             "tickets.is_ftd, tickets.created_at "
             "from tickets "
             "inner join customers on (customers.id = tickets.customer_id "
             "and customers.fname not ilike '%test%' "
             "and customers.lname not ilike '%test%' "
             "and customers.email not ilike '%test%') "
             "where tickets.status = '1' "
             "and tickets.method not in ('Manual', 'Bonus', 'Credit', 'Qiwi') "
             "and tickets.usd_value > 0 and tickets.usd_value < 1e16 "
             "and tickets.created_at >= '2023-12-01' and tickets.created_at < '2024-01-01' "
             "and tickets.deleted_at IS NULL "
             "order by tickets.id desc;")
    return db.execute_read_query(connection, query)


def write_csv(name: str, hosts: str, tickets: dict):
    with open(CSV_FILE_NAME, "a") as f:
        writer = csv.writer(f)
        writer.writerow((name, hosts, f"{len(tickets)} tickets"))
        writer.writerow(("id", "type", "status", "value", "usd_value", "method",
                         "mt5_login", "mt5_currency", "is_ftd", "created_at"))
        for ticket in tickets:
            writer.writerow(ticket)


@click.command()
@pass_context
def cli(context):
    os.system("clear")

    db_args = context.config.db_args()
    existed_db_names = []

    for name, hosts, db_name, fin_group in context.brands:
        try:
            if name == "btrade2":
                console.print(name, style="info")
                existed_db_names.append(db_name)

                conn = db.get_db_connection(context.config, db_name)
                tickets = get_tickets(conn) if "crm2." in hosts else get_tickets_v1(conn)
                if len(tickets):
                    write_csv(name, hosts, tickets)
                    console.print(f"Found {len(tickets)} tickets", style="yellow")
        except Exception as e:
            console.print(e, style="error")
            # console.print_exception(show_locals=True)
