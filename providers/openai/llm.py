import logging
from typing import List, Dict
import openai
from interfaces.llm import BaseLLM
from core.entities import Document

logger = logging.getLogger(__name__)


class OpenAILLM(BaseLLM):
    def __init__(self, api_key: str, model_name: str = "gpt-4-turbo", temperature: float = 0.1):
        # We inject the config values when instantiating the class
        self.client = openai.OpenAI(api_key=api_key)
        self.model_name = model_name
        self.temperature = temperature

    def generate(self, prompt: str, context: List[Document], chat_history: List[Dict]) -> str:
        logger.debug(
            "Calling OpenAI chat completion (model=%s, context_docs=%d, history_messages=%d)",
            self.model_name,
            len(context),
            len(chat_history),
        )

        # 1. Format the context from retrieved documents
        context_text = "\n\n---\n\n".join([doc.text for doc in context])
        
        # 2. Build the final instruction
        final_instruction = (
            f"Use the following context to answer the user.\n\n"
            f"Context:\n{context_text}\n\n"
            f"User Prompt: {prompt}"
        )
        
        # 3. Prepare the conversation history for the API
        messages = chat_history.copy()
        messages.append({"role": "user", "content": final_instruction})
        
        # 4. Call the LLM
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=messages,
            temperature=self.temperature
        )

        answer = response.choices[0].message.content
        logger.debug("OpenAI response received (chars=%d)", len(answer))
        return answer
