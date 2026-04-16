from typing import List
import openai
from interfaces.embedder import BaseEmbedder
from core.entities import Document

class OpenAIEmbedder(BaseEmbedder):
    def __init__(self, api_key: str, model_name: str = "text-embedding-3-small"):
        self.client = openai.OpenAI(api_key=api_key)
        self.model_name = model_name

    def embed_text(self, text: str) -> List[float]:
        response = self.client.embeddings.create(
            input=text,
            model=self.model_name
        )
        return response.data[0].embedding

    def embed_documents(self, documents: List[Document]) -> List[Document]:
        # Extract the text from all documents
        texts = [doc.text for doc in documents]
        
        # Call the API in batch to save time/requests
        response = self.client.embeddings.create(
            input=texts,
            model=self.model_name
        )
        
        # Attach the resulting vectors back to our Document entities
        for i, doc in enumerate(documents):
            doc.embedding = response.data[i].embedding
            
        return documents