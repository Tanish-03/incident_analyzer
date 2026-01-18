import json
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

class IncidentVectorStore:
    def __init__(self, data_path: str):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.index = None
        self.metadata = []
        self._load_data(data_path)

    def _load_data(self, data_path: str):
        with open(data_path, "r", encoding="utf-8") as f:
            incidents = json.load(f)

        texts = []
        for incident in incidents:
            text = (
                f"Service: {incident.get('service','')}. "
                f"Error: {incident.get('error','')}. "
                f"Root cause: {incident.get('root_cause','')}. "
                f"Resolution: {incident.get('resolution','')}."
            )
            texts.append(text)
            self.metadata.append(incident)

        embeddings = self.model.encode(texts, convert_to_numpy=True)
        embeddings = embeddings.astype("float32")  # FAISS needs float32

        dim = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dim)
        self.index.add(embeddings)  # ✅ correct: numpy array (n, dim)

    def search(self, query: str, top_k: int = 2):
        q = self.model.encode([query], convert_to_numpy=True).astype("float32")  # shape (1, dim)
        distances, indices = self.index.search(q, top_k)

        results = []
        for idx in indices[0]:
            if idx == -1:
                continue
            results.append(self.metadata[idx])
        return results
