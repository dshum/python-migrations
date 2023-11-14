import click

from init import pass_migration
from utils import db
from utils.style import console


def run_migration(connection):
    queries = (
        '''
        CREATE SEQUENCE "public"."coinpayments_transactions_id_seq" 
            INCREMENT 1
            MINVALUE  1
            MAXVALUE 2147483647
            START 1
            CACHE 1;
        ''',
        '''
        CREATE TABLE "public"."coinpayments_transactions" (
          "id" int4 NOT NULL DEFAULT nextval('coinpayments_transactions_id_seq'::regclass),
          "amount1" float4 NOT NULL,
          "amount2" float4 NOT NULL,
          "currency1" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
          "currency2" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
          "buyer_name" varchar(255) COLLATE "pg_catalog"."default",
          "email" varchar(255) COLLATE "pg_catalog"."default",
          "fee" float4,
          "ipn_id" varchar(255) COLLATE "pg_catalog"."default",
          "ipn_mode" varchar(255) COLLATE "pg_catalog"."default",
          "ipn_type" varchar(255) COLLATE "pg_catalog"."default",
          "ipn_version" varchar(255) COLLATE "pg_catalog"."default",
          "merchant" varchar(255) COLLATE "pg_catalog"."default",
          "received_amount" float4,
          "received_confirms" int4,
          "status" varchar(255) COLLATE "pg_catalog"."default",
          "status_text" varchar(255) COLLATE "pg_catalog"."default",
          "txn_id" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
          "address" varchar(255) COLLATE "pg_catalog"."default",
          "timeout" int4,
          "checkout_url" varchar(255) COLLATE "pg_catalog"."default",
          "status_url" varchar(255) COLLATE "pg_catalog"."default",
          "qrcode_url" varchar(255) COLLATE "pg_catalog"."default",
          "created_at" timestamp(6) NOT NULL,
          "updated_at" timestamp(6) NOT NULL
        )
        ;
        ''',
        db.migration_query("2023_10_18_113100_create_coinpayments_transactions_table"),
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
