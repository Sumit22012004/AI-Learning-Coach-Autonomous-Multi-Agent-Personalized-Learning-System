from typing import TypedDict, Annotated, List, Dict, Any, Optional
from langgraph.graph import StateGraph, END
from langchain_core.messages import BaseMessage
import operator

# Import Flows
from src.agents.flows.skill_analysis import skill_analysis_node
from src.agents.flows.curriculum import curriculum_generator_node
from src.agents.flows.task_assignment import task_assignment_node
from src.agents.flows.evaluation import evaluation_node
from src.agents.flows.progress_tracking import progress_tracking_node

class AgentState(TypedDict):
    """
    Shared state key-values.
    """
    user_id: str
    messages: Annotated[List[BaseMessage], operator.add]
    user_profile: Optional[Dict[str, Any]]
    curriculum_plan: Optional[Dict[str, Any]]
    current_module_id: Optional[str]
    current_task: Optional[Dict[str, Any]]
    next_agent: Optional[str]
    error: Optional[str]

def router(state: AgentState) -> str:
    """
    Router function to determine the next node based on state.
    """
    next_agent = state.get("next_agent")
    if next_agent == "skill_analysis":
        return "skill_analysis"
    elif next_agent == "curriculum_generator":
        return "curriculum_generator"
    elif next_agent == "task_assignment":
        return "task_assignment"
    elif next_agent == "evaluation":
        return "evaluation"
    elif next_agent == "progress_tracking":
        return "progress_tracking"
    else:
        return END

def create_graph():
    """
    Constructs the compiled multi-agent workflow graph.
    """
    workflow = StateGraph(AgentState)
    
    # 1. Add Nodes
    workflow.add_node("skill_analysis", skill_analysis_node)
    workflow.add_node("curriculum_generator", curriculum_generator_node)
    workflow.add_node("task_assignment", task_assignment_node)
    workflow.add_node("evaluation", evaluation_node)
    workflow.add_node("progress_tracking", progress_tracking_node)
    
    # 2. Add Edges (Logic is handled by router based on 'next_agent' state)
    
    # Skill Analysis -> Router
    workflow.add_conditional_edges(
        "skill_analysis",
        router,
        {
            "skill_analysis": "skill_analysis", # Loop for conversation
            "curriculum_generator": "curriculum_generator", # Done analyzing
            END: END
        }
    )
    
    # Curriculum -> Task
    workflow.add_conditional_edges(
        "curriculum_generator",
        router,
        {"task_assignment": "task_assignment", END: END}
    )
    
    # Task -> Evaluation (Wait for input)
    # Note: In a real async API, we might break the graph here and resume later.
    # For now, we assume continuous flow or external trigger.
    workflow.add_conditional_edges(
        "task_assignment",
        router,
        {"evaluation": "evaluation", END: END}
    )
    
    # Evaluation -> Progress
    workflow.add_conditional_edges(
        "evaluation",
        router,
        {"progress_tracking": "progress_tracking", END: END}
    )
    
    # Progress -> Loop back
    workflow.add_conditional_edges(
        "progress_tracking",
        router,
        {
            "task_assignment": "task_assignment", # Next task
            "curriculum_generator": "curriculum_generator", # Re-plan
            END: END
        }
    )
    
    # 3. Set Entry Point
    workflow.set_entry_point("skill_analysis")
    
    return workflow.compile()
