queries = [
    '''
    CREATE SEQUENCE "public"."sms_requests_id_seq" 
        INCREMENT 1
        MINVALUE  1
        MAXVALUE 2147483647
        START 1
        CACHE 1;
    ''',
    '''
    CREATE TABLE "public"."sms_requests" (
      "id" int4 NOT NULL DEFAULT nextval('sms_requests_id_seq'::regclass),
      "employee_id" int4,
      "customer_id" int4,
      "provider" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
      "url" text COLLATE "pg_catalog"."default" NOT NULL,
      "arguments" text COLLATE "pg_catalog"."default",
      "response" text COLLATE "pg_catalog"."default",
      "status_code" int4 NOT NULL DEFAULT 200,
      "message" varchar(255) COLLATE "pg_catalog"."default",
      "created_at" timestamp(6) NOT NULL,
      "updated_at" timestamp(6) NOT NULL
    )
    ;
    ''',
    '''
    CREATE INDEX "sms_requests_customer_id_index" ON "public"."sms_requests" USING btree (
      "customer_id" "pg_catalog"."int4_ops" ASC NULLS LAST
    );
    ''',
    '''
    CREATE INDEX "sms_requests_employee_id_index" ON "public"."sms_requests" USING btree (
      "employee_id" "pg_catalog"."int4_ops" ASC NULLS LAST
    );
    ''',
    '''
    ALTER TABLE "public"."sms_requests" ADD CONSTRAINT "sms_requests_pkey" PRIMARY KEY ("id");
    ''',
]
