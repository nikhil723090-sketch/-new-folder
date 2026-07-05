# Module 1 - Crime Database

This module stores structured Karnataka SCRB crime records used by the
chatbot, analytics, hotspot detection, reporting, and network analysis modules.

## Contents

- `crime_database/config.py` - database configuration
- `crime_database/database.py` - SQLAlchemy engine and sessions
- `crime_database/models.py` - crime record models
- `crime_database/repository.py` - query helpers
- `crime_database/schemas.py` - validation schemas
- `crime_database/schema_postgresql.sql` - PostgreSQL/PostGIS schema
- `crime_database/schema_mysql.sql` - MySQL schema
- `crime_database/seed_crime_records.sql` - sample records

See `crime_database/README.md` for setup and usage instructions.
