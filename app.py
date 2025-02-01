import streamlit as st
from crewai import Agent, Task, Crew
from crewai_tools import ScrapeWebsiteTool
from openai import OpenAI
import os

client = OpenAI(
    base_url="https://api.electronhub.top/v1/",
    api_key=os.environ["ELECTRONHUB_API_KEY"]  # Secure method
)

# App UI
st.title("⚛️ Nuclear Compliance AI Assistant")
st.caption("Auto-generate IAEA safety checklists")

# Tools
iaea_tool = ScrapeWebsiteTool(urls=['https://www.iaea.org/documents'])

# Agents
compliance_agent = Agent(
    role="Senior Nuclear Safety Engineer",
    goal="Create step-by-step compliance checklists for IAEA standards",
    backstory="20+ years experience in nuclear regulatory compliance",
    tools=[iaea_tool],
    verbose=True,
    llm=client  # Uses your custom API
)

# Task
task = Task(
    description="Generate checklist for: {project_type}",
    expected_output="Markdown list with 10 steps, IAEA standard codes, and deadlines",
    agent=compliance_agent
)

# User Inputs
project_type = st.selectbox(
    "Project Type",
    ["Waste Disposal", "Reactor Maintenance", "Fuel Transport"]
)

# Execution
if st.button("Generate Checklist"):
    crew = Crew(agents=[compliance_agent], tasks=[task])
    result = crew.kickoff(inputs={"project_type": project_type})
    
    st.markdown(result)
    
    # BMAC Integration (REPLACE LINK)
    st.markdown('[☕ Support This Tool](https://www.buymeacoffee.com/omnigpt)')
