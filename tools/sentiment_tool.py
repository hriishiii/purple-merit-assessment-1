import json
import os

def get_feedback_summary() -> str:
    """Read feedback data from JSON and return a summary string."""
    filepath = os.path.join("data", "feedback.json")
    if not os.path.exists(filepath):
        return "No feedback data found."
    with open(filepath, "r") as f:
        data = json.load(f)
    if not data:
        return "Feedback data is empty."
    
    summary = "=== Recent User Feedback ===\n"
    for item in data:
        summary += f"[{item.get('date')}] {item.get('sentiment').upper()}: {item.get('content')}\n"
    return summary
