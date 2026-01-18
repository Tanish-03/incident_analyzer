from semantic_kernel.functions import kernel_function
from crewai import Crew, Task

from agents.analyzer import incident_analyzer
from agents.retriever import knowledge_retriever
from agents.planner import resolution_planner
from agents.risk_assessor import risk_assessor
from skills.knowledge_skills import search_past_incidents


class IncidentSkills:

    @kernel_function(
        name="analyze_incident",
        description="Analyze an incident and classify it"
    )
    def analyze(self, incident_description: str) -> str:
        task = Task(
            description=f"Analyze incident:\n{incident_description}",
            agent=incident_analyzer
        )
        crew = Crew(agents=[incident_analyzer], tasks=[task])
        return crew.kickoff()

    @kernel_function(
        name="retrieve_history",
        description="Retrieve similar historical incidents"
    )
    def retrieve(self, incident_description: str) -> str:
        task = Task(
            description=f"Retrieve similar incidents:\n{incident_description}",
            agent=knowledge_retriever,
            tools=[search_past_incidents]
        )
        crew = Crew(agents=[knowledge_retriever], tasks=[task])
        return crew.kickoff()

    @kernel_function(
        name="plan_resolution",
        description="Plan resolution using analysis and history"
    )
    def plan(self, context: str) -> str:
        task = Task(
            description=f"Create resolution plan:\n{context}",
            agent=resolution_planner
        )
        crew = Crew(agents=[resolution_planner], tasks=[task])
        return crew.kickoff()

    @kernel_function(
        name="assess_risk",
        description="Assess risk and escalation"
    )
    def assess(self, context: str) -> str:
        task = Task(
            description=f"Assess risk:\n{context}",
            agent=risk_assessor
        )
        crew = Crew(agents=[risk_assessor], tasks=[task])
        return crew.kickoff()
