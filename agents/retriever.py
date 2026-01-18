from crewai import Agent

knowledge_retriever = Agent(
    role="Incident Knowledge Specialist",
    goal=(
        "Retrieve the most relevant past incidents based on semantic similarity "
        "to the current incident description."
    ),
    backstory=(
        "You are responsible for institutional memory. You know past incidents, "
        "root causes, and resolutions. You do not speculate — you only retrieve "
        "relevant historical cases."
    ),
    verbose=True,
)
