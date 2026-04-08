from langgraph.graph import StateGraph, START, END
from state import WarRoomState

from nodes.data_analyst import data_analyst_node
from nodes.marketing import marketing_node
from nodes.pm import pm_node
from nodes.risk import risk_node
from nodes.final import final_node

def build_graph():
    graph = StateGraph(WarRoomState)
    
    graph.add_node("data_analyst", data_analyst_node)
    graph.add_node("marketing", marketing_node)
    graph.add_node("pm", pm_node)
    graph.add_node("risk", risk_node)
    graph.add_node("final", final_node)
    
    # Define execution graph sequence
    graph.add_edge(START, "data_analyst")
    graph.add_edge("data_analyst", "marketing")
    graph.add_edge("marketing", "pm")
    graph.add_edge("pm", "risk")
    graph.add_edge("risk", "final")
    graph.add_edge("final", END)
    
    return graph.compile()
