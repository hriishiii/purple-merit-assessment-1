import json
import os

def get_metrics_summary() -> str:
    """Read metrics data from JSON and return a summary string."""
    filepath = os.path.join("data", "metrics.json")
    if not os.path.exists(filepath):
        return "No metrics data found."
    with open(filepath, "r") as f:
        data = json.load(f)
    if not data:
        return "Metrics data is empty."
    
    summary = "=== Metrics Data (Last 14 Days) ===\n"
    for item in data[-30:]: # Return recent to save context length
        summary += f"{item.get('date')} - {item.get('metric_name')}: {item.get('value')}\n"
    return summary

def get_release_notes() -> str:
    filepath = os.path.join("data", "release_notes.json")
    if not os.path.exists(filepath):
        return "No release notes found."
    with open(filepath, "r") as f:
        data = json.load(f)
    if not data:
        return "Release notes are empty."
    
    note = data[-1]
    return f"Version: {note.get('version')}\nNotes: {note.get('notes')}\nKnown Issues: {note.get('known_issues')}"
