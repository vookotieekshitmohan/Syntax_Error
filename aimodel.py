import importlib

try:
    pd = importlib.import_module("pandas")
except ImportError as exc:
    raise ImportError(
        "pandas is required. Install it with: /usr/local/bin/python3 -m pip install pandas"
    ) from exc

try:
    sklearn_model_selection = importlib.import_module("sklearn.model_selection")
    sklearn_ensemble = importlib.import_module("sklearn.ensemble")
    sklearn_metrics = importlib.import_module("sklearn.metrics")
    
    train_test_split = sklearn_model_selection.train_test_split
    RandomForestClassifier = sklearn_ensemble.RandomForestClassifier
    classification_report = sklearn_metrics.classification_report
    confusion_matrix = sklearn_metrics.confusion_matrix
    accuracy_score = sklearn_metrics.accuracy_score
except ImportError as exc:
    raise ImportError(
        "scikit-learn is required. Install it with: /usr/local/bin/python3 -m pip install scikit-learn"
    ) from exc

try:
    joblib = importlib.import_module("joblib")
except ImportError as exc:
    raise ImportError(
        "joblib is required. Install it with: /usr/local/bin/python3 -m pip install joblib"
    ) from exc

# ---------------------------------------------------
# 1. Load and clean column headers
# ---------------------------------------------------
df = pd.read_csv('synthetic_network_traffic.csv')

# Strip any leading/trailing spaces from column headers
df.columns = df.columns.str.strip()

print(f"Loaded {len(df)} rows")
print("Available columns:", df.columns.tolist())

# Detect the target column name automatically
possible_labels = ['label', 'status', 'anomaly', 'traffic_type', 'attack_type', 'severity']
target_col = next((col for col in possible_labels if col in df.columns), None)

if target_col is None:
    # If not found in common names, fallback to the last column
    target_col = df.columns[-1]

print(f"Using '{target_col}' as target label column.")
print(df[target_col].value_counts())

# ---------------------------------------------------
# 2. Clean the numeric data (fix impossible values)
# ---------------------------------------------------
if 'cpu_util_pct' in df.columns:
    df['cpu_util_pct'] = df['cpu_util_pct'].clip(0, 100)
if 'latency_ms' in df.columns:
    df['latency_ms'] = df['latency_ms'].clip(lower=0)
if 'bandwidth_mbps' in df.columns:
    df['bandwidth_mbps'] = df['bandwidth_mbps'].clip(lower=0)
if 'packet_loss_pct' in df.columns:
    df['packet_loss_pct'] = df['packet_loss_pct'].clip(0, 100)
if 'connections' in df.columns:
    df['connections'] = df['connections'].clip(lower=0)
if 'packet_count' in df.columns:
    df['packet_count'] = df['packet_count'].clip(lower=0)

# ---------------------------------------------------
# 3. Select Numeric Features (X) and Target (y)
# ---------------------------------------------------
# Columns to exclude from training features (identifiers and target)
non_feature_cols = [
    'timestamp', 'endpoint_name', 'endpoint_type', 
    'source_ip', 'destination_ip', 'protocol', target_col
]

feature_cols = [c for c in df.columns if c not in non_feature_cols and pd.api.types.is_numeric_dtype(df[c])]

X = df[feature_cols]
y = df[target_col]

print("Training features:", feature_cols)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# ---------------------------------------------------
# 4. Train the model
# ---------------------------------------------------
model = RandomForestClassifier(
    n_estimators=200,
    max_depth=10,
    class_weight='balanced',
    random_state=42
)
model.fit(X_train, y_train)

# ---------------------------------------------------
# 5. Evaluate the model
# ---------------------------------------------------
y_pred = model.predict(X_test)
print("\nModel Accuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred))
print("\nConfusion Matrix:\n", confusion_matrix(y_test, y_pred))

# ---------------------------------------------------
# 6. Save the trained model
# ---------------------------------------------------
joblib.dump(model, 'traffic_model.pkl')
print("\nModel successfully saved to traffic_model.pkl")