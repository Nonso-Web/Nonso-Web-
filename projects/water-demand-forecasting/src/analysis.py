"""Baseline monthly water-demand forecasting using synthetic demonstration data."""
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error

ROOT = Path(__file__).resolve().parents[1]
data = pd.read_csv(ROOT / "data" / "monthly_water_demand.csv", parse_dates=["date"])
data = data.sort_values("date").reset_index(drop=True)
data["t"] = np.arange(len(data))
month = data["date"].dt.month
data["month_sin"] = np.sin(2 * np.pi * month / 12)
data["month_cos"] = np.cos(2 * np.pi * month / 12)

split = len(data) - 12
train, test = data.iloc[:split], data.iloc[split:]
features = ["t", "month_sin", "month_cos"]
model = LinearRegression().fit(train[features], train["demand_ml"])
test = test.copy()
test["prediction"] = model.predict(test[features])
test["seasonal_naive"] = data["demand_ml"].iloc[split-12:split].to_numpy()

for name, pred in [("Regression", test["prediction"]), ("Seasonal-naive", test["seasonal_naive"])]:
    mae = mean_absolute_error(test["demand_ml"], pred)
    rmse = np.sqrt(mean_squared_error(test["demand_ml"], pred))
    print(f"{name}: MAE={mae:.3f} ML, RMSE={rmse:.3f} ML")

plt.figure(figsize=(10, 5))
plt.plot(train["date"], train["demand_ml"], label="Training observations")
plt.plot(test["date"], test["demand_ml"], marker="o", label="Actual test demand")
plt.plot(test["date"], test["prediction"], marker="x", label="Regression forecast")
plt.xlabel("Month")
plt.ylabel("Demand (ML)")
plt.title("Monthly water demand: synthetic data and baseline forecast")
plt.legend()
plt.tight_layout()
plt.show()
