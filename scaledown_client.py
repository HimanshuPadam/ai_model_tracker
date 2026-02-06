import json
import os

class ModelDataEngine:
    def __init__(self, data_path="data/models_2026.json"):
        self.data_path = data_path
        self._ensure_data_exists()
        self.data = self._load_data()

    def _ensure_data_exists(self):
        os.makedirs("data", exist_ok=True)
        # UPDATED: We've added more models to the initial creation list
        sample_data = [
            {
                "name": "GPT-5.2 Turbo",
                "provider": "OpenAI",
                "benchmarks": {"reasoning": 98, "coding": 96},
                "pricing": {"input_1m": 2.50, "output_1m": 10.00},
                "specs": {"latency_ms": 300, "context_window": "128k"}
            },
            {
                "name": "Gemini 3 Pro",
                "provider": "Google",
                "benchmarks": {"reasoning": 95, "coding": 94},
                "pricing": {"input_1m": 2.00, "output_1m": 12.00},
                "specs": {"latency_ms": 500, "context_window": "2M"}
            },
            {
                "name": "Claude 4.5 Opus",
                "provider": "Anthropic",
                "benchmarks": {"reasoning": 99, "coding": 97},
                "pricing": {"input_1m": 5.00, "output_1m": 15.00},
                "specs": {"latency_ms": 900, "context_window": "200k"}
            },
            {
                "name": "Llama 4 (405B)",
                "provider": "Meta",
                "benchmarks": {"reasoning": 92, "coding": 93},
                "pricing": {"input_1m": 0.50, "output_1m": 0.50},
                "specs": {"latency_ms": 400, "context_window": "128k"}
            },
            {
                "name": "Gemini 3 Flash",
                "provider": "Google",
                "benchmarks": {"reasoning": 85, "coding": 82},
                "pricing": {"input_1m": 0.10, "output_1m": 0.30},
                "specs": {"latency_ms": 150, "context_window": "1M"}
            }
        ]
        
        # If the file doesn't exist, OR if you want to force an update, write the file
        if not os.path.exists(self.data_path):
            with open(self.data_path, 'w') as f:
                json.dump(sample_data, f, indent=4)

    def _load_data(self):
        with open(self.data_path, 'r') as f:
            return json.load(f)

    def get_all_models(self):
        return [model['name'] for model in self.data]
        
    def get_comparison_data(self, selected_names):
        selected_data = [m for m in self.data if m['name'] in selected_names]
        return json.dumps(selected_data, indent=2)
    
    def save_new_model(self, model_dict):
        """Adds a new model to the list and persists it to the JSON file."""
        self.data.append(model_dict)
        with open(self.data_path, 'w') as f:
            json.dump(self.data, f, indent=4)
    
    def get_h2h_context(self, model_a_name, model_b_name):
        """Formats a specific H2H comparison string for the AI."""
        models = [m for m in self.data if m['name'] in [model_a_name, model_b_name]]
        return json.dumps(models, indent=2)

if __name__ == "__main__":
    engine = ModelDataEngine()
    print(f"✅ Loaded {len(engine.get_all_models())} models successfully!")