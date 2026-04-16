import logging

from config.settings import setup_logging
from factories.component_factory import ComponentFactory

logger = logging.getLogger(__name__)


def main():
    setup_logging(config_path="config.yaml")
    print("--- Starting RAG Application V1.0 ---")
    logger.info("Application startup initiated")
    
    # 1. Initialize our Factory
    logger.debug("Creating component factory from config.yaml")
    factory = ComponentFactory(config_path="config.yaml")

    # 2. Get our decoupled services
    logger.debug("Building ingestion, retrieval, and generation services")
    ingestion_service = factory.get_ingestion_service()
    retrieval_service = factory.get_retrieval_service()
    generation_service = factory.get_generation_service()
    logger.info("All services initialized successfully")

    # 3. ETL Pipeline: Ingest the document
    print("\n[Ingestion Phase]")
    test_file = "Google.txt"
    try:
        ingestion_service.process_file(test_file)
        print(f"Successfully processed: {test_file}")
        logger.info("Ingestion completed for %s", test_file)
    except FileNotFoundError:
        print(f"Please create a '{test_file}' in the root directory to test.")
        logger.exception("Ingestion failed because input file was missing: %s", test_file)
        return

    # 4. Interactive Chat Loop
    print("\n[Chat Phase] Type 'exit' to quit.")
    chat_history = []
    
    while True:
        user_query = input("\nYou: ")
        if user_query.lower() in ['exit', 'quit']:
            logger.info("Received exit command, shutting down chat loop")
            break

        logger.debug("Received user query (chars=%d)", len(user_query))
        # Retrieval Pipeline
        retrieved_docs = retrieval_service.retrieve(user_query)
        logger.debug("Retrieved %d documents for current query", len(retrieved_docs))
        
        # Generation Pipeline
        response = generation_service.answer_query(
            query=user_query, 
            context=retrieved_docs, 
            chat_history=chat_history
        )
        logger.debug("Generated response (chars=%d)", len(response))

        print(f"\nAI: {response}")
        
        # Update conversational memory
        chat_history.append({"role": "user", "content": user_query})
        chat_history.append({"role": "assistant", "content": response})
        logger.debug("Chat history updated (messages=%d)", len(chat_history))

if __name__ == "__main__":
    main()
