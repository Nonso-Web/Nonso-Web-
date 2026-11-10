# Monthly Water Demand Forecasting

A reproducible baseline time-series project exploring monthly water demand using a clearly labelled synthetic dataset.

## Objectives
- Inspect monthly demand patterns and seasonality.
- Establish a simple seasonal-naive benchmark.
- Compare a linear regression baseline using calendar features.
- Visualise actual and predicted demand.

## Dataset
`data/monthly_water_demand.csv` contains 60 synthetic monthly observations (2020–2024). Demand values are simulated for demonstration and are not measurements from a real water utility.

## Run
```bash
python -m pip install -r requirements.txt
python src/analysis.py
```

Run the notebook with Jupyter:
```bash
jupyter notebook notebooks/water_demand_forecasting.ipynb
```

## Method
The final 12 months are held out as a test period. A linear regression model uses month-of-year sine/cosine terms and a time trend. The benchmark predicts each test month using the value from 12 months earlier. MAE and RMSE are reported.

## Limitations
This is an educational baseline, not an operational forecasting system. It does not model weather, tariffs, population, leakage, restrictions, industrial demand or special events. Results are not field-validated and should not inform operational or investment decisions.
