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
    business_type VARCHAR,
    description TEXT,
    create_date TIMESTAMP,
    update_date TIMESTAMP
);

CREATE TABLE offer_data (
    id SERIAL PRIMARY KEY,
    data JSONB,
    requirements TEXT,
    responsibilities TEXT,
    original_language VARCHAR,
    translated_data JSONB,
    create_date TIMESTAMP,
    update_date TIMESTAMP
);

CREATE TABLE offer (
    id SERIAL PRIMARY KEY,
    url VARCHAR UNIQUE,
    name VARCHAR,
    position_level VARCHAR,
    id_data INTEGER,
    site_id INTEGER,
    id_company INTEGER,
    active BOOLEAN,
    create_date TIMESTAMP,
    update_date TIMESTAMP
);

CREATE TABLE technology (
    id SERIAL PRIMARY KEY,
    name VARCHAR UNIQUE,
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

CREATE TABLE geography (
    id SERIAL PRIMARY KEY,
    city VARCHAR,
    country VARCHAR,
    create_date TIMESTAMP,
    update_date TIMESTAMP
);

CREATE TABLE offer_geography (
    id SERIAL PRIMARY KEY,
    id_offer INTEGER,
    id_geography INTEGER,
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

-- Добавление внешних ключей
ALTER TABLE offer
    ADD CONSTRAINT fk_offer_data FOREIGN KEY (id_data) REFERENCES offer_data (id),
    ADD CONSTRAINT fk_offer_site FOREIGN KEY (site_id) REFERENCES site (id),
    ADD CONSTRAINT fk_offer_company FOREIGN KEY (id_company) REFERENCES company (id);

ALTER TABLE offer_technology
    ADD CONSTRAINT fk_offer_technology_offer FOREIGN KEY (id_offer) REFERENCES offer (id),
    ADD CONSTRAINT fk_offer_technology_technology FOREIGN KEY (id_technology) REFERENCES technology (id);

ALTER TABLE offer_geography
    ADD CONSTRAINT fk_offer_geography_offer FOREIGN KEY (id_offer) REFERENCES offer (id),
    ADD CONSTRAINT fk_offer_geography_geography FOREIGN KEY (id_geography) REFERENCES geography (id);

ALTER TABLE offer_salary
    ADD CONSTRAINT fk_offer_salary_salary FOREIGN KEY (id_salary) REFERENCES salary (id),
    ADD CONSTRAINT fk_offer_salary_offer FOREIGN KEY (id_offer) REFERENCES offer (id);
