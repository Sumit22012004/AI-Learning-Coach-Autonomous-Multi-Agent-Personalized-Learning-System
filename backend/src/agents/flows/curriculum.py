from typing import Dict, Any, List
import json
from langchain_core.messages import SystemMessage
from src.core.llm import get_llm_client
from src.agents.graph import AgentState
from src.core.vector_store import get_qdrant_client

SYSTEM_PROMPT = """You are the Curriculum Architect.
Based on the user's skill profile, generate a personalized learning curriculum.
Return a valid JSON object with a list of modules.
Format:
{
  "goal": "Master Python Data Science",
  "modules": [
    {"title": "Intro to Pandas", "description": "Basics of DataFrames", "topics": ["Series", "DataFrame", "Read CSV"]}
  ]
}
"""

async def curriculum_generator_node(state: AgentState) -> Dict[str, Any]:
    """
    Agent Node: Generates a curriculum based on skill profile.
    """
    user_profile = state.get("user_profile")
    if not user_profile:
        return {"error": "Missing user profile"}

    llm = get_llm_client()
    
    # RAG Step: Retrieve similar curriculums or topics (Placeholder)
    # qdrant = get_qdrant_client()
    # relevant_docs = qdrant.search("learning_materials", query_vector=...)

    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        SystemMessage(content=f"User Profile: {json.dumps(user_profile)}")
    ]
    
    response = await llm.ainvoke(messages)
    
    try:
        # Parse JSON from LLM response
        content = response.content.replace("```json", "").replace("```", "")
        plan = json.loads(content)
        
        return {
            "curriculum_plan": plan,
            "next_agent": "task_assignment" # Ready to start first task
        }
    except Exception as e:
        return {"error": f"Failed to parse curriculum: {str(e)}"}
