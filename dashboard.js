let trafficChart = null;
const maxPoints = 20;

const times = [];
const bandwidthData = [];
const latencyData = [];
const cpuData = [];
const events = [];

function setText(id, value) {
    const el = document.getElementById(id);
    if (el) el.textContent = value ?? "--";
}

function initializeChart() {
    const canvas = document.getElementById("trafficChart");
    if (!canvas) return;

    const ctx = canvas.getContext("2d");
    trafficChart = new Chart(ctx, {
        type: "line",
        data: {
            labels: times,
            datasets: [
                {
                    label: "Bandwidth (Mbps)",
                    data: bandwidthData,
                    borderColor: "#38bdf8",
                    backgroundColor: "rgba(56,189,248,0.08)",
                    borderWidth: 2,
                    tension: 0.35,
                    pointRadius: 0
                },
                {
                    label: "Latency (ms)",
                    data: latencyData,
                    borderColor: "#a78bfa",
                    backgroundColor: "rgba(167,139,250,0.08)",
                    borderWidth: 2,
                    tension: 0.35,
                    pointRadius: 0
                },
                {
                    label: "CPU (%)",
                    data: cpuData,
                    borderColor: "#f59e0b",
                    backgroundColor: "rgba(245,158,11,0.08)",
                    borderWidth: 2,
                    tension: 0.35,
                    pointRadius: 0
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            animation: false,
            plugins: {
                legend: {
                    labels: { color: "#94a3b8" }
                }
            },
            scales: {
                x: {
                    ticks: { color: "#475569" },
                    grid: { color: "#172033" }
                },
                y: {
                    ticks: { color: "#475569" },
                    grid: { color: "#172033" }
                }
            }
        }
    });
}

function updateChart(data) {
    if (!trafficChart) return;

    times.push(data.timestamp || new Date().toLocaleTimeString());
    bandwidthData.push(data.bandwidth ?? 0);
    latencyData.push(data.latency ?? 0);
    cpuData.push(data.cpu ?? 0);

    if (times.length > maxPoints) {
        times.shift();
        bandwidthData.shift();
        latencyData.shift();
        cpuData.shift();
    }

    trafficChart.update();
}

function updateDashboard(data) {
    const health = data.health ?? 100;
    setText("health", health);
    setText("healthScore", health + "/100");

    const healthBar = document.getElementById("healthBar");
    if (healthBar) healthBar.style.width = health + "%";

    setText("bandwidth", data.bandwidth);
    setText("latency", data.latency);
    setText("packetLoss", data.packet_loss);
    setText("connections", data.connections);

    const confidence = data.confidence ?? 95;
    setText("confidence", confidence + "%");
    setText("confidenceText", "AI Confidence: " + confidence + "%");

    const isAnomaly = String(data.prediction || "").toLowerCase() === "anomaly";

    // Status Banner
    const statusAlert = document.getElementById("statusAlert");
    const statusIcon = statusAlert ? statusAlert.querySelector(".status-icon") : null;
    if (statusAlert) {
        statusAlert.className = isAnomaly ? "status anomaly" : "status normal";
    }
    if (statusIcon) {
        statusIcon.textContent = isAnomaly ? "🚨" : "🟢";
    }
    setText("statusText", isAnomaly ? "NETWORK ANOMALY DETECTED" : "NETWORK OPERATING NORMALLY");

    // Prediction Badge
    const badge = document.getElementById("predictionBadge");
    if (badge) {
        badge.className = isAnomaly ? "prediction anomaly" : "prediction normal";
        badge.textContent = isAnomaly ? "🚨 ANOMALY" : "🟢 NORMAL";
    }

    // Threat Panel
    const noThreat = document.getElementById("noThreat");
    const alertPanel = document.getElementById("alertPanel");
    const threatStatus = document.getElementById("threatStatus");

    if (isAnomaly) {
        if (noThreat) noThreat.style.display = "none";
        if (alertPanel) alertPanel.classList.remove("hidden");
        if (threatStatus) {
            threatStatus.textContent = "● THREAT DETECTED";
            threatStatus.style.color = "#f87171";
        }
        setText("detectionStatus", "Threat Detected");
        setText("severity", data.severity || "HIGH");
        setText("alertBandwidth", (data.bandwidth ?? 0) + " Mbps");
        setText("alertLatency", (data.latency ?? 0) + " ms");
        setText("alertLoss", (data.packet_loss ?? 0) + "%");
        setText("alertConnections", data.connections ?? 0);

        addEvent(data);
    } else {
        if (noThreat) noThreat.style.display = "flex";
        if (alertPanel) alertPanel.classList.add("hidden");
        if (threatStatus) {
            threatStatus.textContent = "● MONITORING";
            threatStatus.style.color = "#4ade80";
        }
        setText("detectionStatus", "Monitoring");
    }

    updateChart(data);
}

function addEvent(data) {
    const timestamp = data.timestamp || new Date().toLocaleTimeString();
    if (events.length > 0 && events[0].time === timestamp) return;

    events.unshift({
        time: timestamp,
        endpoint: data.endpoint || "Core-Gateway-01",
        ip: data.source_ip || "10.0.0.1",
        anomalyType: data.anomaly_type || "Traffic Surge",
        severity: data.severity || "HIGH",
        confidence: data.confidence || 95
    });

    if (events.length > 8) events.pop();
    renderEvents();
}

function renderEvents() {
    const container = document.getElementById("events");
    setText("eventCount", events.length);
    if (!container) return;

    if (events.length === 0) {
        container.innerHTML = '<div class="empty">No anomalies detected yet.</div>';
        return;
    }

    container.innerHTML = "";
    events.forEach(event => {
        const item = document.createElement("div");
        item.className = "event";
        item.innerHTML = `
            <div class="event-icon">🚨</div>
            <div class="event-info">
                <strong>${event.endpoint}</strong>
                <span>${event.ip} • ${event.anomalyType} • Severity: ${event.severity}</span>
            </div>
            <div class="event-confidence">${event.confidence}%</div>
        `;
        container.appendChild(item);
    });
}

async function fetchTraffic() {
    const endpoints = ["/traffic_api", "/api/traffic"];
    for (const url of endpoints) {
        try {
            const res = await fetch(url);
            if (res.ok) {
                const data = await res.json();
                updateDashboard(data);
                return;
            }
        } catch (e) {
            // Check next endpoint
        }
    }
}

window.addEventListener("DOMContentLoaded", () => {
    initializeChart();
    fetchTraffic();
    setInterval(fetchTraffic, 2000);
});