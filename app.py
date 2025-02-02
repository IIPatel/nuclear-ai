import streamlit as st
import os
from crewai import Agent, Task, Crew
from openai import OpenAI

# COMPLETELY disable ChromaDB/memory features
os.environ["CREWAI_DISABLE_MEMORY"] = "true"
os.environ["CREWAI_DISABLE_EMBEDDER"] = "true"

# Initialize your custom LLM
client = OpenAI(
    base_url="https://api.electronhub.top/v1/",
    api_key=os.environ["ELECTRONHUB_API_KEY"]
)

# Configure Agent PROPERLY with your LLM
nuclear_agent = Agent(
    role="Nuclear Compliance Expert",
    goal="Generate accurate IAEA compliance checklists",
    backstory="20+ years experience in nuclear regulatory affairs",
    verbose=True,
    allow_delegation=False,
    llm=client,  # CRITICAL: Connect to your LLM
    memory=False
)

# Simple Task
task = Task(
    description="Create checklist for {project_type} projects",
    expected_output="Markdown list of 10 IAEA requirements with standard codes",
    agent=nuclear_agent
)

# Streamlit UI
st.title("⚛️ IAEA Compliance Generator")
project_type = st.selectbox("Project Type", ["Waste Management", "Reactor Safety"])

if st.button("Generate"):
    crew = Crew(agents=[nuclear_agent], tasks=[task])
    result = crew.kickoff({"project_type": project_type})
    st.markdown(result)
    st.markdown('[☕ Support Development](YOUR_BMAC_LINK)')