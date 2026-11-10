# Water Quality Monitoring and Screening

An exploratory data-analysis project for a synthetic water-quality dataset. It demonstrates data cleaning, descriptive statistics, visualisation and simple threshold-based screening.

## Dataset
`data/water_quality_samples.csv` contains illustrative sample readings for pH, turbidity, dissolved oxygen and nitrate. All records are synthetic and are not from a real water body or laboratory.

## Run
```bash
python -m pip install -r requirements.txt
python src/analysis.py
```

## Important interpretation note
The screening values in the script are example thresholds for demonstrating code only. Applicable standards depend on jurisdiction, water use, sampling method and current regulations. This project is not a compliance assessment or a substitute for accredited laboratory testing.
