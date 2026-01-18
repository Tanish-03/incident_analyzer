from memory.vector_store import IncidentVectorStore

store = IncidentVectorStore("data/incidents.json")
results = store.search("Postgres connection timeout")

for r in results:
    print(r["incident_id"], "-", r["root_cause"])