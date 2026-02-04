"""
AI Operations Assistant - Main Orchestrator
Coordinates the multi-agent workflow: Planner → Executor → Verifier
"""
import sys
import os

# Add backend to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
load_dotenv()

from agents import planner_agent, executor_agent, verifier_agent


class AIOperationsAssistant:
    """Main orchestrator for the AI Operations Assistant"""
    
    def __init__(self):
        self.planner = planner_agent
        self.executor = executor_agent
        self.verifier = verifier_agent
    
    def process_task(self, user_task: str) -> dict:
        """
        Process a user task through the multi-agent pipeline
        
        Args:
            user_task: Natural language task from user
            
        Returns:
            dict with complete results from all agents
        """
        result = {
            "user_task": user_task,
            "stages": {},
            "final_answer": None,
            "status": "processing"
        }
        
        # Stage 1: Planning
        try:
            plan = self.planner.create_plan(user_task)
            result["stages"]["planning"] = {
                "status": "success",
                "plan": plan
            }
        except Exception as e:
            result["stages"]["planning"] = {
                "status": "error",
                "error": str(e)
            }
            result["status"] = "failed"
            result["final_answer"] = f"Planning failed: {str(e)}"
            return result
        
        # Stage 2: Execution
        try:
            execution_results = self.executor.execute_plan(plan)
            result["stages"]["execution"] = {
                "status": "success",
                "results": execution_results
            }
        except Exception as e:
            result["stages"]["execution"] = {
                "status": "error",
                "error": str(e)
            }
            result["status"] = "partial"
            result["final_answer"] = f"Execution failed: {str(e)}"
            return result
        
        # Stage 3: Verification
        try:
            verification = self.verifier.verify_and_synthesize(user_task, execution_results)
            result["stages"]["verification"] = {
                "status": "success",
                "verification": verification
            }
            result["final_answer"] = verification.get("final_response", "No response generated")
            result["status"] = "complete"
        except Exception as e:
            result["stages"]["verification"] = {
                "status": "error", 
                "error": str(e)
            }
            result["status"] = "partial"
            result["final_answer"] = f"Verification failed: {str(e)}"
        
        return result


# Create singleton instance
assistant = AIOperationsAssistant()


def run_task(task: str) -> dict:
    """Convenience function to run a task"""
    return assistant.process_task(task)


if __name__ == "__main__":
    # CLI mode
    if len(sys.argv) > 1:
        task = " ".join(sys.argv[1:])
        print(f"\n🤖 Processing task: {task}\n")
        result = run_task(task)
        print(f"\n📋 Final Answer:\n{result['final_answer']}")
    else:
        print("Usage: python main.py <your task>")
        print("Example: python main.py 'What is the weather in London?'")
