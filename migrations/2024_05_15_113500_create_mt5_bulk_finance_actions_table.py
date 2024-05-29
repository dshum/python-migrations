queries = [
    '''
    CREATE SEQUENCE "public"."mt5_bulk_finance_actions_id_seq" 
    INCREMENT 1
    MINVALUE  1
    MAXVALUE 2147483647
    START 1
    CACHE 1;
    ''',

    '''
    CREATE TABLE "public"."mt5_bulk_finance_actions" (
      "id" int4 NOT NULL DEFAULT nextval('mt5_bulk_finance_actions_id_seq'::regclass),
      "employee_id" int4 NOT NULL,
      "broker_employee_id" int4,
      "mt5_type" int2 NOT NULL,
      "amount" float4 NOT NULL,
      "currency" varchar(10) COLLATE "pg_catalog"."default" NOT NULL,
      "direction" varchar(10) COLLATE "pg_catalog"."default" NOT NULL,
      "provider" varchar(255) COLLATE "pg_catalog"."default",
      "method" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
      "description" varchar(32) COLLATE "pg_catalog"."default",
      "meta" jsonb NOT NULL,
      "status" int2 NOT NULL,
      "created_at" timestamp(6) NOT NULL,
      "updated_at" timestamp(6) NOT NULL,
      "ticket_created_at" timestamp(6),
      "cancelled_at" timestamp(6)
    )
    ;
    ''',

    '''
    ALTER SEQUENCE "public"."mt5_bulk_finance_actions_id_seq"
    OWNED BY "public"."mt5_bulk_finance_actions"."id";
    SELECT setval('"public"."mt5_bulk_finance_actions_id_seq"', 5, true);
    ''',

    '''
    CREATE INDEX "mt5_bulk_finance_actions_broker_employee_id_index" ON "public"."mt5_bulk_finance_actions" USING btree (
      "broker_employee_id" "pg_catalog"."int4_ops" ASC NULLS LAST
    );
    ''',

    '''
    CREATE INDEX "mt5_bulk_finance_actions_employee_id_index" ON "public"."mt5_bulk_finance_actions" USING btree (
      "employee_id" "pg_catalog"."int4_ops" ASC NULLS LAST
    );
    ''',

    '''
    ALTER TABLE "public"."mt5_bulk_finance_actions" ADD CONSTRAINT "mt5_bulk_finance_actions_pkey" PRIMARY KEY ("id");
    ''',

]
