def final_node(state):
    print("--- [NODE: Final Consolidation] ---")
    pm = state.get("pm_decision", {})
    risks = state.get("risk_assessment", {})
    
    decision = pm.get("decision", "Proceed")
    if risks.get("severity") == "high" and decision == "Proceed":
        # Risk override
        decision = "Pause"
        
    final_output = {
        "decision": decision,
        "rationale": pm.get("rationale"),
        "risk_register": risks.get("risks", []),
        "action_plan": pm.get("actions", []),
        "confidence_score": int(pm.get("confidence", 0.7) * 10),
        "communication_plan": "Internal: Halt rollout. External: Monitor." if decision == "Pause" else "Continue rollout linearly.",
        "what_would_increase_confidence": "More time to monitor DAU stability without spikes."
    }
    
    return {
        "final_output": final_output,
        "logs": ["Coordinator generated final structured output payload."]
    }
