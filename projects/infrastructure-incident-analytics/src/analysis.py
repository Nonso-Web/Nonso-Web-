from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "infrastructure_incidents.csv"
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)

df = pd.read_csv(DATA, parse_dates=["date_reported"])
required = {"incident_id", "date_reported", "asset_type", "severity",
            "response_time_hours", "repair_time_hours", "status",
            "district", "coord_x", "coord_y"}
missing = required - set(df.columns)
if missing:
    raise ValueError(f"Missing required columns: {sorted(missing)}")
if df["incident_id"].duplicated().any():
    raise ValueError("incident_id values must be unique")
if (df[["response_time_hours", "repair_time_hours"]] < 0).any().any():
    raise ValueError("Durations must be non-negative")

monthly = (df.set_index("date_reported").resample("MS")
           .size().rename("incident_count").reset_index())
by_asset = (df.groupby("asset_type").size().rename("incident_count")
            .sort_values(ascending=False).reset_index())
by_severity = (df.groupby("severity")
               .agg(incident_count=("incident_id", "count"),
                    median_response_hours=("response_time_hours", "median"),
                    median_repair_hours=("repair_time_hours", "median"))
               .reset_index())
district_summary = (df.groupby("district").size()
                    .rename("incident_count").reset_index())

monthly.to_csv(OUT / "monthly_incidents.csv", index=False)
by_asset.to_csv(OUT / "incidents_by_asset.csv", index=False)
by_severity.to_csv(OUT / "severity_summary.csv", index=False)
district_summary.to_csv(OUT / "incidents_by_fictional_district.csv", index=False)

fig, ax = plt.subplots(figsize=(9, 4))
by_asset.sort_values("incident_count").plot(
    x="asset_type", y="incident_count", kind="barh", legend=False, ax=ax)
ax.set(title="Synthetic incidents by asset type", xlabel="Incident count", ylabel="")
fig.tight_layout()
fig.savefig(OUT / "incidents_by_asset.png", dpi=150)
plt.close(fig)

fig, ax = plt.subplots(figsize=(9, 4))
monthly.plot(x="date_reported", y="incident_count", ax=ax, legend=False)
ax.set(title="Monthly synthetic incident counts", xlabel="Month", ylabel="Incidents")
fig.tight_layout()
fig.savefig(OUT / "monthly_incidents.png", dpi=150)
plt.close(fig)

fig, ax = plt.subplots(figsize=(7, 5))
for severity, group in df.groupby("severity"):
    ax.scatter(group["coord_x"], group["coord_y"], label=severity, alpha=0.75)
ax.set(title="Fictional coordinate-plane view (not a map)",
       xlabel="Synthetic X position", ylabel="Synthetic Y position")
ax.legend(title="Severity")
fig.tight_layout()
fig.savefig(OUT / "fictional_coordinate_plot.png", dpi=150)
plt.close(fig)

print(f"Loaded {len(df)} synthetic incidents")
print("\nBy asset type:\n", by_asset.to_string(index=False))
print("\nBy severity:\n", by_severity.to_string(index=False))
print(f"\nOutputs saved to: {OUT}")
