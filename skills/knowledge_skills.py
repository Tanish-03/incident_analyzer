from crewai.tools import tool
from memory.vector_store import IncidentVectorStore

# Initialize once (acts like long-term memory)
vector_store = IncidentVectorStore("data/incidents.json")

@tool("search_past_incidents")
def search_past_incidents(query: str) -> str:
    """
    Search historical incidents relevant to the given incident description.
    """
    results = vector_store.search(query, top_k=2)

    formatted = []
    for r in results:
        formatted.append(
            f"Incident ID: {r['incident_id']}\n"
            f"Service: {r['service']}\n"
            f"Error: {r['error']}\n"
            f"Root Cause: {r['root_cause']}\n"
            f"Resolution: {r['resolution']}\n"
        )

    return "\n---\n".join(formatted)
