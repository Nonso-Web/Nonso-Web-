# Infrastructure Incident Analytics

An exploratory Python project for analysing a **synthetic** infrastructure incident register. It demonstrates data cleaning, incident trend analysis, response and repair time summaries, and a simple spatial-style view.

## Dataset

`data/infrastructure_incidents.csv` contains 72 generated records covering 2024–2029. The dataset includes:
- incident date, asset type and severity
- response and repair durations in hours
- status and fictional district labels
- `coord_x` and `coord_y`: fictional coordinate-plane positions, **not GPS coordinates or real locations**

No real council, utility, road, water network, asset, incident or service record is represented.

## Run

```bash
python -m pip install -r requirements.txt
python src/analysis.py
```

The script writes summary CSV files and charts to `outputs/`.

## Questions explored

1. Which asset categories account for the most reported incidents?
2. How does incident volume vary over time?
3. How do response and repair durations vary by severity?
4. What does the distribution of fictional incident points look like?

## Limitations

This is a portfolio demonstration using generated data. It does not establish actual infrastructure performance, service quality, risk, geographic patterns or causes. The coordinate plot is not a map. The analysis is not an operational prioritisation tool and must not be used for safety, maintenance or investment decisions. Real-world use would require validated records, clear definitions, missing-data checks, appropriate privacy controls and domain review.
