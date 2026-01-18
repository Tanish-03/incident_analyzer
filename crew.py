from crewai import Task, Crew

from agents.analyzer import incident_analyzer
from agents.retriever import knowledge_retriever
from agents.planner import resolution_planner

from skills.knowledge_skills import search_past_incidents

incident_description = """
Service: Payment API
Error: Timeout connecting to PostgreSQL
Frequency: High
Last Deployment: 2 hours ago
"""

# 1) Analyze the incident
analyze_task = Task(
    description=(
        "Analyze the incident and return:\n"
        "- Incident category (Database/Auth/Infra/etc.)\n"
        "- Affected service\n"
        "- Severity (Low/Medium/High)\n"
        "- One-line summary\n\n"
        f"Incident:\n{incident_description}"
    ),
    expected_output="Structured incident analysis.",
    agent=incident_analyzer,
)

# 2) Retrieve similar historical incidents from memory (RAG)
retrieve_task = Task(
    description=(
        "Retrieve 2 most relevant historical incidents from memory for the given incident.\n"
        "Use the tool to search by meaning. Return the incidents exactly as found.\n\n"
        f"Incident:\n{incident_description}"
    ),
    expected_output="Relevant past incidents with root cause and resolution.",
    agent=knowledge_retriever,
    tools=[search_past_incidents],
)

# 3) Plan a resolution using analysis + retrieved incidents as evidence
plan_task = Task(
    description=(
        "Using:\n"
        "1) The incident analysis\n"
        "2) The retrieved historical incidents\n\n"
        "Create a resolution plan with sections:\n"
        "A) Likely root cause (based on evidence)\n"
        "B) Step-by-step resolution plan\n"
        "C) Validation steps\n"
        "D) Rollback plan\n"
        "E) Monitoring checklist (what metrics/logs to watch)\n\n"
        "Rules:\n"
        "- If history suggests a likely cause, mention it explicitly.\n"
        "- If uncertain, list 2-3 hypotheses and how to confirm.\n"
        "- Be concise but practical.\n"
    ),
    expected_output="A structured resolution plan with the requested sections.",
    agent=resolution_planner,
    context=[analyze_task, retrieve_task],  
)

crew = Crew(
    agents=[incident_analyzer, knowledge_retriever, resolution_planner],
    tasks=[analyze_task, retrieve_task, plan_task],
    verbose=True,
)

result = crew.kickoff()
print(result)
