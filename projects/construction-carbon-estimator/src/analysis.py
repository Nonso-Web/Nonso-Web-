"""Illustrative construction material carbon estimator.

All quantities and emission factors are demonstration values, not verified project data.
"""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
quantities = pd.read_csv(ROOT / "data" / "material_quantities.csv")
factors = pd.read_csv(ROOT / "data" / "illustrative_emission_factors.csv")

df = quantities.merge(
    factors, on="material", how="left",
    suffixes=("_quantity", "_factor"), validate="one_to_one"
)
if df["illustrative_kgco2e_per_unit"].isna().any():
    missing = df.loc[df["illustrative_kgco2e_per_unit"].isna(), "material"].tolist()
    raise ValueError(f"Missing emission factors for: {missing}")
if df["unit_quantity"].ne(df["unit_factor"]).any():
    raise ValueError("Quantity and emission-factor units must match.")

df["estimated_kgco2e"] = df["quantity"] * df["illustrative_kgco2e_per_unit"]
print("Illustrative emissions by material (kgCO2e):")
print(df[["material", "quantity", "unit_quantity", "estimated_kgco2e"]].to_string(index=False))
print(f"\nIllustrative total: {df['estimated_kgco2e'].sum():,.0f} kgCO2e")
print("\nReminder: factors are placeholders, not verified EPD/database values.")

ax = df.set_index("material")["estimated_kgco2e"].sort_values().plot(kind="barh", figsize=(8, 4))
ax.set_xlabel("Illustrative emissions (kgCO2e)")
ax.set_title("Material contribution (demonstration data)")
plt.tight_layout()
plt.show()
