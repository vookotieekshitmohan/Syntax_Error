import importlib
import random
from datetime import datetime

try:
    flask_module = importlib.import_module("flask")
    Flask = flask_module.Flask
    jsonify = flask_module.jsonify
    render_template = flask_module.render_template
except ModuleNotFoundError as exc:
    raise RuntimeError("Flask is required: pip install flask") from exc

try:
    joblib = importlib.import_module("joblib")
except ModuleNotFoundError as exc:
    raise RuntimeError("joblib is required: pip install joblib") from exc

try:
    pandas_module = importlib.import_module("pandas")
    pd = pandas_module
except ModuleNotFoundError as exc:
    raise RuntimeError("pandas is required: pip install pandas") from exc

app = Flask(__name__)

# Load trained AI model safely
MODEL_PATH = "traffic_model.pkl"
try:
    model = joblib.load(MODEL_PATH)
except Exception as e:
    print(f"Warning: Could not load '{MODEL_PATH}': {e}")
    model = None


def generate_traffic():
    """Generates synthetic network telemetry."""
    is_anomaly = random.random() < 0.30

    if is_anomaly:
        return {
            "bandwidth_mbps": max(1.0, random.gauss(140, 25)),
            "latency_ms": max(1.0, random.gauss(130, 40)),
            "packet_loss_pct": min(100.0, max(0.0, random.gauss(3.5, 1.5))),
            "cpu_util_pct": min(100.0, max(0.0, random.gauss(85, 10))),
            "connections": max(1, round(random.gauss(1300, 300))),
        }

    return {
        "bandwidth_mbps": max(1.0, random.gauss(90, 25)),
        "latency_ms": max(1.0, random.gauss(45, 15)),
        "packet_loss_pct": max(0.0, random.expovariate(1.5)),
        "cpu_util_pct": min(100.0, max(0.0, random.gauss(55, 15))),
        "connections": max(1, round(random.gauss(650, 180))),
    }


def calculate_health(traffic, prediction):
    health = 100.0
    health -= min(30.0, traffic["latency_ms"] / 8)
    health -= min(25.0, traffic["packet_loss_pct"] * 5)
    health -= min(25.0, max(0.0, traffic["cpu_util_pct"] - 60) / 2)

    if str(prediction).strip().lower() == "anomaly":
        health -= 20.0

    return max(0, min(100, int(health)))


@app.route("/")
def dashboard():
    return render_template("dashboard.html")


@app.route("/traffic_api")
@app.route("/api/traffic")
def traffic_api():
    traffic = generate_traffic()
    prediction = "Normal"
    confidence = 95.0

    if model is not None:
        try:
            if hasattr(model, "feature_names_in_"):
                expected_cols = list(model.feature_names_in_)
                data = pd.DataFrame(
                    [{col: traffic.get(col, 0.0) for col in expected_cols}]
                )
            else:
                data = pd.DataFrame([traffic])

            pred_raw = model.predict(data)[0]
            prediction = str(pred_raw).capitalize()

            if hasattr(model, "predict_proba"):
                probs = model.predict_proba(data)[0]
                confidence = round(max(probs) * 100, 2)
        except Exception as err:
            print(f"Inference error: {err}")
            prediction = (
                "Anomaly" if traffic["bandwidth_mbps"] > 115 else "Normal"
            )

    is_anomaly = prediction.strip().lower() == "anomaly"
    health = calculate_health(traffic, prediction)

    if is_anomaly:
        severity = (
            "CRITICAL"
            if confidence >= 95
            else ("HIGH" if confidence >= 80 else "MEDIUM")
        )
        anomaly_type = "Traffic Surge / DoS Pattern"
    else:
        severity = "NONE"
        anomaly_type = "None"

    return jsonify(
        {
            "timestamp": datetime.now().strftime("%H:%M:%S"),
            "bandwidth": round(traffic["bandwidth_mbps"], 2),
            "latency": round(traffic["latency_ms"], 2),
            "packet_loss": round(traffic["packet_loss_pct"], 2),
            "cpu": round(traffic["cpu_util_pct"], 2),
            "connections": traffic["connections"],
            "prediction": "Anomaly" if is_anomaly else "Normal",
            "confidence": confidence,
            "health": health,
            "severity": severity,
            "endpoint": "Core-Gateway-01",
            "source_ip": (
                f"10.0.0.{random.randint(100, 250)}"
                if is_anomaly
                else f"192.168.1.{random.randint(10, 99)}"
            ),
            "anomaly_type": anomaly_type,
        }
    )


if __name__ == "__main__":
    app.run(debug=True, port=8080)