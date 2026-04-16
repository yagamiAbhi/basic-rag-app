import logging
import math
from typing import List
from interfaces.vector_store import BaseVectorStore
from core.entities import Document

logger = logging.getLogger(__name__)


class InMemoryVectorStore(BaseVectorStore):
    def __init__(self):
        self.documents: List[Document] = []

    def upsert(self, documents: List[Document]) -> None:
        self.documents.extend(documents)
        logger.info(
            "Upserted %d document(s) to memory store (total=%d)",
            len(documents),
            len(self.documents),
        )

    def search(self, query_embedding: List[float], top_k: int) -> List[Document]:
        # Helper function for Cosine Similarity
        def cosine_similarity(vec1, vec2):
            dot_product = sum(a * b for a, b in zip(vec1, vec2))
            magnitude = math.sqrt(sum(a * a for a in vec1)) * math.sqrt(sum(b * b for b in vec2))
            return dot_product / magnitude if magnitude else 0.0

        # Score all documents
        scored_docs = []
        for doc in self.documents:
            if doc.embedding:
                score = cosine_similarity(query_embedding, doc.embedding)
                scored_docs.append((score, doc))
        
        # Sort by score descending and return top_k
        scored_docs.sort(key=lambda x: x[0], reverse=True)
        top_docs = [doc for score, doc in scored_docs[:top_k]]
        logger.debug(
            "Memory search completed (top_k=%d, candidates=%d, returned=%d)",
            top_k,
            len(scored_docs),
            len(top_docs),
        )
        return top_docs
