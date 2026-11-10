"""Exploratory screening of synthetic water-quality sample data."""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
df = pd.read_csv(ROOT / "data" / "water_quality_samples.csv")
print("Summary statistics:")
print(df[["ph", "turbidity_ntu", "dissolved_oxygen_mg_l", "nitrate_mg_l"]].describe())

# Illustrative screening limits only; not regulatory standards.
df["ph_flag"] = ~df["ph"].between(6.5, 8.5)
df["turbidity_flag"] = df["turbidity_ntu"] > 3.0
df["nitrate_flag"] = df["nitrate_mg_l"] > 5.0
print("\nIllustrative screening flags by sample:")
print(df[["sample_id", "site", "ph_flag", "turbidity_flag", "nitrate_flag"]].to_string(index=False))

ax = df.groupby("site")["turbidity_ntu"].mean().plot(kind="bar", figsize=(8, 4))
ax.set_ylabel("Mean turbidity (NTU)")
ax.set_title("Synthetic sample turbidity by site")
plt.tight_layout()
plt.show()
