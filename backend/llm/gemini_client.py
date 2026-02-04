"""
Gemini LLM Client for AI Operations Assistant
Uses emergentintegrations library for Gemini 3 Flash
"""
import os
import json
import asyncio
from dotenv import load_dotenv
from emergentintegrations.llm.chat import LlmChat, UserMessage

load_dotenv()


class GeminiClient:
    """Wrapper for Gemini LLM interactions"""
    
    def __init__(self, system_message: str = "You are a helpful AI assistant."):
        self.api_key = os.environ.get("GEMINI_API_KEY")
        self.system_message = system_message
        
    def _create_chat(self, session_id: str) -> LlmChat:
        """Create a new chat instance with Gemini model"""
        chat = LlmChat(
            api_key=self.api_key,
            session_id=session_id,
            system_message=self.system_message
        ).with_model("gemini", "gemini-3-flash-preview")
        return chat
    
    async def generate(self, prompt: str, session_id: str = "default") -> str:
        """Generate a response from the LLM"""
        chat = self._create_chat(session_id)
        user_message = UserMessage(text=prompt)
        response = await chat.send_message(user_message)
        return response
    
    async def generate_json(self, prompt: str, session_id: str = "default") -> dict:
        """Generate a JSON response from the LLM"""
        json_prompt = f"""{prompt}

IMPORTANT: Respond ONLY with valid JSON. No markdown, no code blocks, no explanations.
Start directly with {{ and end with }}"""
        
        chat = self._create_chat(session_id)
        user_message = UserMessage(text=json_prompt)
        response = await chat.send_message(user_message)
        
        # Clean response and parse JSON
        cleaned = response.strip()
        if cleaned.startswith("```"):
            lines = cleaned.split("\n")
            cleaned = "\n".join(lines[1:-1] if lines[-1] == "```" else lines[1:])
        
        try:
            return json.loads(cleaned)
        except json.JSONDecodeError:
            # Try to extract JSON from response
            start = cleaned.find("{")
            end = cleaned.rfind("}") + 1
            if start != -1 and end > start:
                return json.loads(cleaned[start:end])
            return {"error": "Failed to parse JSON", "raw": response}


def run_async(coro):
    """Helper to run async functions synchronously"""
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            import nest_asyncio
            nest_asyncio.apply()
            return loop.run_until_complete(coro)
        return loop.run_until_complete(coro)
    except RuntimeError:
        return asyncio.run(coro)
