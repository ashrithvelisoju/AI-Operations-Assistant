"""
Executor Agent - Executes plan steps and calls APIs
"""
from llm.gemini_client import GeminiClient, run_async
from tools import AVAILABLE_TOOLS


class ExecutorAgent:
    """Agent responsible for executing plan steps and calling tools"""
    
    def __init__(self):
        self.llm = GeminiClient(
            system_message="""You are an Executor Agent for an AI Operations Assistant.
Your job is to execute individual steps of a plan and process tool outputs.
When a step requires reasoning without a tool, provide helpful analysis."""
        )
        self.tools = AVAILABLE_TOOLS
    
    def execute_step(self, step: dict, context: dict = None) -> dict:
        """
        Execute a single step from the plan
        
        Args:
            step: Step dict with action, tool, tool_input
            context: Previous execution results for reference
            
        Returns:
            dict with step execution result
        """
        context = context or {}
        step_number = step.get("step_number", 0)
        action = step.get("action", "Unknown action")
        tool_name = step.get("tool")
        tool_input = step.get("tool_input")
        
        result = {
            "step_number": step_number,
            "action": action,
            "status": "pending",
            "tool_used": tool_name,
            "output": None,
            "error": None
        }
        
        try:
            if tool_name and tool_name in self.tools:
                # Execute the tool
                tool = self.tools[tool_name]
                tool_result = tool.execute(tool_input)
                
                if tool_result.get("success", False):
                    result["status"] = "success"
                    result["output"] = tool_result
                else:
                    result["status"] = "failed"
                    result["error"] = tool_result.get("error", "Tool execution failed")
                    result["output"] = tool_result
                    
            elif tool_name and tool_name not in self.tools:
                result["status"] = "failed"
                result["error"] = f"Unknown tool: {tool_name}"
                
            else:
                # No tool needed - use LLM for reasoning
                context_str = "\n".join([
                    f"Step {k}: {v.get('output', 'N/A')}" 
                    for k, v in context.items() if isinstance(v, dict)
                ])
                
                prompt = f"""Execute this reasoning step:
Action: {action}

Previous context:
{context_str if context_str else 'No previous context'}

Provide a clear, concise response for this step."""

                llm_response = run_async(self.llm.generate(prompt, session_id=f"executor_{step_number}"))
                result["status"] = "success"
                result["output"] = {"reasoning": llm_response}
                
        except Exception as e:
            result["status"] = "error"
            result["error"] = str(e)
        
        return result
    
    def execute_plan(self, plan: dict) -> dict:
        """
        Execute all steps in a plan
        
        Args:
            plan: Full execution plan from PlannerAgent
            
        Returns:
            dict with all step results
        """
        results = {
            "task_summary": plan.get("task_summary", ""),
            "steps": [],
            "final_output_format": plan.get("final_output_format", ""),
            "overall_status": "pending"
        }
        
        context = {}
        all_success = True
        
        for step in plan.get("steps", []):
            step_result = self.execute_step(step, context)
            results["steps"].append(step_result)
            context[step.get("step_number", len(context))] = step_result
            
            if step_result["status"] not in ["success"]:
                all_success = False
        
        results["overall_status"] = "success" if all_success else "partial"
        return results


# Singleton instance
executor_agent = ExecutorAgent()
