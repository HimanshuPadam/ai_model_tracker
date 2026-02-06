📊 AI Model Tracker

AI Model Tracker is a Streamlit-based web app that lets you compare AI models (benchmarks, pricing, specs) and generate AI-assisted recommendations using the ScaleDown API.

This tool helps developers, researchers, and decision-makers visualize and compare different AI models to pick the best one for their use case.

🛠️ Features

✅ Select models from a sidebar list and compare them
✅ Display model benchmarks, pricing & specs in an interactive table
✅ Export comparison results as CSV
✅ Visualize price charts and radar charts for capabilities
✅ AI-powered recommendation using the ScaleDown API
✅ Add new models to the local database via a sidebar form

🧾 Requirements

1. Make sure you have Python 3.8+ installed.

2. Install dependencies:
    pip install -r requirements.txt

🚀 Run the App
    streamlit run app.py

📁 Project Structure
ai_model_tracker/
├── app.py
├── requirements.txt
├── scaledown_client.py
├── data/ model JSON files
├── __pycache__/
└── README.md

⚙️ Usage

🧠 Model Comparison
1. Use the sidebar to select models you want to compare.
2. View the comparison table in the main UI.
3. Download the results as CSV using the download button.

📊 Visual Charts
1. Price Chart: Compares input & output prices per 1M tokens.
2. Radar Chart: Visual “capability fingerprint” including reasoning, coding, efficiency, and latency.

🤖 AI Recommendation
    Enter your goal in the “AI Recommendation” section and click the button to get a suggestion on the best model.

🧩 Add New Model
    Expand the Add New Model section in the sidebar and fill in:
        Model name
        Provider
        Pricing
        Benchmarks
    Click “Save Model to JSON” to store it and refresh the app.

🔑 ScaleDown API Integration
    This project uses the ScaleDown API for prompt compression and reasoning augmentation:
        Add your API key in the app
        Sends model comparison context to ScaleDown
        Outputs recommendations based on compressed context

📦 Requirements
    Here’s a minimal list:
        streamlit
        pandas
        requests
        plotly
        scaledown-client

Install them via pip install -r requirements.txt.

🙌 Contributing
We welcome contributions! To contribute:
    Fork the repository
    Create a feature branch
    Submit a Pull Request

🧾 License
    This project is open source and available under the MIT License.

💬 Contact
Created by Himanshu Padam – himanshupadam808@gmail.com