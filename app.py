import streamlit as st
import os
from crewai import Agent, Task, Crew

# Bypass ChromaDB requirements
os.environ["CREWAI_DISABLE_MEMORY"] = "true"
os.environ["CREWAI_EMBEDDER"] = "openai"

# Simplified agent configuration
nuclear_expert = Agent(
    role="Nuclear Compliance Specialist",
    goal="Generate IAEA compliance checklists without database dependencies",
    backstory="Expert in nuclear regulations with streamlined analysis",
    verbose=True,
    allow_delegation=False,
    memory=False
)

task = Task(
    description="Create checklist for {project_type} projects",
    expected_output="Markdown list of 8-10 IAEA requirements with standard codes",
    agent=nuclear_expert
)

# Streamlit UI
st.title("⚛️ Nuclear Compliance Generator")
project_type = st.selectbox("Project Type", ["Waste Management", "Reactor Safety"])
if st.button("Generate"):
    result = Crew(agents=[nuclear_expert], tasks=[task]).kickoff({"project_type": project_type})
    st.markdown(result)
    st.markdown('[☕ Support Development](YOUR_BMAC_LINK)')