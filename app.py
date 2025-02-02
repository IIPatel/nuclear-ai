import streamlit as st
import os
from crewai import Agent, Task, Crew
from openai import OpenAI

# Disable ChromaDB requirements
os.environ["CREWAI_EMBEDDER"] = "openai"  # Bypasses ChromaDB
os.environ["CREWAI_DISABLE_MEMORY"] = "true"  # Disables memory features

# Secure API setup
client = OpenAI(
    base_url="https://api.electronhub.top/v1/",
    api_key=os.environ["ELECTRONHUB_API_KEY"]
)

st.title("⚛️ Nuclear Compliance AI")
st.markdown("""
<style>
    .stApp {background: #f8f9fa}
    .stButton>button {background: #4CAF50!important; color: white!important;}
</style>
""", unsafe_allow_html=True)

# Simplified agent without ChromaDB-dependent tools
compliance_agent = Agent(
    role="Chief Nuclear Safety Officer",
    goal="Generate IAEA compliance checklists",
    backstory="20+ years experience in nuclear regulatory affairs",
    verbose=True,
    llm=client,
    memory=False  # Disables ChromaDB-based memory
)

# Task setup
task = Task(
    description="Create checklist for: {project_type}",
    expected_output="Markdown list with IAEA standard codes and deadlines",
    agent=compliance_agent
)

# UI Elements
project_type = st.selectbox(
    "Select Project Type",
    ["Waste Disposal", "Reactor Safety", "Radiation Shielding"]
)

if st.button("🚀 Generate Compliance Plan"):
    with st.spinner("Analyzing IAEA regulations..."):
        crew = Crew(agents=[compliance_agent], tasks=[task])
        result = crew.kickoff(inputs={"project_type": project_type})
        st.markdown(result)
        st.markdown('[☕ Support Development](YOUR_BMAC_LINK_HERE)')