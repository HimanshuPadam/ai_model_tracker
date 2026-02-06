import streamlit as st
import pandas as pd
from scaledown_client import ModelDataEngine
import requests
import urllib3
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import plotly.graph_objects as go
from openai import OpenAI

# Configuration
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

st.set_page_config(
    page_title="2026 AI Model Tracker",
    page_icon="🤖",
    layout="wide"
)

# API Keys (Keep these secure!)
SCALEDOWN_API_KEY = "zs8b8JXoFG9TK73EZX5AmK4MFWvHxmU2BFDU2kC7"
SCALEDOWN_URL = "https://api.scaledown.xyz/compress/raw/"
OPENAI_API_KEY = "your-openai-key-here" # REPLACE WITH YOUR OPENAI KEY

engine = ModelDataEngine()

# --- SIDEBAR ---
st.sidebar.header("Comparison Settings")
all_model_names = engine.get_all_models()
select_all = st.sidebar.checkbox("Select All Models")

if select_all:
    selected_models = st.sidebar.multiselect(
        "Select Models to Compare", options=all_model_names, default=all_model_names
    )
else:
    selected_models = st.sidebar.multiselect(
        "Select Models to Compare", options=all_model_names
    )

st.sidebar.divider()
with st.sidebar.expander("➕ Add New Model to Database"):
    with st.form("add_model_form", clear_on_submit=True):
        new_name = st.text_input("Model Name")
        new_provider = st.text_input("Provider")
        col_a, col_b = st.columns(2)
        new_in = col_a.number_input("Input $ (1M)", min_value=0.0, format="%.2f")
        new_out = col_b.number_input("Output $ (1M)", min_value=0.0, format="%.2f")
        new_reasoning = st.slider("Reasoning Score", 0, 100, 80)
        submit_new = st.form_submit_button("Save Model")

        if submit_new and new_name and new_provider:
            engine.save_new_model({
                "name": new_name, "provider": new_provider,
                "benchmarks": {"reasoning": new_reasoning, "coding": new_reasoning - 2},
                "pricing": {"input_1m": new_in, "output_1m": new_out},
                "specs": {"latency_ms": 300, "context_window": "128k"}
            })
            st.success(f"Added {new_name}")
            st.rerun()

# --- MAIN UI ---
st.title("🤖 AI Model Comparison Tool")
st.markdown("Compare 2026's top AI models using compressed benchmark data.")

if selected_models:
    raw_data = [m for m in engine.data if m["name"] in selected_models]
    df = pd.DataFrame(raw_data)

    st.subheader("📊 Comparison Overview")
    st.dataframe(df[["name", "provider", "benchmarks", "pricing", "specs"]], use_container_width=True)

    # --- CHARTS ---
    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("💰 Cost Comparison")
        cost_df = pd.DataFrame({
            "Input ($/1M)": [m["pricing"]["input_1m"] for m in raw_data],
            "Output ($/1M)": [m["pricing"]["output_1m"] for m in raw_data]
        }, index=selected_models)
        st.bar_chart(cost_df)

    with col2:
        st.subheader("📈 Capability Radar")
        categories = ["Reasoning", "Coding", "Creative", "Efficiency", "Latency Score"]
        fig = go.Figure()
        for m in raw_data:
            latency_score = max(0, 100 - (m["specs"].get("latency_ms", 500) / 10))
            values = [m["benchmarks"].get("reasoning", 50), m["benchmarks"].get("coding", 50), 
                      m["benchmarks"].get("creative", 70), 85, latency_score]
            values += values[:1]
            fig.add_trace(go.Scatterpolar(r=values, theta=categories + [categories[0]], fill="toself", name=m["name"]))
        fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])), template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)

    # --- AI RECOMMENDATION ---
    st.divider()
    st.subheader("🧠 AI Recommendation")
    user_goal = st.text_area("What are you building?", placeholder="e.g., A low-latency customer support bot...", height=120)

    analyze_btn = st.button("Generate AI Recommendation", type="primary")
    if analyze_btn:
            if not user_goal:
                st.error("Please enter your goal/use case first!")
            else:
                with st.spinner("Scaledown is analyzing benchmarks..."):
                    # 1. Get the data for selected models
                    comparison_context = engine.get_comparison_data(selected_models)
                    
                    # 2. Call Scaledown just to show the optimization power (optional but cool)
                    payload = {
                        "context": comparison_context,
                        "prompt": f"Recommend a model for: {user_goal}",
                        "scaledown": {"rate": "auto"}
                    }
                    headers = {"x-api-key": SCALEDOWN_API_KEY, "Content-Type": "application/json"}
                    
                    try:
                        session = requests.Session()
                        response = session.post(SCALEDOWN_URL, json=payload, headers=headers, verify=False, timeout=20)
                        scaledown_data = response.json()

                        # 3. INTERNAL LOGIC: Find the best model mathematically
                        # We'll look for the highest reasoning score among selected models
                        best_model = max(raw_data, key=lambda x: x['benchmarks'].get('reasoning', 0))
                        
                        st.divider()
                        st.markdown(f"### 🏆 Logic Recommendation: **{best_model['name']}**")
                        
                        # Custom logic based on user keywords
                        if "cheap" in user_goal.lower() or "cost" in user_goal.lower():
                            cheapest_model = min(raw_data, key=lambda x: x['pricing']['input_1m'])
                            st.write(f"Since you mentioned **cost**, the most budget-friendly option is **{cheapest_model['name']}** at ${cheapest_model['pricing']['input_1m']} per 1M tokens.")
                        else:
                            st.write(f"Based on your goal, **{best_model['name']}** is the top performer with a Reasoning Score of **{best_model['benchmarks']['reasoning']}**.")

                        # 4. Show the Scaledown Benefit
                        if "results" in scaledown_data:
                            with st.expander("🔍 See Scaledown Optimization"):
                                ratio = scaledown_data['results']['compression_ratio']
                                st.info(f"Scaledown reduced this prompt's size by **{ratio:.2%}**!")
                                st.code(scaledown_data['results']['compressed_prompt'], language="json")

                    except Exception as e:
                        st.error(f"Logic Error: {str(e)}")
else:
    st.info("💡 Select models from the sidebar to start comparing.")