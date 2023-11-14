import os

import psycopg2

from init import Config

exclude_databases = ", ".join((
    "assets", "brands", "cms", "controlcenter", "cron", "metabase",
    "mt5_henry", "mt5_henry_backup", "mt5_migrations",
    "mt5_xclusive", "mt5_zanx", "mt5_zanx2", "mt53",
    "positions_watcher", "postgres", "productiondb", "retool", "rdsadmin",
    "statistics", "template0", "template1", "wiki",
))


def create_ssh_tunnel(ssh_host, remote_db_host, remote_db_port, ssh_key):
    os.system(f"kill $(lsof -t -i:{remote_db_port})")
    os.system(f"sudo lsof -i -P -n | grep {remote_db_port}")
    os.system(f"ssh -f -N -i {ssh_key} {ssh_host} -L {remote_db_port}:{remote_db_host}")


def create_connection(db_name, db_user, db_password, db_host, db_port):
    return psycopg2.connect(
        database=db_name,
        user=db_user,
        password=db_password,
        host=db_host,
        port=db_port,
    )


def get_db_connection(config: Config, db_name: str):
    db_args = config.db_args()
    db_args.update({"db_name": db_name})
    return create_connection(**db_args)


def get_databases(connection):
    select_databases = (f"SELECT datname FROM pg_database "
                        f"WHERE datname <> ALL ('{{{exclude_databases}}}') "
                        f"ORDER BY datname;")
    databases = execute_read_query(connection, select_databases)
    return [database[0] for database in databases]


def get_brands(connection):
    query = "SELECT name, hosts, db_name, fin_group FROM brands ORDER BY name;"
    return execute_read_query(connection, query)
    # return [{"name": brand[0], "hosts": brand[1], "db_name": brand[2], "fin_group": brand[3]}
    #         for brand in brands]


def execute_read_query(connection, query, params: tuple = ()):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query, params)
        result = cursor.fetchall()
        return result
    except psycopg2.OperationalError as e:
        print(f"The error '{e}' occurred")


def execute_query(connection, query, params: tuple = ()):
    connection.autocommit = True
    cursor = connection.cursor()
    try:
        cursor.execute(query, params)
        print("Query executed successfully")
    except psycopg2.OperationalError as e:
        print(f"The error '{e}' occurred")


def migration_query(name: str):
    return f"INSERT INTO migrations (migration, batch) VALUES ('{name}', (SELECT max(batch) + 1 FROM migrations));"
