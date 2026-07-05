"""Useful Cypher queries for criminal network analysis."""

GANG_DISCOVERY = """
MATCH path = (s1:Suspect)-[:SUSPECT_IN]->(:Crime)<-[:USED_IN|VICTIM_IN|OCCURRED_AT*1..2]-(x)
WHERE s1.name IS NOT NULL
RETURN path
LIMIT 100
"""

SHARED_VEHICLE_NETWORK = """
MATCH path = (s1:Suspect)-[:SUSPECT_IN]->(:Crime)<-[:USED_IN]-(v:Vehicle)-[:USED_IN]->(:Crime)<-[:SUSPECT_IN]-(s2:Suspect)
WHERE s1.name <> s2.name
RETURN path
LIMIT 100
"""

SUSPECT_LOCATION_NETWORK = """
MATCH path = (s:Suspect)-[:SUSPECT_IN]->(:Crime)-[:OCCURRED_AT]->(l:Location)
RETURN path
LIMIT 100
"""
