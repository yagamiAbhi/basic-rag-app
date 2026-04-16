import requests
from typing import List
from interfaces.embedder import BaseEmbedder
from core.entities import Document

class OllamaEmbedder(BaseEmbedder):
    def __init__(self, model_name: str, base_url: str = "http://127.0.0.1:11434"):
        self.model_name = model_name
        self.base_url = base_url

    def embed_text(self, text: str) -> List[float]:
        payload = {
            "model": self.model_name,
            "prompt": text
        }
        
        response = requests.post(f"{self.base_url}/api/embeddings", json=payload, timeout=60)
        try:
            response.raise_for_status()
        except requests.HTTPError as exc:
            error_message = response.text
            try:
                error_message = response.json().get("error", response.text)
            except ValueError:
                pass
            raise RuntimeError(
                f"Ollama embedding failed for model '{self.model_name}': {error_message}"
            ) from exc
        
        return response.json()["embedding"]

    def embed_documents(self, documents: List[Document]) -> List[Document]:
        # Ollama's /api/embeddings endpoint processes one text at a time.
        # We loop through and attach embeddings sequentially.
        for doc in documents:
            doc.embedding = self.embed_text(doc.text)
            
        return documents
