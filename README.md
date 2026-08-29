# Corporate SkillGraph Matrix Application

A complete graph database take-home engineering application built using **CognoDB Cloud**, **Python**, and **Streamlit**.

## ❓ Why a Graph Database?
In standard relational databases, mapping connections across organizational teams requires complex middle join tables and slow, multi-hop recursive SQL `JOIN` statements or CTEs. Graph databases leverage index-free adjacency, allowing queries to jump directly along memory pointer relationships instantly. This structure simplifies tracking knowledge intersections across global teams.

## 📊 Data Model Diagram
```text
(:Employee {name, team}) ───[:HAS_SKILL]───> (:Skill {name})
```

## 🔍 Core Multi-Hop Cypher Query
This application utilizes a parameterized **2-hop pattern traversal** to find colleagues who share overlapping skills with indirect team connections:
```cypher
MATCH (target:Skill {name: \$skillName})<-[:HAS_SKILL]-(directEmp:Employee)
MATCH (directEmp)-[:HAS_SKILL]->(sharedSkill:Skill)<-[:HAS_SKILL]-(colleague:Employee)
WHERE colleague <> directEmp
RETURN DISTINCT directEmp.name, sharedSkill.name, colleague.name
```

## 🚀 Local Installation
1. Clone the repository.
2. Install the required libraries: `pip install -r requirements.txt`
3. Configure your local variables inside a `.env` file with below credentials:
```text
    COGNODB_URI=YOUR_URI
    COGNODB_PASSWORD=YOUR_PASSWORD
```
4. Seed the instance: `python seed.py`
5. Launch the dashboard interface: `python -m streamlit run app.py`
