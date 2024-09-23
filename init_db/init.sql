CREATE TABLE IF NOT EXISTS contacts (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    phone_number VARCHAR(15) UNIQUE,
    address TEXT,
    created_ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_ts TIMESTAMP
);


CREATE EXTENSION pg_trgm;  -- for GIN indexes

CREATE INDEX idx_deleted_ts ON contacts(deleted_ts);
CREATE INDEX idx_first_name_gin ON contacts USING gin (first_name gin_trgm_ops);
CREATE INDEX idx_last_name_gin ON contacts USING gin (last_name gin_trgm_ops);
CREATE INDEX idx_phone_number_gin ON contacts USING gin (phone_number gin_trgm_ops);