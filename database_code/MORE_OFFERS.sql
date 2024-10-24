CREATE TABLE "site" (
  "id" integer PRIMARY KEY,
  "name" varchar,
  "domain" varchar,
  "create_date" datetime,
  "update_date" datetime
);

CREATE TABLE "company" (
  "id" integer PRIMARY KEY,
  "name" varchar,
  "url" varchar,
  "description" text,
  "create_date" datetime,
  "update_date" datetime
);

CREATE TABLE "location" (
  "id" integer PRIMARY KEY,
  "site_id" integer,
  "url" varchar,
  "active" bool,
  "create_date" datetime,
  "update_date" datetime
);

CREATE TABLE "offer" (
  "id" integer,
  "name" varchar,
  "id_company" integer,
  "id_position_level" integer,
  "create_date" datetime,
  "update_date" datetime,
  "primary" key(id,name,id_company)
);

CREATE TABLE "offer_location" (
  "id" integer PRIMARY KEY,
  "offer_id" integer,
  "location_id" integer,
  "id_position_level" integer,
  "create_date" datetime,
  "update_date" datetime
);

CREATE TABLE "technology" (
  "id" integer PRIMARY KEY,
  "name" varchar UNIQUE,
  "create_date" datetime,
  "update_date" datetime
);

CREATE TABLE "position_level" (
  "id" integer PRIMARY KEY,
  "level" varchar UNIQUE,
  "create_date" datetime,
  "update_date" datetime
);

CREATE TABLE "offer_technology" (
  "id" integer PRIMARY KEY,
  "id_offer" integer,
  "id_technology" integer,
  "create_date" datetime,
  "update_date" datetime
);

CREATE TABLE "offer_data" (
  "id" integer PRIMARY KEY,
  "id_offer" integer,
  "data" jsonb,
  "id_original_language" integer,
  "translated_data" jsonb,
  "create_date" datetime,
  "update_date" datetime
);

CREATE TABLE "country" (
  "id" integer PRIMARY KEY,
  "name" varchar,
  "create_date" datetime,
  "update_date" datetime
);

CREATE TABLE "city" (
  "id" integer PRIMARY KEY,
  "name" varchar,
  "create_date" datetime,
  "update_date" datetime
);

CREATE TABLE "offer_geography" (
  "id" integer PRIMARY KEY,
  "id_city" integer,
  "id_country" integer,
  "id_offer" integer,
  "create_date" datetime,
  "update_date" datetime
);

CREATE TABLE "language" (
  "id" integer PRIMARY KEY,
  "name" varchar,
  "create_date" datetime,
  "update_date" datetime
);

CREATE TABLE "salary" (
  "id" integer PRIMARY KEY,
  "value" varchar,
  "contract_type" varchar,
  "create_date" datetime,
  "update_date" datetime
);

CREATE TABLE "offer_salary" (
  "id" integer,
  "id_salary" integer,
  "id_offer" integer,
  "create_date" datetime,
  "update_date" datetime
);

CREATE TABLE "bussines_type" (
  "id" integer,
  "type" varchar,
  "create_date" datetime,
  "update_date" datetime
);

CREATE TABLE "company_bussines_type" (
  "id" integer,
  "id_company" integer,
  "id_bussines_type" integer,
  "create_date" datetime,
  "update_date" datetime
);

ALTER TABLE "company_bussines_type" ADD FOREIGN KEY ("id_company") REFERENCES "company" ("id");

ALTER TABLE "company_bussines_type" ADD FOREIGN KEY ("id_bussines_type") REFERENCES "bussines_type" ("id");

ALTER TABLE "offer_salary" ADD FOREIGN KEY ("id_salary") REFERENCES "salary" ("id");

ALTER TABLE "offer_salary" ADD FOREIGN KEY ("id_offer") REFERENCES "offer" ("id");

ALTER TABLE "location" ADD FOREIGN KEY ("site_id") REFERENCES "site" ("id");

ALTER TABLE "company" ADD FOREIGN KEY ("id") REFERENCES "offer" ("id_company");

ALTER TABLE "offer_location" ADD FOREIGN KEY ("location_id") REFERENCES "location" ("id");

ALTER TABLE "offer_location" ADD FOREIGN KEY ("offer_id") REFERENCES "offer" ("id");

ALTER TABLE "offer" ADD FOREIGN KEY ("id_position_level") REFERENCES "position_level" ("id");

ALTER TABLE "offer_technology" ADD FOREIGN KEY ("id_offer") REFERENCES "offer" ("id");

ALTER TABLE "technology" ADD FOREIGN KEY ("id") REFERENCES "offer_technology" ("id_technology");

ALTER TABLE "offer_data" ADD FOREIGN KEY ("id_offer") REFERENCES "offer" ("id");

ALTER TABLE "offer_geography" ADD FOREIGN KEY ("id_city") REFERENCES "city" ("id");

ALTER TABLE "offer_geography" ADD FOREIGN KEY ("id_country") REFERENCES "country" ("id");

ALTER TABLE "offer_geography" ADD FOREIGN KEY ("id_offer") REFERENCES "offer" ("id");

ALTER TABLE "offer_data" ADD FOREIGN KEY ("id_original_language") REFERENCES "language" ("id");
