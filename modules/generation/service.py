import logging
from typing import List, Dict
from interfaces.llm import BaseLLM
from core.entities import Document

logger = logging.getLogger(__name__)


class GenerationService:
    def __init__(self, llm: BaseLLM):
        self.llm = llm

    def answer_query(self, query: str, context: List[Document], chat_history: List[Dict]) -> str:
        logger.debug(
            "Generation started (query_chars=%d, context_docs=%d, history_messages=%d)",
            len(query),
            len(context),
            len(chat_history),
        )

        # Format the system prompt instructions
        system_prompt = (
            "You are a helpful assistant. Use the provided context to answer the user's query. "
            "If the answer is not in the context, state that you do not know."
        )
        
        # Combine system prompt with the actual query
        final_prompt = f"{system_prompt}\n\nUser Query: {query}"
        
        # Call the injected LLM
        response = self.llm.generate(
            prompt=final_prompt, 
            context=context, 
            chat_history=chat_history
        )
        logger.debug("Generation completed (response_chars=%d)", len(response))
        return response
