"""
Planner Agent - Converts user input into step-by-step plan and selects tools
"""
from llm.gemini_client import GeminiClient, run_async
from tools import TOOL_DESCRIPTIONS


class PlannerAgent:
    """Agent responsible for creating execution plans from user tasks"""
    
    def __init__(self):
        self.llm = GeminiClient(
            system_message="""You are a Planner Agent for an AI Operations Assistant.
Your job is to analyze user requests and create structured execution plans.
You have access to specific tools and must select the appropriate ones.

Available tools:
- weather: Get current weather for a city
- news: Get latest news on a topic or headlines

Always respond with a valid JSON execution plan."""
        )
    
    def create_plan(self, user_task: str) -> dict:
        """
        Create an execution plan for the given task
        
        Args:
            user_task: Natural language task from user
            
        Returns:
            dict containing the execution plan
        """
        tools_info = "\n".join([f"- {name}: {desc}" for name, desc in TOOL_DESCRIPTIONS.items()])
        
        prompt = f"""Analyze this user task and create an execution plan.

USER TASK: {user_task}

AVAILABLE TOOLS:
{tools_info}

Create a JSON plan with this exact structure:
{{
    "task_summary": "Brief summary of what user wants",
    "steps": [
        {{
            "step_number": 1,
            "action": "Description of the action",
            "tool": "tool_name or null if no tool needed",
            "tool_input": "input for the tool or null",
            "expected_output": "what this step should produce"
        }}
    ],
    "final_output_format": "Description of the final answer format"
}}

Rules:
1. Use only available tools (weather, news) or null for reasoning steps
2. Break complex tasks into logical steps
3. Be specific about tool inputs
4. Each step should have a clear purpose"""

        result = run_async(self.llm.generate_json(prompt, session_id="planner"))
        
        # Validate plan structure
        if "steps" not in result:
            result = {
                "task_summary": user_task,
                "steps": [
                    {
                        "step_number": 1,
                        "action": "Process the request",
                        "tool": None,
                        "tool_input": None,
                        "expected_output": "Response to user"
                    }
                ],
                "final_output_format": "Text response",
                "error": result.get("error", "Plan generation incomplete")
            }
        
        return result


# Singleton instance
planner_agent = PlannerAgent()
