import os
import csv
import click

from context import pass_context
from utils import db
from utils.style import console


def get_countries(connection):
    query = ("select country, count(id) as trader_count from customers "
             "where created_at >= '2023-08-13' "
             "group by country having count(id) > 0 order by count(id) desc;")
    return db.execute_read_query(connection, query)


def write_csv(country_stat: dict):
    with open("countries.csv", "a") as f:
        writer = csv.writer(f)
        for group, stat in country_stat.items():
            writer.writerow((group,))
            sorted_countries = sorted(stat.items(), key=lambda x: x[1], reverse=True)
            for country, count in dict(sorted_countries).items():
                writer.writerow((country, count))
            writer.writerow("")


@click.command()
@pass_context
def cli(context):
    os.system("clear")

    db_args = context.config.db_args()
    country_stat = {}
    existed_db_names = []

    for name, hosts, db_name, fin_group in context.brands:
        try:
            console.print(name, style="info")

            if not fin_group or db_name in existed_db_names:
                console.print("Ignored", style="grey69")
                continue

            existed_db_names.append(db_name)

            conn = db.get_db_connection(context.config, db_name)
            countries = get_countries(conn)

            if fin_group not in country_stat:
                country_stat[fin_group] = {}

            for country, trader_count in countries:
                if country in country_stat[fin_group]:
                    country_stat[fin_group][country] = country_stat[fin_group][country] + int(trader_count)
                else:
                    country_stat[fin_group].update({country: trader_count})

            console.print(f"Found {len(countries)} countries", style="yellow")
        except Exception as e:
            console.print(e, style="error")

    write_csv(country_stat)
