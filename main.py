from semantic_kernel import Kernel
from semantic_kernel.functions import KernelArguments

# -------- SKILLS (CrewAI wrapped) ----------
from skills.incident_skills import IncidentSkills


def main():
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
    # 1️⃣ CREATE SEMANTIC KERNEL
    # =========================
    kernel = Kernel()

    # NOTE:
    # We are NOT using SK for LLM reasoning here.
    # SK is only orchestrating flow (Confucius role).
    # CrewAI agents handle LLM execution.
    
    # =========================
    # 2️⃣ REGISTER SKILLS
    # =========================
    kernel.import_skill(
        IncidentSkills(),
        skill_name="incident"
    )

    # =========================
    # 3️⃣ ORCHESTRATED FLOW
    # =========================

    print("\n--- STEP 1: ANALYZE INCIDENT ---\n")
    analysis = kernel.invoke(
        "incident.analyze_incident",
        KernelArguments(incident_description=incident_description),
    )

    print("\n--- STEP 2: RETRIEVE HISTORY (RAG) ---\n")
    history = kernel.invoke(
        "incident.retrieve_history",
        KernelArguments(incident_description=incident_description),
    )

    combined_context = f"""
    INCIDENT ANALYSIS:
    {analysis}

    HISTORICAL INCIDENTS:
    {history}
    """

    print("\n--- STEP 3: PLAN RESOLUTION ---\n")
    plan = kernel.invoke(
        "incident.plan_resolution",
        KernelArguments(context=combined_context),
    )

    print("\n--- STEP 4: RISK & ESCALATION ---\n")
    risk = kernel.invoke(
        "incident.assess_risk",
        KernelArguments(context=str(plan)),
    )

    # =========================
    print("\n\n===== FINAL INCIDENT REPORT =====\n")
    print(risk)


if __name__ == "__main__":
    main()
