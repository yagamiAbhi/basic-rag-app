from typing import List
from interfaces.embedder import BaseEmbedder
from interfaces.vector_store import BaseVectorStore
from core.entities import Document

class RetrievalService:
    def __init__(
        self, 
        embedder: BaseEmbedder, 
        vector_store: BaseVectorStore,
        top_k: int = 5
    ):
        self.embedder = embedder
        self.vector_store = vector_store
        self.top_k = top_k

    def retrieve(self, user_query: str) -> List[Document]:
        # 1. Embed the query
        query_embedding = self.embedder.embed_text(user_query)
        
        # 2. Vector Search
        retrieved_docs = self.vector_store.search(query_embedding, self.top_k)
        
        # 3. TODO: Implement Re-ranker (e.g., Cohere, Cross-Encoder) here in V2
        # reranked_docs = self.reranker.rank(user_query, retrieved_docs)
        # return reranked_docs
        
        return retrieved_docs