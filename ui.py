import streamlit as st
import json
import pandas as pd
import requests
import os

st.set_page_config(page_title="War Room Dashboard", layout="wide")

st.title("🚀 Product Launch War Room")
st.markdown("This dashboard simulates the real-time inputs of our launch. The agents (Data Analyst, Marketing, Risk, PM) will analyze this data to produce a Go/No-Go decision.")

st.header("1. Live Dashboard (Mock Inputs)")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Quantitative Metrics")
    if os.path.exists('data/metrics.json'):
        with open('data/metrics.json', 'r') as f:
            metrics_data = json.load(f)
            df_metrics = pd.DataFrame(metrics_data)
            st.dataframe(df_metrics.tail(25), use_container_width=True)
    else:
        st.warning("No metrics data found in data/metrics.json")

with col2:
    st.subheader("User Feedback")
    if os.path.exists('data/feedback.json'):
        with open('data/feedback.json', 'r') as f:
            feedback_data = json.load(f)
            df_feedback = pd.DataFrame(feedback_data)
            st.dataframe(df_feedback.tail(15), use_container_width=True)
    else:
        st.warning("No feedback data found in data/feedback.json")

st.subheader("Release Notes")
if os.path.exists('data/release_notes.json'):
    with open('data/release_notes.json', 'r') as f:
        rn_data = json.load(f)
        if rn_data:
            latest = rn_data[-1]
            st.info(f"**Version**: {latest.get('version')}\n\n**Notes**:\n{latest.get('notes')}\n\n**Known Issues**:\n{latest.get('known_issues')}")

st.divider()

st.header("2. AI Agent Orchestration")
st.markdown("Trigger the multi-agent system (ensure `main.py` is running on port 8000).")

if st.button("Trigger War Room Agents", type="primary"):
    with st.spinner("🤖 Orchestrating agents (Analyst, Marketing, Risk, PM)... Check FastAPI terminal for logs..."):
        try:
            response = requests.post("http://127.0.0.1:8000/simulate", timeout=120)
            if response.status_code == 200:
                result = response.json()
                st.success("Simulation Complete! Check out the PM's structured decision below.")
                
                decision = result.get('decision', '').upper()
                if decision == 'PROCEED':
                    st.success(f"### Final Decision: {decision}")
                    st.balloons()
                elif decision == 'PAUSE':
                    st.warning(f"### Final Decision: {decision}")
                else:
                    st.error(f"### Final Decision: {decision}")
                
                colA, colB = st.columns(2)
                with colA:
                    st.metric("Confidence Score", f"{result.get('confidence_score')}/10")
                with colB:
                    st.markdown(f"**What would increase confidence?**\n\n{result.get('what_would_increase_confidence')}")

                st.markdown("#### Rationale")
                st.write(result.get('rationale'))
                
                st.markdown("#### 📝 Action Plan (24-48 hours)")
                if result.get('action_plan'):
                    df_action = pd.DataFrame(result.get('action_plan'))
                    st.table(df_action)
                
                st.markdown("#### 🚨 Risk Register")
                if result.get('risk_register'):
                    df_risks = pd.DataFrame(result.get('risk_register'))
                    st.table(df_risks)
                
                st.markdown("#### 📢 Communication Plan")
                st.info(result.get('communication_plan'))
                
            else:
                st.error(f"Error {response.status_code}: {response.text}")
        except requests.exceptions.ConnectionError:
            st.error("Failed to connect to the FastAPI backend. Please run `python main.py` in a separate terminal!")
        except Exception as e:
            st.error(f"An error occurred: {e}")
