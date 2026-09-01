import random
import csv
from datetime import datetime, timedelta

# ============================================================
# 1. CREATE 50 VIRTUAL ENDPOINT DEVICES
# ============================================================

endpoints = []

device_types = {
    "Desktop": 10,
    "Laptop": 10,
    "Smartphone": 10,
    "Server": 5,
    "IP Camera": 5,
    "Printer": 3,
    "IoT Sensor": 7
}

ip_number = 10

for device_type, count in device_types.items():

    for i in range(1, count + 1):

        endpoint_name = f"{device_type.replace(' ', '-')}-{i:02d}"

        endpoints.append({
            "name": endpoint_name,
            "type": device_type,
            "ip": f"192.168.1.{ip_number}"
        })

        ip_number += 1


# ============================================================
# 2. NORMAL TRAFFIC PROFILES
# ============================================================

def generate_normal(endpoint):

    device_type = endpoint["type"]

    # -------------------------
    # Desktop
    # -------------------------
    if device_type == "Desktop":

        traffic_rate = random.uniform(100, 1000)
        connections = random.randint(5, 50)
        latency = random.uniform(10, 60)
        packet_loss = random.uniform(0, 2)
        cpu = random.uniform(10, 70)

    # -------------------------
    # Laptop
    # -------------------------
    elif device_type == "Laptop":

        traffic_rate = random.uniform(80, 800)
        connections = random.randint(5, 40)
        latency = random.uniform(15, 70)
        packet_loss = random.uniform(0, 2)
        cpu = random.uniform(10, 70)

    # -------------------------
    # Smartphone
    # -------------------------
    elif device_type == "Smartphone":

        traffic_rate = random.uniform(50, 500)
        connections = random.randint(3, 30)
        latency = random.uniform(20, 100)
        packet_loss = random.uniform(0, 3)
        cpu = random.uniform(10, 60)

    # -------------------------
    # Server
    # -------------------------
    elif device_type == "Server":

        traffic_rate = random.uniform(2000, 15000)
        connections = random.randint(50, 500)
        latency = random.uniform(5, 40)
        packet_loss = random.uniform(0, 2)
        cpu = random.uniform(20, 80)

    # -------------------------
    # IP Camera
    # -------------------------
    elif device_type == "IP Camera":

        traffic_rate = random.uniform(500, 4000)
        connections = random.randint(2, 20)
        latency = random.uniform(20, 100)
        packet_loss = random.uniform(0, 3)
        cpu = random.uniform(20, 70)

    # -------------------------
    # Printer
    # -------------------------
    elif device_type == "Printer":

        traffic_rate = random.uniform(10, 200)
        connections = random.randint(1, 10)
        latency = random.uniform(20, 100)
        packet_loss = random.uniform(0, 3)
        cpu = random.uniform(5, 40)

    # -------------------------
    # IoT Sensor
    # -------------------------
    elif device_type == "IoT Sensor":

        traffic_rate = random.uniform(5, 150)
        connections = random.randint(1, 8)
        latency = random.uniform(20, 120)
        packet_loss = random.uniform(0, 4)
        cpu = random.uniform(5, 50)

    else:

        traffic_rate = random.uniform(50, 500)
        connections = random.randint(5, 30)
        latency = random.uniform(10, 80)
        packet_loss = random.uniform(0, 2)
        cpu = random.uniform(10, 70)


    # Packet count is related to traffic rate
    packet_count = int(
        traffic_rate * random.uniform(0.8, 1.2)
    )

    # Bandwidth is related to traffic
    bandwidth = traffic_rate * random.uniform(0.8, 1.2)


    return {

        "traffic_rate": round(traffic_rate, 2),

        "bandwidth": round(bandwidth, 2),

        "packet_count": packet_count,

        "connections": connections,

        "latency": round(latency, 2),

        "packet_loss": round(packet_loss, 2),

        "cpu_utilization": round(cpu, 2),

        "label": "Normal",

        "anomaly_type": "None"
    }


# ============================================================
# 3. GENERATE DIFFERENT ANOMALIES
# ============================================================

def generate_anomaly(endpoint):

    # First create normal traffic
    data = generate_normal(endpoint)

    anomaly_type = random.choice([

        "Traffic Spike",

        "Excessive Connections",

        "High Latency",

        "High Packet Loss",

        "High CPU",

        "Combined Anomaly"

    ])


    # ========================================================
    # TRAFFIC SPIKE
    # ========================================================

    if anomaly_type == "Traffic Spike":

        multiplier = random.uniform(5, 15)

        data["traffic_rate"] *= multiplier

        data["bandwidth"] *= multiplier

        data["packet_count"] *= random.randint(5, 15)


    # ========================================================
    # EXCESSIVE CONNECTIONS
    # ========================================================

    elif anomaly_type == "Excessive Connections":

        data["connections"] *= random.randint(10, 30)


    # ========================================================
    # HIGH LATENCY
    # ========================================================

    elif anomaly_type == "High Latency":

        data["latency"] *= random.uniform(5, 10)


    # ========================================================
    # HIGH PACKET LOSS
    # ========================================================

    elif anomaly_type == "High Packet Loss":

        data["packet_loss"] = random.uniform(10, 40)


    # ========================================================
    # HIGH CPU
    # ========================================================

    elif anomaly_type == "High CPU":

        data["cpu_utilization"] = random.uniform(90, 100)


    # ========================================================
    # COMBINED ANOMALY
    # ========================================================

    elif anomaly_type == "Combined Anomaly":

        data["traffic_rate"] *= random.uniform(5, 10)

        data["bandwidth"] *= random.uniform(5, 10)

        data["packet_count"] *= random.randint(5, 10)

        data["connections"] *= random.randint(10, 25)

        data["latency"] *= random.uniform(5, 10)

        data["packet_loss"] = random.uniform(10, 30)

        data["cpu_utilization"] = random.uniform(80, 100)


    # Make sure values are clean

    data["traffic_rate"] = round(
        data["traffic_rate"], 2
    )

    data["bandwidth"] = round(
        data["bandwidth"], 2
    )

    data["packet_count"] = int(
        data["packet_count"]
    )

    data["connections"] = int(
        data["connections"]
    )

    data["latency"] = round(
        data["latency"], 2
    )

    data["packet_loss"] = round(
        data["packet_loss"], 2
    )

    data["cpu_utilization"] = round(
        data["cpu_utilization"], 2
    )

    data["label"] = "Anomaly"

    data["anomaly_type"] = anomaly_type


    return data


# ============================================================
# 4. GENERATE DATASET
# ============================================================

TOTAL_RECORDS = 20000

OUTPUT_FILE = "synthetic_network_traffic.csv"

start_time = datetime.now()


fieldnames = [

    "timestamp",

    "endpoint_name",

    "endpoint_type",

    "source_ip",

    "destination_ip",

    "protocol",

    "traffic_rate",

    "bandwidth",

    "packet_count",

    "connections",

    "latency",

    "packet_loss",

    "cpu_utilization",

    "label",

    "anomaly_type"

]


destination_ips = [

    "192.168.1.1",

    "192.168.1.20",

    "192.168.1.50",

    "192.168.1.100",

    "8.8.8.8"

]


protocols = [

    "TCP",

    "UDP",

    "ICMP"

]


# ============================================================
# 5. WRITE CSV
# ============================================================

with open(
    OUTPUT_FILE,
    "w",
    newline=""
) as file:

    writer = csv.DictWriter(
        file,
        fieldnames=fieldnames
    )

    writer.writeheader()


    for i in range(TOTAL_RECORDS):

        # Pick random endpoint

        endpoint = random.choice(
            endpoints
        )


        # 80% normal
        # 20% anomaly

        if random.random() < 0.80:

            traffic = generate_normal(
                endpoint
            )

        else:

            traffic = generate_anomaly(
                endpoint
            )


        row = {

            "timestamp":
            (
                start_time +
                timedelta(seconds=i)
            ).strftime(
                "%Y-%m-%d %H:%M:%S"
            ),

            "endpoint_name":
            endpoint["name"],

            "endpoint_type":
            endpoint["type"],

            "source_ip":
            endpoint["ip"],

            "destination_ip":
            random.choice(
                destination_ips
            ),

            "protocol":
            random.choice(
                protocols
            ),

            **traffic

        }


        writer.writerow(row)


# ============================================================
# 6. DISPLAY RESULT
# ============================================================

print()
print("======================================")
print(" SYNTHETIC NETWORK TRAFFIC GENERATED ")
print("======================================")

print(
    f"Total Endpoints : {len(endpoints)}"
)

print(
    f"Total Records   : {TOTAL_RECORDS}"
)

print(
    f"Output File     : {OUTPUT_FILE}"
)

print()

print("Endpoint Types:")

for device_type, count in device_types.items():

    print(
        f"  {device_type:<15} : {count}"
    )

print()

print("Traffic Distribution:")

print("  Normal   : ~80%")

print("  Anomaly  : ~20%")

print()

print("Anomaly Types:")

print("  - Traffic Spike")

print("  - Excessive Connections")

print("  - High Latency")

print("  - High Packet Loss")

print("  - High CPU")

print("  - Combined Anomaly")

print()

print("======================================")