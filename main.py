from crewai import Task, Crew

from agents.analyzer import incident_analyzer
from agents.retriever import knowledge_retriever
from agents.planner import resolution_planner
from agents.risk_assessor import risk_assessor

from skills.knowledge_skills import search_past_incidents

# =========================
# INCIDENT INPUT
# =========================
incident_description = """
Service: Payment API
Error: Timeout connecting to PostgreSQL
Frequency: High
Last Deployment: 2 hours ago
"""

# =========================
# TASK 1: ANALYZE INCIDENT
# =========================
analyze_task = Task(
    description=(
        "Analyze the incident and provide:\n"
        "- Incident category\n"
        "- Affected service\n"
        "- Severity (Low/Medium/High)\n"
        "- One-line summary\n\n"
        f"Incident:\n{incident_description}"
    ),
    expected_output="Structured incident analysis.",
    agent=incident_analyzer,
)

# =========================
# TASK 2: RETRIEVE HISTORY
# =========================
retrieve_task = Task(
    description=(
        "Retrieve the most relevant historical incidents using semantic search.\n\n"
        f"Incident:\n{incident_description}"
    ),
    expected_output="Relevant historical incidents.",
    agent=knowledge_retriever,
    tools=[search_past_incidents],
)

# =========================
# TASK 3: RESOLUTION PLAN
# =========================
plan_task = Task(
    description=(
        "Using the incident analysis and retrieved incidents, create a resolution plan with:\n"
        "A) Likely root cause\n"
        "B) Step-by-step resolution\n"
        "C) Validation steps\n"
        "D) Rollback plan\n"
        "E) Monitoring checklist\n"
    ),
    expected_output="Structured resolution plan.",
    agent=resolution_planner,
    context=[analyze_task, retrieve_task],
)

# =========================
# TASK 4: RISK & ESCALATION
# =========================
risk_task = Task(
    description=(
        "Assess the business risk and escalation needs using:\n"
        "- Incident analysis\n"
        "- Resolution plan\n\n"
        "Provide:\n"
        "- Final severity level (Sev-1/2/3)\n"
        "- Business impact\n"
        "- Escalation recommendation\n"
        "- Teams to notify"
    ),
    expected_output="Risk assessment and escalation decision.",
    agent=risk_assessor,
    context=[analyze_task, plan_task],
)

# =========================
# CREW EXECUTION
# =========================
crew = Crew(
    agents=[
        incident_analyzer,
        knowledge_retriever,
        resolution_planner,
        risk_assessor,
    ],
    tasks=[
        analyze_task,
        retrieve_task,
        plan_task,
        risk_task,
    ],
    verbose=True,
)

if __name__ == "__main__":
    result = crew.kickoff()
    print("\n\n===== FINAL INCIDENT REPORT =====\n")
    print(result)
