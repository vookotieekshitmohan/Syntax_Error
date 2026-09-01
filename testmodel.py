import sys

# ---------------------------------------------------
# Safe Imports
# ---------------------------------------------------
try:
    import joblib
except ImportError as exc:
    raise SystemExit(
        "Missing dependency: install it with '/usr/local/bin/python3 -m pip install joblib'"
    ) from exc

try:
    import pandas as pd
except ImportError as exc:
    raise SystemExit(
        "Missing dependency: install it with '/usr/local/bin/python3 -m pip install pandas'"
    ) from exc

# ---------------------------------------------------
# 1. Load Trained Model
# ---------------------------------------------------
MODEL_PATH = "traffic_model.pkl"

try:
    model = joblib.load(MODEL_PATH)
except FileNotFoundError:
    raise SystemExit(
        f"Error: '{MODEL_PATH}' not found. Please run 'aimodel.py' first to train and generate the model."
    )

# ---------------------------------------------------
# 2. Define Simulated Traffic Metrics
# ---------------------------------------------------
raw_input_data = {
    "bandwidth_mbps": 85.0,
    "latency_ms": 42.0,
    "packet_loss_pct": 0.6,
    "cpu_util_pct": 48.0,
    "connections": 600,
    "traffic_rate": 1000.0,
    "packet_count": 850
}

# ---------------------------------------------------
# 3. Align Input Data with Model's Expected Features
# ---------------------------------------------------
if hasattr(model, "feature_names_in_"):
    expected_features = list(model.feature_names_in_)
    # Build DataFrame matching exact column order and names expected by the model
    sample_dict = {
        col: raw_input_data.get(col, 0.0) for col in expected_features
    }
    new_data = pd.DataFrame([sample_dict])
else:
    # Fallback if model was trained without feature names
    new_data = pd.DataFrame([raw_input_data])

print("Input Data for Prediction:")
print(new_data)
print("-" * 40)

# ---------------------------------------------------
# 4. Make Prediction & Calculate Confidence
# ---------------------------------------------------
prediction = model.predict(new_data)[0]

if hasattr(model, "predict_proba"):
    probabilities = model.predict_proba(new_data)[0]
    confidence = max(probabilities) * 100
    print(f"Prediction : {prediction}")
    print(f"Confidence : {confidence:.2f}%")
else:
    print(f"Prediction : {prediction}")