
import pandas as pd
import json
import joblib
from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, roc_auc_score

# Load dataset
df = pd.read_csv("ml/training_pipeline/historical_vehicle_data.csv")

# Features and target
X = df.drop("failure", axis=1)
y = df["failure"]

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model
model = RandomForestClassifier(
    n_estimators=150,
    max_depth=10,
    random_state=42
)

model.fit(X_train, y_train)

# Predictions
y_pred = model.predict(X_test)
y_proba = model.predict_proba(X_test)[:, 1]

# Metrics
metrics = {
    "accuracy": float(round(accuracy_score(y_test, y_pred), 4)),
    "precision": float(round(precision_score(y_test, y_pred), 4)),
    "recall": float(round(recall_score(y_test, y_pred), 4)),
    "roc_auc": float(round(roc_auc_score(y_test, y_proba), 4))
}

# Save model
model_path = "ml/models/failure_model_v1.pkl"
joblib.dump(model, model_path)

# Save metrics
metrics_path = "ml/models/metrics_v1.json"
with open(metrics_path, "w") as f:
    json.dump(metrics, f, indent=4)

print("Model training complete ✅")
print("Saved model to:", model_path)
print("Saved metrics to:", metrics_path)
print("Metrics:", metrics)
