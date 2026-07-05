CREATE EXTENSION IF NOT EXISTS postgis;

CREATE TABLE IF NOT EXISTS crime_records (
    id BIGSERIAL PRIMARY KEY,
    crime_id VARCHAR(40) NOT NULL UNIQUE,
    police_station VARCHAR(120) NOT NULL,
    district VARCHAR(120) NOT NULL,
    crime_type VARCHAR(120) NOT NULL,
    crime_date DATE NOT NULL,
    crime_time TIME,
    victim VARCHAR(160),
    suspect VARCHAR(160),
    vehicle VARCHAR(120),
    weapon VARCHAR(120),
    latitude NUMERIC(9, 6) NOT NULL CHECK (latitude BETWEEN 11.0 AND 19.5),
    longitude NUMERIC(9, 6) NOT NULL CHECK (longitude BETWEEN 74.0 AND 79.5),
    location GEOGRAPHY(POINT, 4326)
        GENERATED ALWAYS AS (ST_SetSRID(ST_MakePoint(longitude, latitude), 4326)::geography) STORED,
    status VARCHAR(40) NOT NULL,
    notes TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_crime_records_district ON crime_records (district);
CREATE INDEX IF NOT EXISTS idx_crime_records_station ON crime_records (police_station);
CREATE INDEX IF NOT EXISTS idx_crime_records_type ON crime_records (crime_type);
CREATE INDEX IF NOT EXISTS idx_crime_records_date ON crime_records (crime_date);
CREATE INDEX IF NOT EXISTS idx_crime_records_status ON crime_records (status);
CREATE INDEX IF NOT EXISTS idx_crime_records_suspect ON crime_records (suspect);
CREATE INDEX IF NOT EXISTS idx_crime_records_location ON crime_records USING GIST (location);
