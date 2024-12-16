-- SQL Code for the Database Schema
DO $$ DECLARE
    table_name TEXT;
BEGIN
    FOR table_name IN
        SELECT tablename
        FROM pg_tables
        WHERE schemaname = 'public'
        LOOP
            EXECUTE format('DROP TABLE IF EXISTS %I CASCADE', table_name);
        END LOOP;
END $$;

CREATE TABLE site (
                      id SERIAL PRIMARY KEY,
                      name VARCHAR,
                      domain VARCHAR,
                      create_date TIMESTAMP,
                      update_date TIMESTAMP
);

CREATE TABLE company (
                         id SERIAL PRIMARY KEY,
                         name VARCHAR,
                         url VARCHAR,
                         description TEXT,
                         create_date TIMESTAMP,
                         update_date TIMESTAMP
);

CREATE TABLE location (
                          id SERIAL PRIMARY KEY,
                          site_id INTEGER,
                          url VARCHAR,
                          active BOOLEAN,
                          create_date TIMESTAMP,
                          update_date TIMESTAMP
);

CREATE TABLE offer (
                       id SERIAL PRIMARY KEY,
                       name VARCHAR,
                       id_company INTEGER,
                       create_date TIMESTAMP,
                       update_date TIMESTAMP
);

CREATE TABLE offer_location (
                                id SERIAL PRIMARY KEY,
                                offer_id INTEGER,
                                location_id INTEGER,
                                id_position_level INTEGER,
                                create_date TIMESTAMP,
                                update_date TIMESTAMP
);

CREATE TABLE technology (
                            id SERIAL PRIMARY KEY,
                            name VARCHAR UNIQUE,
                            create_date TIMESTAMP,
                            update_date TIMESTAMP
);

CREATE TABLE position_level (
                                id SERIAL PRIMARY KEY,
                                level VARCHAR UNIQUE,
                                create_date TIMESTAMP,
                                update_date TIMESTAMP
);

CREATE TABLE offer_technology (
                                  id SERIAL PRIMARY KEY,
                                  id_offer INTEGER,
                                  id_technology INTEGER,
                                  obligatory BOOLEAN,
                                  create_date TIMESTAMP,
                                  update_date TIMESTAMP
);

CREATE TABLE offer_data (
                            id SERIAL PRIMARY KEY,
                            id_offer INTEGER,
                            data JSONB,
                            requirements TEXT,
                            responsibilities TEXT,
                            id_original_language INTEGER,
                            translated_data JSONB,
                            create_date TIMESTAMP,
                            update_date TIMESTAMP
);

CREATE TABLE offer_position_level (
                                      id_offer INTEGER,
                                      id_position_level INTEGER,
                                      create_date TIMESTAMP,
                                      update_date TIMESTAMP
);

CREATE TABLE country (
                         id SERIAL PRIMARY KEY,
                         name VARCHAR,
                         create_date TIMESTAMP,
                         update_date TIMESTAMP
);

CREATE TABLE city (
                      id SERIAL PRIMARY KEY,
                      name VARCHAR,
                      create_date TIMESTAMP,
                      update_date TIMESTAMP
);

CREATE TABLE offer_geography (
                                 id SERIAL PRIMARY KEY,
                                 id_city INTEGER,
                                 id_country INTEGER,
                                 id_offer INTEGER,
                                 create_date TIMESTAMP,
                                 update_date TIMESTAMP
);

CREATE TABLE language (
                          id SERIAL PRIMARY KEY,
                          name VARCHAR,
                          create_date TIMESTAMP,
                          update_date TIMESTAMP
);

CREATE TABLE salary (
                        id SERIAL PRIMARY KEY,
                        value VARCHAR,
                        contract_type VARCHAR,
                        create_date TIMESTAMP,
                        update_date TIMESTAMP
);

CREATE TABLE offer_salary (
                              id SERIAL PRIMARY KEY,
                              id_salary INTEGER,
                              id_offer INTEGER,
                              create_date TIMESTAMP,
                              update_date TIMESTAMP
);

CREATE TABLE business_type (
                               id SERIAL PRIMARY KEY,
                               type VARCHAR,
                               create_date TIMESTAMP,
                               update_date TIMESTAMP
);

CREATE TABLE company_business_type (
                                       id SERIAL PRIMARY KEY,
                                       id_company INTEGER,
                                       id_business_type INTEGER,
                                       create_date TIMESTAMP,
                                       update_date TIMESTAMP
);

-- Foreign key relationships
ALTER TABLE location ADD FOREIGN KEY (site_id) REFERENCES site(id);
ALTER TABLE offer ADD FOREIGN KEY (id_company) REFERENCES company(id);
ALTER TABLE offer_location ADD FOREIGN KEY (offer_id) REFERENCES offer(id);
ALTER TABLE offer_location ADD FOREIGN KEY (location_id) REFERENCES location(id);
ALTER TABLE offer_technology ADD FOREIGN KEY (id_offer) REFERENCES offer(id);
ALTER TABLE offer_technology ADD FOREIGN KEY (id_technology) REFERENCES technology(id);
ALTER TABLE offer_data ADD FOREIGN KEY (id_offer) REFERENCES offer(id);
ALTER TABLE offer_data ADD FOREIGN KEY (id_original_language) REFERENCES language(id);
ALTER TABLE offer_position_level ADD FOREIGN KEY (id_offer) REFERENCES offer(id);
ALTER TABLE offer_position_level ADD FOREIGN KEY (id_position_level) REFERENCES position_level(id);
ALTER TABLE offer_geography ADD FOREIGN KEY (id_city) REFERENCES city(id);
ALTER TABLE offer_geography ADD FOREIGN KEY (id_country) REFERENCES country(id);
ALTER TABLE offer_geography ADD FOREIGN KEY (id_offer) REFERENCES offer(id);
ALTER TABLE offer_salary ADD FOREIGN KEY (id_salary) REFERENCES salary(id);
ALTER TABLE offer_salary ADD FOREIGN KEY (id_offer) REFERENCES offer(id);
ALTER TABLE company_business_type ADD FOREIGN KEY (id_company) REFERENCES company(id);
ALTER TABLE company_business_type ADD FOREIGN KEY (id_business_type) REFERENCES business_type(id);
