import os
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, HTTPException
import json
from graph import build_graph

app = FastAPI(title="War Room - LangGraph Simulation")

def load_data():
    with open("data/metrics.json") as f:
        metrics = json.load(f)
    with open("data/feedback.json") as f:
        feedback = json.load(f)
    if os.path.exists("data/release_notes.json"):
        with open("data/release_notes.json") as f:
            release_notes = json.load(f)
    else:
        release_notes = []
    return metrics, feedback, release_notes

@app.post("/simulate")
def trigger_simulation():
    """
    Triggers the LangGraph multi-agent war room simulation.
    Returns the final structured JSON decision.
    """
    try:
        metrics, feedback, release_notes = load_data()
        
        # Build and invoke langgraph state machine
        workflow = build_graph()
        result = workflow.invoke({
            "metrics": metrics,
            "feedback": feedback,
            "release_notes": release_notes,
            "logs": []
        })
        
        final_output = result.get("final_output", {})
        
        # Persist standard JSON per spec
        os.makedirs("output", exist_ok=True)
        with open("output/decision.json", "w") as f:
            json.dump(final_output, f, indent=4)
            
        print("Simulation complete. Output saved to output/decision.json.")
        
        return final_output
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
