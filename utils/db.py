import os

import psycopg2

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


def get_databases(connection):
    select_databases = (f"SELECT datname FROM pg_database "
                        f"WHERE datname <> ALL ('{{{exclude_databases}}}') "
                        f"ORDER BY datname;")
    databases = execute_read_query(connection, select_databases)
    return [database[0] for database in databases]


def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except psycopg2.OperationalError as e:
        print(f"The error '{e}' occurred")


def execute_query(connection, query):
    connection.autocommit = True
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print("Query executed successfully")
    except psycopg2.OperationalError as e:
        print(f"The error '{e}' occurred")


def migration_query(name: str):
    return f"INSERT INTO migrations (migration, batch) VALUES ('{name}', (SELECT max(batch) + 1 FROM migrations));"
