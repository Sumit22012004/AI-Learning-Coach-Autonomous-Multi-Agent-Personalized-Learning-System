from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
from src.agents.graph import create_graph
from langchain_core.messages import HumanMessage

router = APIRouter()

# Initialize the graph once
graph = create_graph()

class AgentRequest(BaseModel):
    user_id: str
    message: str
    context: Optional[Dict[str, Any]] = {}

class AgentResponse(BaseModel):
    response: str
    next_agent: Optional[str]
    current_state: Dict[str, Any] # Debugging/Frontend sync

@router.post("/interact", response_model=AgentResponse)
async def interact_with_agent(request: AgentRequest):
    """
    Main entry point for Chat UI to talk to the Agent System.
    """
    try:
        # Construct initial state input
        initial_state = {
            "user_id": request.user_id,
            "messages": [HumanMessage(content=request.message)],
            **request.context
        }
        
        # Run the graph (ainvoke runs until it hits an interrupt or END)
        # Note: In a real app, you'd load existing thread state from DB first
        final_state = await graph.ainvoke(initial_state)
        
        # Extract the last response from the AI
        last_message = final_state["messages"][-1]
        response_text = last_message.content if hasattr(last_message, "content") else str(last_message)
        
        return AgentResponse(
            response=response_text,
            next_agent=final_state.get("next_agent"),
            current_state={k: v for k, v in final_state.items() if k != "messages"} # Exclude huge message history
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
