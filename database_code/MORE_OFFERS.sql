CREATE TABLE "site" (
  "id" serial PRIMARY KEY,
  "name" varchar,
  "domain" varchar,
  "create_date" timestamp,
  "update_date" timestamp
);

CREATE TABLE "company" (
  "id" serial PRIMARY KEY,
  "name" varchar,
  "url" varchar,
  "business_type" varchar,
  "description" text,
  "create_date" timestamp,
  "update_date" timestamp
);

CREATE TABLE "location" (
  "id" serial PRIMARY KEY,
  "site_id" integer,
  "url" varchar,
  "active" bool,
  "create_date" timestamp,
  "update_date" timestamp
);

CREATE TABLE "offer" (
  "id" serial PRIMARY KEY,
  "name" varchar,
  "work_type" varchar,
  "id_company" integer,
  "id_position_level" integer,
  "create_date" timestamp,
  "update_date" timestamp
);

CREATE TABLE "offer_location" (
  "id" serial PRIMARY KEY,
  "offer_id" integer,
  "location_id" integer,
  "id_position_level" integer,
  "create_date" timestamp,
  "update_date" timestamp
);

CREATE TABLE "technology" (
  "id" serial PRIMARY KEY,
  "name" varchar UNIQUE,
  "create_date" timestamp,
  "update_date" timestamp
);

CREATE TABLE "position_level" (
  "id" serial PRIMARY KEY,
  "level" varchar UNIQUE,
  "create_date" timestamp,
  "update_date" timestamp
);

CREATE TABLE "offer_technology" (
  "id" serial PRIMARY KEY,
  "id_offer" integer,
  "id_technology" integer,
  "obligatory" boolean,
  "create_date" timestamp,
  "update_date" timestamp
);

CREATE TABLE "offer_data" (
  "id" serial PRIMARY KEY,
  "id_offer" integer,
  "data" jsonb,
  "original_language" varchar,
  "translated_data" jsonb,
  "create_date" timestamp,
  "update_date" timestamp
);

CREATE TABLE "country" (
  "id" serial PRIMARY KEY,
  "name" varchar,
  "create_date" timestamp,
  "update_date" timestamp
);

CREATE TABLE "city" (
  "id" serial PRIMARY KEY,
  "name" varchar,
  "create_date" timestamp,
  "update_date" timestamp
);

CREATE TABLE "offer_geography" (
  "id" serial PRIMARY KEY,
  "id_city" integer,
  "id_country" integer,
  "id_offer" integer,
  "create_date" timestamp,
  "update_date" timestamp
);

CREATE TABLE "salary" (
  "id" serial PRIMARY KEY,
  "value" varchar,
  "contract_type" varchar,
  "create_date" timestamp,
  "update_date" timestamp
);

CREATE TABLE "offer_salary" (
  "id" serial PRIMARY KEY,
  "id_salary" integer,
  "id_offer" integer,
  "employment_type" varcahr,
  "create_date" timestamp,
  "update_date" timestamp
);

CREATE TABLE "working_type" (
  "id" serial PRIMARY KEY,
  "type" varchar UNIQUE,
  "create_date" timestamp,
  "update_date" timestamp
);

CREATE TABLE "offer_working_type" (
  "id" serial PRIMARY KEY,
  "id_working_type" integer,
  "if_offer" integer,
  "create_date" timestamp,
  "update_date" timestamp
);

ALTER TABLE "location" ADD FOREIGN KEY ("site_id") REFERENCES "site" ("id");

ALTER TABLE "offer" ADD FOREIGN KEY ("id_company") REFERENCES "company" ("id");

ALTER TABLE "offer" ADD FOREIGN KEY ("id_position_level") REFERENCES "position_level" ("id");

ALTER TABLE "offer_location" ADD FOREIGN KEY ("offer_id") REFERENCES "offer" ("id");

ALTER TABLE "offer_location" ADD FOREIGN KEY ("location_id") REFERENCES "location" ("id");

ALTER TABLE "offer_technology" ADD FOREIGN KEY ("id_offer") REFERENCES "offer" ("id");

ALTER TABLE "offer_technology" ADD FOREIGN KEY ("id_technology") REFERENCES "technology" ("id");

ALTER TABLE "offer_data" ADD FOREIGN KEY ("id_offer") REFERENCES "offer" ("id");

ALTER TABLE "offer_geography" ADD FOREIGN KEY ("id_city") REFERENCES "city" ("id");

ALTER TABLE "offer_geography" ADD FOREIGN KEY ("id_country") REFERENCES "country" ("id");

ALTER TABLE "offer_geography" ADD FOREIGN KEY ("id_offer") REFERENCES "offer" ("id");

ALTER TABLE "offer_salary" ADD FOREIGN KEY ("id_salary") REFERENCES "salary" ("id");

ALTER TABLE "offer_salary" ADD FOREIGN KEY ("id_offer") REFERENCES "offer" ("id");

ALTER TABLE "offer_working_type" ADD FOREIGN KEY ("id_working_type") REFERENCES "working_type" ("id");

ALTER TABLE "offer_working_type" ADD FOREIGN KEY ("if_offer") REFERENCES "offer" ("id");
