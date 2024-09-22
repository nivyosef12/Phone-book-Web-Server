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


CREATE INDEX idx_phone_number ON contacts(phone_number);
CREATE INDEX idx_deleted_ts ON contacts(deleted_ts);
