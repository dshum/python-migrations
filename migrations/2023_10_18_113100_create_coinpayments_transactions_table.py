queries = [
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
]
