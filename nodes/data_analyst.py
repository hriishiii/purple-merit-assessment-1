from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
import json

def data_analyst_node(state):
    print("--- [NODE: Data Analyst] ---")
    metrics = state.get("metrics", [])
    
    # Simple tool heuristic
    health = "good"
    anomalies = []
    # Identify if p95 latency spiked over 800ms
    for m in metrics:
        if m["metric_name"] == "API Latency p95 (ms)" and m["value"] > 500:
            anomalies.append(f"High API Latency on {m['date']}: {m['value']}ms")
            health = "bad"
            
    # Add LLM reasoning
    llm = ChatOpenAI(model="gpt-4o", temperature=0)
    prompt = f"Analyze the following metrics data for a product launch: {json.dumps(metrics[-20:])}. \nAnomalies detected by internal tool: {anomalies}. \nProvide a concise 2-sentence summary of the metrics health."
    
    response = llm.invoke([
        SystemMessage(content="You are an expert Data Analyst Agent evaluating quantitative product launch metrics."),
        HumanMessage(content=prompt)
    ])
    
    return {
        "data_report": {
            "summary": response.content,
            "anomalies": anomalies,
            "health": health
        },
        "logs": ["Data Analyst evaluated quantitative metrics and pinpointed anomalies."]
    }
