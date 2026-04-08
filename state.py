from typing import TypedDict, List, Dict, Any, Optional
import operator
from typing import Annotated

class WarRoomState(TypedDict):
    """LangGraph State definition for the War Room simulation."""
    # Inputs injected at start
    metrics: List[Dict[str, Any]]
    feedback: List[Dict[str, Any]]
    release_notes: List[Dict[str, Any]]

    # Step-by-step reports
    data_report: Dict[str, Any]
    sentiment: Dict[str, Any]
    risk_assessment: Dict[str, Any]
    pm_decision: Dict[str, Any]

    # Final combined output
    final_output: Dict[str, Any]
    
    # Internal agent steps tracing
    logs: Annotated[List[str], operator.add]
