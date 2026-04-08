from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from pydantic import BaseModel, Field
from typing import List

class ActionItem(BaseModel):
    action: str
    owner: str

class LaunchDecisionFormat(BaseModel):
    decision: str = Field(description="Must be Proceed, Pause, or Roll Back")
    rationale: str
    actions: List[ActionItem]
    confidence: float

def pm_node(state):
    print("--- [NODE: Product Manager] ---")
    data = state.get("data_report", {})
    sentiment = state.get("sentiment", {})
    
    # LLM Structured extraction
    llm = ChatOpenAI(model="gpt-4o", temperature=0)
    structured_llm = llm.with_structured_output(LaunchDecisionFormat)
    
    prompt = f"Make a launch decision based on this Analyst Report: {data.get('summary')} and this Marketing Report: {sentiment.get('summary')}."
    
    # In a prod scenario we might pass the full tool history, this is kept optimal.
    result = structured_llm.invoke([
        SystemMessage(content="You are a Product Manager deciding if we should Proceed, Pause, or Roll Back a launch."),
        HumanMessage(content=prompt)
    ])
    
    return {
        "pm_decision": {
            "decision": result.decision,
            "rationale": result.rationale,
            "actions": [{"action": a.action, "owner": a.owner} for a in result.actions],
            "confidence": result.confidence
        },
        "logs": ["PM Agent synthesized cross-functional reports into a structured decision."]
    }
