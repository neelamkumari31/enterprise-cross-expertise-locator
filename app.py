import os
import streamlit as st
from neo4j import GraphDatabase
from dotenv import load_dotenv

load_dotenv()
URI = os.getenv("COGNODB_URI")
PASSWORD = os.getenv("COGNODB_PASSWORD")

# Initialize DB connection safely
@st.cache_resource
def get_db_driver():
    try:
        return GraphDatabase.driver(URI, auth=("cognodb", PASSWORD))
    except Exception as e:
        st.error("⚠️ Failed to connect to CognoDB Cloud. Verify connection settings.")
        return None
driver = get_db_driver()

# App Layout Customization
st.set_page_config(page_title="SkillGraph Explorer", page_icon="🕸️", layout="wide")
st.title("🕸️ Corporate SkillGraph Explorer")
st.caption("A candidate take-home technical application leveraging graph dependencies.")

if driver:
    # 1. Fetch skills dropdown list dynamically from the database
    with driver.session() as session:
        result = session.run("MATCH (s:Skill) RETURN s.name AS name ORDER BY name")
        skill_list = [record["name"] for record in result]

    # UI Dropdown Menu Selection
    selected_skill = st.selectbox("🎯 Target Skill Matrix:", skill_list)

    if st.button("Analyze Graph Connections", type="primary"):
        st.subheader(f"Results for: {selected_skill}")

        with driver.session() as session:
            # Multi-hop Traversal Query (2+ Hops)
            # Find colleagues who share skills with people who know the targeted skill
            query = """
            MATCH (target:Skill {name: $skillName})<-[:HAS_SKILL]-(directEmp:Employee)
            MATCH (directEmp)-[:HAS_SKILL]->(sharedSkill:Skill)<-[:HAS_SKILL]-(colleague:Employee)
            WHERE colleague <> directEmp
            RETURN DISTINCT 
                directEmp.name AS PrimaryExpert, 
                sharedSkill.name AS IntersectingSkill, 
                colleague.name AS SecondaryContact,
                colleague.team AS SecondaryTeam
            """
            
            results = session.run(query, skillName=selected_skill)
            records = [dict(r) for r in results]

            if records:
                st.success(f"Discovered {len(records)} structural relationship paths in the corporate network!")
                st.dataframe(records, use_container_width=True)
            else:
                st.info("No indirect paths found for this selection.")
