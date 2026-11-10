from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (accuracy_score, precision_score, recall_score,
                             f1_score, confusion_matrix, classification_report,
                             ConfusionMatrixDisplay)

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "pump_sensor_data.csv"
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)

df = pd.read_csv(DATA)
target = "failure"
features = ["vibration_mm_s", "temperature_c", "pressure_bar",
            "runtime_hours", "months_since_service", "flow_rate_l_min"]
if df[features + [target]].isna().any().any():
    raise ValueError("Dataset contains missing model values")
if not set(df[target].unique()).issubset({0, 1}):
    raise ValueError("Target must be binary (0 or 1)")

X, y = df[features], df[target]
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y
)
model = Pipeline([
    ("scale", StandardScaler()),
    ("classifier", LogisticRegression(max_iter=1000, class_weight="balanced"))
])
model.fit(X_train, y_train)
pred = model.predict(X_test)

metrics = {
    "accuracy": accuracy_score(y_test, pred),
    "precision": precision_score(y_test, pred, zero_division=0),
    "recall": recall_score(y_test, pred, zero_division=0),
    "f1": f1_score(y_test, pred, zero_division=0),
}
pd.DataFrame([metrics]).to_csv(OUT / "test_metrics.csv", index=False)
(OUT / "classification_report.txt").write_text(
    classification_report(y_test, pred, zero_division=0), encoding="utf-8"
)
ConfusionMatrixDisplay(confusion_matrix(y_test, pred), display_labels=["No failure", "Failure"]).plot()
plt.title("Synthetic test-set confusion matrix")
plt.tight_layout()
plt.savefig(OUT / "confusion_matrix.png", dpi=150)
plt.close()

importance = pd.Series(
    model.named_steps["classifier"].coef_[0], index=features
).sort_values()
importance.to_csv(OUT / "scaled_model_coefficients.csv", header=["coefficient"])
importance.plot(kind="barh", figsize=(8, 5), title="Logistic regression coefficients (scaled features)")
plt.xlabel("Coefficient")
plt.tight_layout()
plt.savefig(OUT / "model_coefficients.png", dpi=150)
plt.close()

print("Synthetic dataset rows:", len(df))
print("Training rows:", len(X_train), "| Test rows:", len(X_test))
print("Test metrics:", metrics)
print("\n", classification_report(y_test, pred, zero_division=0))
print("Outputs saved to:", OUT)
