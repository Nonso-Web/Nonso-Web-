# Pump Failure Classification

A supervised machine-learning demonstration that predicts a binary pump-failure label from a **synthetic** sensor and operating-history dataset.

## Dataset

`data/pump_sensor_data.csv` contains 180 generated pump observations with vibration, temperature, pressure, runtime, months since service, flow rate and a binary `failure` label.

The records and labels are entirely synthetic. The label is generated from simple illustrative rules and is not based on real failure events, engineering standards or a validated failure mechanism. This creates a learnable demonstration dataset, not evidence of real predictive performance.

## Run

```bash
python -m pip install -r requirements.txt
python src/train_model.py
```

The script uses a stratified train/test split, a standardised logistic-regression baseline and reports accuracy, precision, recall, F1 and a confusion matrix. Outputs are saved in `outputs/`.

## Important limitations

- Synthetic data and rule-generated labels can produce misleadingly optimistic metrics.
- The model is not calibrated or validated for any real pump, site or operating environment.
- It must not be used for maintenance scheduling, safety decisions, asset operation or failure prevention.
- Real deployment would require representative labelled field data, leakage checks, temporal or asset-level validation, calibration, monitoring, engineering review and documented risk controls.
- Metrics describe only this generated sample and split.
