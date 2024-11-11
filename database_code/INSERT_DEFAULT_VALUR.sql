-- Insert default value into the "site" table
INSERT INTO "site" (id, "name", "domain", "create_date", "update_date")
VALUES
    (0, 'Unknown Site', 'unknown.domain', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

-- Insert default value into the "company" table
INSERT INTO "company" (id, "name", "url", "description", "create_date", "update_date")
VALUES
    (0, 'Unknown Company', 'http://unknown.company', 'No description available.', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

-- Insert default value into the "location" table
INSERT INTO "location" (id, "site_id", "url", "active", "create_date", "update_date")
VALUES
    (0, 0, 'http://unknown.location', FALSE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

-- Insert default value into the "position_level" table
INSERT INTO "position_level" (id, "level", "create_date", "update_date")
VALUES
    (0, 'Unknown Level', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

-- Insert default value into the "offer" table
INSERT INTO "offer" (id, "name", "id_company", "id_position_level", "create_date", "update_date")
VALUES
    (0, 'Unknown Offer', 0, 0, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

-- Insert default value into the "technology" table
INSERT INTO "technology" (id, "name", "create_date", "update_date")
VALUES
    (0, 'Unknown Technology', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

-- Insert default value into the "offer_technology" table
INSERT INTO "offer_technology" (id, "id_offer", "id_technology", "create_date", "update_date")
VALUES
    (0, 0, 0, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

-- Insert default value into the "language" table
INSERT INTO "language" (id, "name", "create_date", "update_date")
VALUES
    (0, 'Unknown Language', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

-- Insert default value into the "offer_data" table
INSERT INTO "offer_data" (id, "id_offer", "data", "id_original_language", "translated_data", "create_date", "update_date")
VALUES
    (0, 0, '{}'::jsonb, 0, '{}'::jsonb, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

-- Insert default value into the "country" table
INSERT INTO "country" (id, "name", "create_date", "update_date")
VALUES
    (0, 'Unknown Country', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

-- Insert default value into the "city" table
INSERT INTO "city" (id, "name", "create_date", "update_date")
VALUES
    (0, 'Unknown City', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

-- Insert default value into the "offer_geography" table
INSERT INTO "offer_geography" (id, "id_city", "id_country", "id_offer", "create_date", "update_date")
VALUES
    (0, 0, 0, 0, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

-- Insert default value into the "salary" table
INSERT INTO "salary" (id, "value", "contract_type", "create_date", "update_date")
VALUES
    (0, 'Not Specified', 'Unknown', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

-- Insert default value into the "offer_salary" table
INSERT INTO "offer_salary" (id, "id_salary", "id_offer", "create_date", "update_date")
VALUES
    (0, 0, 0, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

-- Insert default value into the "business_type" table
INSERT INTO "bussines_type" (id, "type", "create_date", "update_date")
VALUES
    (0, 'Unknown Type', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

-- Insert default value into the "company_business_type" table
INSERT INTO "company_bussines_type" (id, "id_company", "id_bussines_type", "create_date", "update_date")
VALUES
    (0, 0, 0, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

-- Insert default value into the "offer_location" table
INSERT INTO "offer_location" (id, "offer_id", "location_id", "id_position_level", "create_date", "update_date")
VALUES
    (0, 0, 0, 0, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);
