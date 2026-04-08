# PurpleMerit - AI/ML Engineer Assessment 1 (War Room Simulation)

This project implements a multi-agent system that simulates a cross-functional war room during a product launch. A FastAPI backend is used to orchestrate four agents (Data Analyst, Marketing/Comms, Risk/Critic, and Product Manager) using OpenAI's models via explicit tool-calling capabilities.

## Architecture

- **FastAPI (`main.py`)**: Entry point to kickstart the simulation.
- **SQLite (`war_room.db`)**: Stores a 14-day mock dataset including metrics, user feedbacks, and release notes. 
- **Agents (`agents.py`)**: Defines the custom orchestration flow. Agents use "get_metrics_summary", "get_feedback_summary", and "get_release_notes" programmatically to fetch contexts.
- **Data Generator (`mock_data.py`)**: Script that seeds the SQLite DB with a failing product launch.

## Setup Instructions

1. **Clone/Download the repository**
2. **Create a virtual environment (optional but recommended)**:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```
3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Set Environment Variables**:
   You must export your OpenAI API key for the agents to function.
   ```bash
   export OPENAI_API_KEY="sk-your-openai-key"
   ```
   *(Alternatively, create a `.env` file and it will be loaded)*

## How to Run End-to-End

1. **Start the API Server**:
   ```bash
   python main.py
   ```
   *(This will automatically initialize `war_room.db` by running `mock_data.py` if it doesn't exist)*
   
2. **Trigger the Simulation**:
   Open a new terminal and invoke the simulation endpoint using `curl`:
   ```bash
   curl -X POST http://localhost:8000/simulate
   ```
   
   Alternatively, visit the interactive API docs at [http://localhost:8000/docs](http://localhost:8000/docs) and execute the `POST /simulate` endpoint directly.

3. **Check the Output**:
   - The CLI logs will trace which tool is called by which agent, and the handoffs.
   - A final structured report will be returned via the API response.
   - The output is automatically saved locally to `output.json`.

## Traceability
Traces of agent decisions and tool calls are visible directly in the console log where the FastAPI server is running. You will see markers like `--- [START: Agent Name] ---` and `[Agent Name] Tool called programmatically: get_metrics_summary`.

## Web Dashboard (Streamlit UI)

We have also included a Streamlit web UI to visualize the mock inputs seamlessly and simulate the launch decision cleanly without curl.

1. Ensure the FastAPI backend is running:
   ```bash
   python main.py
   ```
2. Open a new terminal and run:
   ```bash
   streamlit run ui.py
   ```
3. A local webpage will open. You can view the mock metrics data and User Feedback, and click **Trigger War Room* to stream the outcomes visually on the layout!