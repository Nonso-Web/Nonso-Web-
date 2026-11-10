# Construction Carbon Estimator

A small, reproducible demonstration of how construction material quantities can be combined with embodied-carbon factors to estimate an illustrative project-level carbon total.

## What it does
- Reads a sample bill of quantities.
- Multiplies material quantities by example emission factors.
- Summarises estimated emissions by material and category.
- Produces a simple chart to support interpretation.

## Dataset and factors
The bill of quantities in `data/material_quantities.csv` and the factors in `data/illustrative_emission_factors.csv` are synthetic/illustrative. They are not extracted from Environmental Product Declarations (EPDs), verified lifecycle databases, supplier declarations or a real construction project.

## Run
```bash
python -m pip install -r requirements.txt
python src/analysis.py
```
Or open `notebooks/construction_carbon_estimator.ipynb` in Jupyter.

## Calculation
`estimated_kgco2e = quantity × illustrative_factor`

The unit of each factor must match the unit of its material quantity. The sample dataset uses kgCO2e per tonne for cement, steel and aggregate, and kgCO2e per cubic metre for ready-mix concrete.

## Important limitations
This is an educational calculator, not a whole-life carbon assessment, verified carbon report, procurement recommendation or regulatory submission. Before any real use, replace all example factors with current, geographically and technologically appropriate EPD or recognised database values; check system boundaries, declared units, transport, waste, reuse, lifecycle modules and project-specific quantities with a competent professional.
