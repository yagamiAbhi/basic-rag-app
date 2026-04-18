# 🚀 Modular RAG Architecture

[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A production-grade, highly decoupled Retrieval-Augmented Generation (RAG) pipeline designed for extensibility, scalability, and local execution.

Unlike standard RAG tutorials that tightly couple business logic to specific frameworks (like LangChain) or proprietary APIs (like OpenAI), this project is built from the ground up using **SOLID principles**. Core logic depends entirely on abstract interfaces, allowing you to hot-swap LLMs, vector stores, and embedding models via a simple configuration file with **zero code changes**.

---

## 🏗️ Architecture

The system is strictly separated into Contracts (Interfaces), Workstations (Modules), and Concrete Tools (Providers). The `ComponentFactory` dynamically resolves dependencies at runtime using a **Provider Registry**, ensuring the core logic remains closed for modification but completely open for extension.

```mermaid
flowchart LR
    classDef setup fill:#fff3e0,stroke:#e65100,stroke-width:2px;
    classDef module fill:#e1f5fe,stroke:#01579b,stroke-width:2px;
    classDef interface fill:#f9f2f4,stroke:#c7254e,stroke-width:2px,stroke-dasharray: 5 5;
    classDef provider fill:#e8f5e9,stroke:#1b5e20,stroke-width:2px;

    subgraph Setup ["1. Initialization"]
        direction TB
        main[main.py]:::setup
        factory[ComponentFactory]:::setup
        main --> factory
    end

    subgraph Modules ["2. Core Logic (Modules)"]
        direction TB
        ingest[IngestionService]:::module
        retrieval[RetrievalService]:::module
        gen[GenerationService]:::module
    end

    subgraph Interfaces ["3. Contracts (Interfaces)"]
        direction TB
        iLoader([BaseDocumentLoader]):::interface
        iEmbed([BaseEmbedder]):::interface
        iVector([BaseVectorStore]):::interface
        iLLM([BaseLLM]):::interface
    end

    subgraph Providers ["4. Implementations (Providers)"]
        direction TB
        txt[TxtDocumentLoader]:::provider
        oEmbed[OllamaEmbedder]:::provider
        chroma[ChromaVectorStore]:::provider
        oLLM[OllamaLLM]:::provider
    end

    factory ==>|Instantiates| ingest & retrieval & gen
    ingest ---> iLoader & iEmbed & iVector
    retrieval ---> iEmbed & iVector
    gen ---> iLLM

    iLoader -.->|Resolved to| txt
    iEmbed -.->|Resolved to| oEmbed
    iVector -.->|Resolved to| chroma
    iLLM -.->|Resolved to| oLLM
```

## 📁 Directory Structure

```text
basic-rag-app/
├── main.py                     # Application entry point
├── config.yaml                 # System behavior and provider toggles
├── requirements.txt            # Python dependencies
├── core/
│   ├── entities.py             # Shared data models (e.g., Document)
│   └── registry.py             # Provider Registry for dynamic class loading
├── interfaces/                 # Abstract Base Classes (The Contracts)
│   ├── document_loader.py
│   ├── embedder.py
│   ├── llm.py
│   └── vector_store.py
├── modules/                    # Core business logic
│   ├── generation/             # Prompting and LLM orchestration
│   ├── ingestion/              # ETL pipeline (Load, Chunk, Embed, Store)
│   └── retrieval/              # Vector search and reranking logic
├── providers/                  # Concrete implementations
│   ├── __init__.py             # Triggers decorator registrations
│   ├── chroma/                 # ChromaDB vector store
│   ├── local/                  # Local implementations (Ollama, Txt loader)
│   └── openai/                 # OpenAI API implementations (optional)
└── factories/
    └── component_factory.py    # Dependency injection logic via Registry lookup
```

## ⚡ Getting Started

### 1. Prerequisites

By default, the application runs entirely locally using Ollama. Ensure Ollama is installed and running, then pull the required models:

```bash
ollama pull qwen3:8b-q4_K_M
ollama pull qwen3-embedding:0.6b
```

### 2. Installation

Clone the repository and install dependencies:

```bash
git clone https://github.com/yagamiAbhi/basic-rag-app.git
cd basic-rag-app
pip install -r requirements.txt
```

### 3. Usage

Place the text data you want the assistant to learn in `Google.txt` at the project root (or update the `test_file` value in `main.py`).

Ensure your `config.yaml` is set properly (default uses Ollama + ChromaDB).

Start the app:

```bash
python main.py
```

The application ingests the document, stores embeddings in local ChromaDB, and opens a terminal chat loop for querying your data.

## 🧠 Extensibility (Developer Guide)

This application utilizes a Provider Registry pattern. Adding new features (like a Gemini LLM or a specialized medical data loader) requires absolutely no modifications to the core factory or `modules/` directory.

Example: adding a Gemini LLM provider
1. Create `providers/gemini/llm.py`.
2. Inherit from `BaseLLM` and implement `generate()`.
3. Add the `@ProviderRegistry.register_llm("gemini")` decorator to your class.
4. Import your new file in `providers/__init__.py`.
5. Update `config.yaml` to use `"gemini"`.
6. The factory will dynamically resolve and instantiate your new class at runtime.

## 🗺️ Roadmap

- [ ] Advanced ingestion: support PDFs, CSVs, and specialized web scraping.
- [ ] Semantic chunking: smarter text splitting strategies inside the ingestion module.
- [ ] Advanced retrieval: integrate a cross-encoder reranker to improve search accuracy.
- [ ] Settings validation: implement `pydantic` in `config/settings.py` for strict config validation.
- [ ] Long-term memory engine: transition from standard conversational arrays to an optimized chat history manager.
