"""Neo4j graph ingestion for crime relationship analysis."""

from __future__ import annotations

import os
from dataclasses import dataclass

import pandas as pd


@dataclass(frozen=True)
class GraphIngestSummary:
    """Summary of graph ingestion."""

    crimes: int
    suspects: int
    vehicles: int
    victims: int
    locations: int


class CrimeGraphBuilder:
    """Build a suspect-vehicle-location-victim-crime graph in Neo4j."""

    def __init__(self, uri: str | None = None, user: str | None = None, password: str | None = None) -> None:
        from neo4j import GraphDatabase

        self.driver = GraphDatabase.driver(
            uri or os.getenv("NEO4J_URI", "bolt://localhost:7687"),
            auth=(user or os.getenv("NEO4J_USER", "neo4j"), password or os.getenv("NEO4J_PASSWORD", "password")),
        )

    def close(self) -> None:
        self.driver.close()

    def create_constraints(self) -> None:
        statements = [
            "CREATE CONSTRAINT crime_id IF NOT EXISTS FOR (c:Crime) REQUIRE c.crime_id IS UNIQUE",
            "CREATE CONSTRAINT suspect_name IF NOT EXISTS FOR (s:Suspect) REQUIRE s.name IS UNIQUE",
            "CREATE CONSTRAINT victim_name IF NOT EXISTS FOR (v:Victim) REQUIRE v.name IS UNIQUE",
            "CREATE CONSTRAINT vehicle_id IF NOT EXISTS FOR (v:Vehicle) REQUIRE v.identifier IS UNIQUE",
            "CREATE CONSTRAINT location_id IF NOT EXISTS FOR (l:Location) REQUIRE l.key IS UNIQUE",
        ]
        with self.driver.session() as session:
            for statement in statements:
                session.run(statement)

    def ingest_records(self, records: pd.DataFrame) -> GraphIngestSummary:
        """Create graph nodes and edges from crime records."""

        query = """
        MERGE (c:Crime {crime_id: $crime_id})
        SET c.type = $crime_type, c.date = $crime_date, c.status = $status
        MERGE (l:Location {key: $location_key})
        SET l.district = $district, l.police_station = $police_station,
            l.latitude = $latitude, l.longitude = $longitude
        MERGE (c)-[:OCCURRED_AT]->(l)
        WITH c
        CALL {
          WITH c
          WITH c WHERE $suspect IS NOT NULL AND $suspect <> '' AND toLower($suspect) <> 'unknown'
          MERGE (s:Suspect {name: $suspect})
          MERGE (s)-[:SUSPECT_IN]->(c)
        }
        CALL {
          WITH c
          WITH c WHERE $victim IS NOT NULL AND $victim <> ''
          MERGE (v:Victim {name: $victim})
          MERGE (v)-[:VICTIM_IN]->(c)
        }
        CALL {
          WITH c
          WITH c WHERE $vehicle IS NOT NULL AND $vehicle <> ''
          MERGE (veh:Vehicle {identifier: $vehicle})
          MERGE (veh)-[:USED_IN]->(c)
        }
        """
        with self.driver.session() as session:
            for _, row in records.fillna("").iterrows():
                session.run(query, _row_params(row))
        return GraphIngestSummary(
            crimes=records["crime_id"].nunique(),
            suspects=_non_empty_unique(records, "suspect"),
            vehicles=_non_empty_unique(records, "vehicle"),
            victims=_non_empty_unique(records, "victim"),
            locations=records[["latitude", "longitude"]].drop_duplicates().shape[0],
        )


def _row_params(row: pd.Series) -> dict:
    return {
        "crime_id": str(row["crime_id"]),
        "crime_type": str(row["crime_type"]),
        "crime_date": str(row["crime_date"]),
        "status": str(row["status"]),
        "district": str(row["district"]),
        "police_station": str(row["police_station"]),
        "latitude": float(row["latitude"]),
        "longitude": float(row["longitude"]),
        "location_key": f"{row['district']}:{row['latitude']}:{row['longitude']}",
        "suspect": str(row.get("suspect", "")),
        "victim": str(row.get("victim", "")),
        "vehicle": str(row.get("vehicle", "")),
    }


def _non_empty_unique(records: pd.DataFrame, column: str) -> int:
    if column not in records:
        return 0
    values = records[column].dropna().astype(str)
    values = values[(values != "") & (values.str.lower() != "unknown")]
    return values.nunique()
