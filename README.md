# 🛡️ NetGuard AI (EdgeShield AI)

**Real-Time Network Telemetry Monitoring & AI Anomaly Detection Platform**

NetGuard AI is an intelligent, full-stack network monitoring dashboard built using **Python (Flask)**, **Machine Learning (Scikit-Learn Random Forest)**, and **Chart.js**. It processes live synthetic network telemetry (bandwidth, latency, packet loss, CPU utilization, and active connections), detects potential anomalies/attacks in real time, and provides automated threat diagnostics.

---

## ✨ Features

- **Live Network Telemetry**: Visualizes real-time metrics for bandwidth, latency, and CPU load using responsive **Chart.js** line graphs.
- **AI Anomaly Detection**: Employs a pre-trained **Random Forest** classification model to inspect traffic and predict anomalous behavior with confidence scores.
- **Dynamic Network Health Index**: Computes a holistic network health rating (0–100%) dynamically based on latency, packet loss, and CPU load.
- **Automated Incident Logging**: Tracks anomalies, timestamps, source IPs, severity levels, and automated AI diagnostic explanations.
- **Resilient Fallbacks**: Integrated dynamic feature alignment and polling failover to ensure uninterrupted monitoring streams.

---

## 🏗️ System Architecture

```text
├── app.py                         # Flask application backend & API endpoints
├── aimodel.py                     # Model training script (Random Forest)
├── testmodel.py                   # Standalone inference & verification script
├── traffic.py                     # Traffic simulation generator
├── traffic_model.pkl              # Serialized Scikit-Learn predictive model
├── synthetic_network_traffic.csv  # Training dataset
├── templates/
│   └── dashboard.html             # Web dashboard UI
├── static/
│   ├── dashboard.js               # Polling client & Chart.js renderer
│   └── style.css                  # Dark-mode dashboard styling
└── .gitignore                     # Git ignore file (excludes .venv, __pycache__)
