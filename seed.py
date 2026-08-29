import os
from neo4j import GraphDatabase
from dotenv import load_dotenv

# Load credentials from your .env file
load_dotenv()
URI = os.getenv("COGNODB_URI")
PASSWORD = os.getenv("COGNODB_PASSWORD")

# Define sample corporate network data
employees = [
    {"id": "E1", "name": "Alice Smith", "team": "Engineering"},
    {"id": "E2", "name": "Bob Jones", "team": "Engineering"},
    {"id": "E3", "name": "Charlie Brown", "team": "Product"},
    {"id": "E4", "name": "Diana Prince", "team": "Design"},
    {"id": "E5", "name": "Evan Wright", "team": "Marketing"}
]

skills = [
    {"id": "S1", "name": "Python"},
    {"id": "S2", "name": "Neo4j / Cypher"},
    {"id": "S3", "name": "UI Design"},
    {"id": "S4", "name": "Growth Hacking"}
]

relationships = [
    {"emp_id": "E1", "skill_id": "S1"},  # Alice knows Python
    {"emp_id": "E1", "skill_id": "S2"},  # Alice knows Neo4j
    {"emp_id": "E2", "skill_id": "S1"},  # Bob knows Python
    {"emp_id": "E3", "skill_id": "S2"},  # Charlie knows Neo4j
    {"emp_id": "E4", "skill_id": "S3"},  # Diana knows UI Design
    {"emp_id": "E5", "skill_id": "S4"}   # Evan knows Growth Hacking
]

def seed_database():
    # Connect using the official Neo4j driver
    driver = GraphDatabase.driver(URI, auth=("cognodb", PASSWORD))
    with driver.session() as session:
        # Clear existing data safely to prevent duplicates
        session.run("MATCH (n) DETACH DELETE n")
        print("🧹 Database cleared.")

        # Create Employee Nodes using parameterized arrays
        session.run("""
        UNWIND $employees AS emp
        CREATE (e:Employee {id: emp.id, name: emp.name, team: emp.team})
        """, employees=employees)

        # Create Skill Nodes using parameterized arrays
        session.run("""
        UNWIND $skills AS sk
        CREATE (s:Skill {id: sk.id, name: sk.name})
        """, skills=skills)

        # Connect Employees to their Skills using paths
        session.run("""
        UNWIND $rels AS rel
        MATCH (e:Employee {id: rel.emp_id})
        MATCH (s:Skill {id: rel.skill_id})
        CREATE (e)-[:HAS_SKILL]->(s)
        """, rels=relationships)

        print("🌱 Seed data populated successfully!")
    driver.close()

if __name__ == "__main__":
    seed_database()
