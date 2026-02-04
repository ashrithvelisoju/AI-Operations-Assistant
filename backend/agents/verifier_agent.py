"""
Verifier Agent - Validates results and synthesizes final response
"""
from llm.gemini_client import GeminiClient, run_async


class VerifierAgent:
    """Agent responsible for validating results and creating final output"""
    
    def __init__(self):
        self.llm = GeminiClient(
            system_message="""You are a Verifier Agent for an AI Operations Assistant.
Your job is to:
1. Validate execution results for completeness and accuracy
2. Identify any missing or incorrect information
3. Synthesize results into a clear, structured final response
4. Suggest corrections if needed

Always provide helpful, accurate, and well-formatted responses."""
        )
    
    def verify_and_synthesize(self, original_task: str, execution_results: dict) -> dict:
        """
        Verify execution results and create final response
        
        Args:
            original_task: The original user request
            execution_results: Results from ExecutorAgent
            
        Returns:
            dict with verification status and final response
        """
        # Build context from execution results
        steps_summary = []
        has_errors = False
        tool_outputs = []
        
        for step in execution_results.get("steps", []):
            step_num = step.get("step_number", 0)
            status = step.get("status", "unknown")
            output = step.get("output", {})
            error = step.get("error")
            
            if status == "success" and output:
                if step.get("tool_used"):
                    tool_outputs.append({
                        "tool": step.get("tool_used"),
                        "data": output
                    })
                steps_summary.append(f"Step {step_num}: SUCCESS - {step.get('action', 'N/A')}")
            else:
                has_errors = True
                steps_summary.append(f"Step {step_num}: {status.upper()} - {error or 'Unknown error'}")
        
        # Create verification prompt
        prompt = f"""Verify and synthesize the following execution results.

ORIGINAL USER TASK: {original_task}

EXECUTION SUMMARY:
{chr(10).join(steps_summary)}

COLLECTED DATA:
{tool_outputs}

OVERALL STATUS: {execution_results.get('overall_status', 'unknown')}

Your tasks:
1. Check if the execution addressed the user's request completely
2. Identify any missing information or errors
3. Create a clear, helpful final response for the user

Respond with JSON:
{{
    "verification_status": "complete" or "partial" or "failed",
    "issues_found": ["list of any issues or missing data"],
    "final_response": "A clear, formatted response that directly answers the user's original question",
    "suggestions": ["any suggestions for improvement or additional info the user might want"]
}}"""

        result = run_async(self.llm.generate_json(prompt, session_id="verifier"))
        
        # Ensure required fields exist
        if "final_response" not in result:
            result["final_response"] = "Unable to generate a complete response. Please try again."
        if "verification_status" not in result:
            result["verification_status"] = "partial" if has_errors else "complete"
        if "issues_found" not in result:
            result["issues_found"] = []
        if "suggestions" not in result:
            result["suggestions"] = []
            
        # Add raw data for transparency
        result["raw_execution_results"] = execution_results
        
        return result


# Singleton instance
verifier_agent = VerifierAgent()
