from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
import json

def marketing_node(state):
    print("--- [NODE: Marketing/Comms] ---")
    feedback = state.get("feedback", [])
    
    # Programmatic Tool heuristic
    negative_count = sum(1 for f in feedback if f.get("sentiment", "neutral").lower() == "negative")
    sentiment_score = 1.0 - (negative_count / max(len(feedback), 1))
    
    # LLM Reasoning
    llm = ChatOpenAI(model="gpt-4o", temperature=0)
    prompt = f"Summarize the recent user feedback for our product launch and identify the primary customer complaints: {json.dumps(feedback)}. Sentiment score is {sentiment_score} (0 is bad, 1 is perfect)."
    
    response = llm.invoke([
        SystemMessage(content="You are a Marketing and Comms Agent assessing user sentiment."),
        HumanMessage(content=prompt)
    ])
    
    return {
        "sentiment": {
            "score": sentiment_score,
            "summary": response.content
        },
        "logs": [f"Marketing Agent analyzed feedback. Negative ratio yielded score: {round(sentiment_score, 2)}"]
    }
