import os
import yaml
from dotenv import load_dotenv

# Local Providers
from providers.local.txt_loader import TxtDocumentLoader
from providers.local.memory_vector_store import InMemoryVectorStore
from providers.chroma.vector_store import ChromaVectorStore
from providers.local.ollama_llm import OllamaLLM
from providers.local.ollama_embedder import OllamaEmbedder

# Services
from modules.ingestion.service import IngestionService
from modules.retrieval.service import RetrievalService
from modules.generation.service import GenerationService

class ComponentFactory:
    def __init__(self, config_path: str = "config.yaml"):
        # Load behavior from config.yaml
        with open(config_path, "r") as f:
            self.config = yaml.safe_load(f)
            
        # Dynamically instantiate the Vector Store based on config
        vs_config = self.config["vector_store"]
        
        if vs_config["provider"] == "memory":
            self._vector_store = InMemoryVectorStore()
        elif vs_config["provider"] == "chroma":
            self._vector_store = ChromaVectorStore(
                collection_name=vs_config.get("collection_name", "local_knowledge"),
                persist_directory=vs_config.get("persist_directory", "./chroma_db")
            )
        else:
            raise ValueError(f"Unsupported vector store: {vs_config['provider']}")

    def get_ingestion_service(self) -> IngestionService:
        loader = TxtDocumentLoader()
        
        embedder_config = self.config["models"]["embedder"]
        if embedder_config["provider"] == "ollama":
            embedder = OllamaEmbedder(model_name=embedder_config["model_name"])
        else:
            raise ValueError(f"Unsupported embedder provider: {embedder_config['provider']}")

        chunk_size = self.config["ingestion"].get("chunk_size", 1000)
        chunk_overlap = self.config["ingestion"].get("chunk_overlap", 200)

        return IngestionService(
            loader=loader,
            embedder=embedder,
            vector_store=self._vector_store,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )

    def get_retrieval_service(self) -> RetrievalService:
        embedder_config = self.config["models"]["embedder"]
        
        if embedder_config["provider"] == "ollama":
            embedder = OllamaEmbedder(model_name=embedder_config["model_name"])
        else:
            raise ValueError(f"Unsupported embedder provider: {embedder_config['provider']}")
        
        top_k = self.config["retrieval"].get("top_k", 5)

        return RetrievalService(
            embedder=embedder,
            vector_store=self._vector_store,
            top_k=top_k
        )

    def get_generation_service(self) -> GenerationService:
        llm_config = self.config["models"]["llm"]
        
        if llm_config["provider"] == "ollama":
            llm = OllamaLLM(
                model_name=llm_config["model_name"],
                temperature=llm_config["temperature"]
            )
        else:
            raise ValueError(f"Unsupported LLM provider: {llm_config['provider']}")

        return GenerationService(llm=llm)
