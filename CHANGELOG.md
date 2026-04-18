# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2026-04-19

### Added
- **Provider Registry Pattern:** Created `core/registry.py` to handle dynamic tracking and instantiation of all application providers.
- **Decorator Routing:** Added `@ProviderRegistry` decorators to all existing classes in the `providers/` directory to enable automatic registration.
- **Plugin Manifest:** Added `providers/__init__.py` to trigger provider registrations securely at runtime.

### Changed
- **Component Factory Optimization:** Completely removed hardcoded provider imports and `if/elif` conditional logic from `factories/component_factory.py`. The factory now resolves dependencies dynamically via registry string lookups driven by `config.yaml`.
- **README Updates:** Updated the Developer Guide to reflect the zero-modification extensibility workflow using the new registry architecture.

## [1.0.0] - 2026-04-19

### Added
- **Core Architecture:** Implemented SOLID-compliant, interface-driven directory structure (`/core`, `/interfaces`, `/modules`, `/providers`, `/factories`).
- **Interfaces:** Created base contracts for `BaseDocumentLoader`, `BaseEmbedder`, `BaseVectorStore`, and `BaseLLM`.
- **Modules (Business Logic):**
  - `IngestionService`: Handles the ETL pipeline (Extract, Transform, Load).
  - `RetrievalService`: Handles query embedding and vector similarity search.
  - `GenerationService`: Handles prompt construction, conversational memory injection, and LLM execution.
- **Providers (Concrete Implementations):**
  - Text file loader (`TxtDocumentLoader`).
  - Local Ollama LLM integration (`OllamaLLM`).
  - Local Ollama embeddings integration (`OllamaEmbedder`).
  - Persistent vector database integration (`ChromaVectorStore`).
- **Configuration & Orchestration:**
  - Added `ComponentFactory` to dynamically inject dependencies based on system settings.
  - Added `config.yaml` for zero-code swapping of providers and models.
  - Implemented interactive CLI chat loop in `main.py` with chat history tracking.
