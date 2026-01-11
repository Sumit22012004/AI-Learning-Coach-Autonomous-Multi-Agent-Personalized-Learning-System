from typing import Dict, Any
import json
from langchain_core.messages import SystemMessage
from src.core.llm import get_llm_client
from src.agents.graph import AgentState

SYSTEM_PROMPT = """You are the Evaluation Expert.
Compare the user's answer with the correct solution.
Provide:
1. A score (0-100).
2. Constructive feedback.
Output JSON:
{
  "score": 85,
  "feedback": "Correct approach, but missed edge case X."
}
"""

async def evaluation_node(state: AgentState) -> Dict[str, Any]:
    """
    Agent Node: Evaluates the user's latest submission.
    """
    task = state.get("current_task")
    # In a real flow, 'messages' would contain the user's submission as the last HumanMessage
    user_answer_msg = state["messages"][-1] 
    
    llm = get_llm_client()
    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        SystemMessage(content=f"Task: {json.dumps(task)}"),
        SystemMessage(content=f"User Answer: {user_answer_msg.content}")
    ]
    
    response = await llm.ainvoke(messages)
    
    try:
        content = response.content.replace("```json", "").replace("```", "")
        result = json.loads(content)
        
        # Save submission to DB would happen here (omitted for brevity)
        
        return {
            "messages": [response], # Feedback to user
            "next_agent": "progress_tracking"
        }
    except Exception as e:
        return {"error": f"Evaluation failed: {str(e)}"}
