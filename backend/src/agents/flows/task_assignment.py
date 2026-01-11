from typing import Dict, Any
import json
from langchain_core.messages import SystemMessage
from src.core.llm import get_llm_client
from src.agents.graph import AgentState

SYSTEM_PROMPT = """You are the Task Master.
Create a specific learning task for the user based on the current module topic.
Output JSON format:
{
  "type": "quiz",
  "content": {
    "question": "What function is used to read a CSV in Pandas?",
    "options": ["read_csv", "load_csv", "import_csv", "scan_csv"]
  },
  "solution": {"correct_option": "read_csv"}
}
"""

async def task_assignment_node(state: AgentState) -> Dict[str, Any]:
    """
    Agent Node: Generates the next task.
    """
    curriculum = state.get("curriculum_plan")
    if not curriculum:
        return {"error": "No curriculum found"}
        
    # Logic to find the next unfinished module/topic would go here
    current_topic = curriculum["modules"][0]["topics"][0] # specific logic needed
    
    llm = get_llm_client()
    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        SystemMessage(content=f"Create a task for topic: {current_topic}")
    ]
    
    response = await llm.ainvoke(messages)
    
    try:
        content = response.content.replace("```json", "").replace("```", "")
        task = json.loads(content)
        return {
            "current_task": task,
            "next_agent": "evaluation" # Wait for user input -> then evaluate
        }
    except Exception as e:
        return {"error": f"Task generation failed: {str(e)}"}
