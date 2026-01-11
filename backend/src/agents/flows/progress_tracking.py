from typing import Dict, Any
from src.agents.graph import AgentState

async def progress_tracking_node(state: AgentState) -> Dict[str, Any]:
    """
    Agent Node: Analyzes result and decides next step.
    Simple logic: > 80% pass, else retry.
    """
    # We need to extract the score from the last AI message (Evaluation)
    # Ideally, the evaluation node should have passed the structured score in the state
    # For now, we simulate looking at the last message or a specific state key
    
    # Assuming evaluation_node stored result in a temporary state key (not yet defined in TypedDict, let's pretend)
    # In a real app, we'd add 'last_score' to AgentState
    
    # Placeholder logic
    last_score = 85 # Simulated success
    
    if last_score >= 80:
        return {
            "completed_tasks": [], # Add to list
            "next_agent": "task_assignment" # Get next task
        }
    else:
        # Needs remediation
        return {
            "next_agent": "curriculum_generator" # Re-plan or add review module
        }
