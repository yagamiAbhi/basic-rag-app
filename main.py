from factories.component_factory import ComponentFactory

def main():
    print("--- Starting RAG Application V1.0 ---")
    
    # 1. Initialize our Factory
    factory = ComponentFactory(config_path="config.yaml")

    # 2. Get our decoupled services
    ingestion_service = factory.get_ingestion_service()
    retrieval_service = factory.get_retrieval_service()
    generation_service = factory.get_generation_service()

    # 3. ETL Pipeline: Ingest the document
    print("\n[Ingestion Phase]")
    test_file = "Google.txt"
    try:
        ingestion_service.process_file(test_file)
        print(f"Successfully processed: {test_file}")
    except FileNotFoundError:
        print(f"Please create a '{test_file}' in the root directory to test.")
        return

    # 4. Interactive Chat Loop
    print("\n[Chat Phase] Type 'exit' to quit.")
    chat_history = []
    
    while True:
        user_query = input("\nYou: ")
        if user_query.lower() in ['exit', 'quit']:
            break

        # Retrieval Pipeline
        retrieved_docs = retrieval_service.retrieve(user_query)
        
        # Generation Pipeline
        response = generation_service.answer_query(
            query=user_query, 
            context=retrieved_docs, 
            chat_history=chat_history
        )

        print(f"\nAI: {response}")
        
        # Update conversational memory
        chat_history.append({"role": "user", "content": user_query})
        chat_history.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()