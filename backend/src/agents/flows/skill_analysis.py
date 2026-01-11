from typing import Dict, Any
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
from src.core.llm import get_llm_client
from src.agents.graph import AgentState

SYSTEM_PROMPT = """You are the Skill Analysis Agent for the AI Learning Coach.
Your goal is to actively diagnose the user's skill level in a specific topic.
1. Ask probing questions to understand their current knowledge.
2. If you have enough information, generate a JSON skill profile.
3. Be encouraging but precise.

If you are ready to finalize the profile, end your response with specific 'FINAL_PROFILE: {json_data}' format.
"""

async def skill_analysis_node(state: AgentState) -> Dict[str, Any]:
    """
    Agent Node: Diagnoses user skills through conversation.
    """
    messages = state["messages"]
    llm = get_llm_client()
    
    # Basic conversation chain
    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        *messages
    ])
    
    chain = prompt | llm
    response = await chain.ainvoke({})
    
    # Check if analysis is complete (Naive implementation for Phase 2 start)
    if "FINAL_PROFILE" in response.content:
        # TODO: Parse JSON securely in production
        # For now, we assume the next step is Curriculum Generation
        return {
            "messages": [response],
            "next_agent": "curriculum_generator"
        }
    
    return {
        "messages": [response],
        "next_agent": "skill_analysis" # Continue conversation
    }
