from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "fictional_procurement.csv"
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)

df = pd.read_csv(DATA, parse_dates=["award_date"])
required = {"record_id", "financial_year", "department", "category", "supplier",
            "tender_method", "contract_value_gbp", "award_date",
            "days_to_award", "number_of_bids"}
missing = required - set(df.columns)
if missing:
    raise ValueError(f"Missing required columns: {sorted(missing)}")
if df["record_id"].duplicated().any():
    raise ValueError("record_id values must be unique")
if (df["contract_value_gbp"] < 0).any():
    raise ValueError("Contract values must be non-negative")

total_spend = df["contract_value_gbp"].sum()
by_department = (df.groupby("department")["contract_value_gbp"]
                 .agg(contract_count="count", total_value="sum", mean_value="mean")
                 .sort_values("total_value", ascending=False).reset_index())
by_category = (df.groupby("category")["contract_value_gbp"]
               .agg(contract_count="count", total_value="sum")
               .sort_values("total_value", ascending=False).reset_index())
by_supplier = (df.groupby("supplier")["contract_value_gbp"]
               .agg(contract_count="count", total_value="sum")
               .sort_values("total_value", ascending=False).reset_index())
by_supplier["share_of_total_pct"] = by_supplier["total_value"] / total_spend * 100
shares = by_supplier["total_value"] / total_spend
hhi = float((shares ** 2).sum() * 10000) if total_spend else 0.0

by_method = (df.groupby("tender_method")
             .agg(contract_count=("record_id", "count"),
                  total_value_gbp=("contract_value_gbp", "sum"),
                  median_bids=("number_of_bids", "median"))
             .reset_index())
q1, q3 = df["contract_value_gbp"].quantile([0.25, 0.75])
iqr = q3 - q1
upper = q3 + 1.5 * iqr
outliers = df.loc[df["contract_value_gbp"] > upper].copy()
outliers["review_flag"] = "Above IQR upper bound; investigate context, not an allegation"

by_department.to_csv(OUT / "spend_by_department.csv", index=False)
by_category.to_csv(OUT / "spend_by_category.csv", index=False)
by_supplier.to_csv(OUT / "spend_by_fictional_supplier.csv", index=False)
by_method.to_csv(OUT / "tender_method_summary.csv", index=False)
outliers.to_csv(OUT / "high_value_review_candidates.csv", index=False)

fig, ax = plt.subplots(figsize=(9, 4))
by_department.sort_values("total_value").plot(
    x="department", y="total_value", kind="barh", legend=False, ax=ax)
ax.set(title="Fictional contract value by department",
       xlabel="Contract value (GBP, illustrative)", ylabel="")
fig.tight_layout()
fig.savefig(OUT / "spend_by_department.png", dpi=150)
plt.close(fig)

fig, ax = plt.subplots(figsize=(9, 4))
by_supplier.sort_values("total_value").plot(
    x="supplier", y="total_value", kind="barh", legend=False, ax=ax)
ax.set(title="Fictional supplier contract values",
       xlabel="Contract value (GBP, illustrative)", ylabel="")
fig.tight_layout()
fig.savefig(OUT / "spend_by_supplier.png", dpi=150)
plt.close(fig)

fig, ax = plt.subplots(figsize=(7, 4))
by_method.set_index("tender_method")["contract_count"].plot(kind="bar", ax=ax)
ax.set(title="Contracts by fictional tender method",
       xlabel="Tender method", ylabel="Contract count")
fig.tight_layout()
fig.savefig(OUT / "tender_method_counts.png", dpi=150)
plt.close(fig)

print(f"Records: {len(df)} | Total fictional spend: £{total_spend:,.2f}")
print(f"Supplier HHI (illustrative dataset only): {hhi:.1f}")
print("\nDepartment summary:\n", by_department.to_string(index=False))
print("\nTender method summary:\n", by_method.to_string(index=False))
print(f"\nIQR review candidates: {len(outliers)} (not allegations)")
print("Outputs saved to:", OUT)
