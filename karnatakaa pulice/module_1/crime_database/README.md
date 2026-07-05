# Module 1 - Crime Database

This module stores structured Karnataka SCRB crime records for chatbot queries,
analytics, hotspot detection, reporting, and later graph/network extraction.

## Recommended Database

Use PostgreSQL with PostGIS when possible. It supports spatial indexes and
location-based queries needed for hotspot detection.

MySQL is also supported through `schema_mysql.sql`.

## Main Table

`crime_records` stores:

- Crime ID
- Police Station
- District
- Crime Type
- Date
- Time
- Victim
- Suspect
- Vehicle
- Weapon
- Latitude
- Longitude
- Status

The schema also includes `notes`, timestamps, indexes, and a generated spatial
`location` column for map and hotspot queries.

## PostgreSQL Setup

```bash
createdb scrb
psql -d scrb -f crime_database/schema_postgresql.sql
psql -d scrb -f crime_database/seed_crime_records.sql
```

Example application connection string:

```bash
DATABASE_URL=postgresql+psycopg://scrb:scrb@localhost:5432/scrb
```

## MySQL Setup

```bash
mysql -u root -p -e "CREATE DATABASE scrb CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
mysql -u root -p scrb < crime_database/schema_mysql.sql
mysql -u root -p scrb < crime_database/seed_crime_records.sql
```

Example application connection string:

```bash
DATABASE_URL=mysql+pymysql://scrb:scrb@localhost:3306/scrb
```

## Python Usage

```python
from crime_database.database import SessionLocal
from crime_database.repository import search_crime_records

with SessionLocal() as session:
    records = search_crime_records(session, district="Bengaluru Urban")
```

## Next Integration Points

- Backend API endpoints can use `repository.py`.
- The LLM SQL/query planner can map natural-language filters to this schema.
- Hotspot analytics can use `latitude`, `longitude`, and `location`.
- Neo4j extraction can create person, vehicle, weapon, station, and location nodes
  from the same records.
