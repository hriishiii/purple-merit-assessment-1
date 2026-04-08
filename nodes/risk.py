def risk_node(state):
    print("--- [NODE: Risk Assessment] ---")
    data = state.get("data_report", {})
    sentiment = state.get("sentiment", {})
    
    risks = []
    
    if data.get("health") == "bad":
        risks.append("Metric anomalies detected via Data Analyst")
    
    if sentiment.get("score", 1) < 0.5:
        risks.append("Highly critical negative user sentiment detected")
        
    severity = "high" if len(risks) >= 1 else "low"
    
    return {
        "risk_assessment": {
            "risks": risks,
            "severity": severity
        },
        "logs": [f"Risk Agent categorized current launch severity as: {severity.upper()}"]
    }
