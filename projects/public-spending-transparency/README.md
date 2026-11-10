# Public Spending Transparency: Procurement Data Exploration

An exploratory data analytics project using a **fictional, synthetic procurement dataset**. It demonstrates how public procurement records can be structured and examined for spending patterns, supplier concentration, tender-method mix and unusual values that may warrant further checking.

## Dataset

`data/fictional_procurement.csv` contains 120 generated contract-award records. Department names, supplier names, categories, values, dates and bid counts are all invented. Currency values are illustrative GBP amounts, not real contracts or public expenditure.

## Run

```bash
python -m pip install -r requirements.txt
python src/analyse_procurement.py
```

Outputs are saved to `outputs/`.

## Analysis

- Total and average contract value by department and category
- Spend distribution by fictional supplier
- Supplier concentration using share of total value and a Herfindahl–Hirschman Index (HHI)
- Tender-method distribution and bid-count summaries
- Exploratory review of unusually high contract values using the IQR rule

## Interpretation and safeguards

An outlier is a statistical observation for review, not evidence of fraud, corruption, overpricing or wrongdoing. Supplier concentration can arise for many reasons and is not, by itself, evidence of improper conduct. Direct awards and low bid counts may have lawful explanations depending on the applicable framework and context.

This project contains no real government, council, department, supplier or procurement records. It must not be used to make allegations or identify real organisations. Real procurement analysis requires verified source records, consistent contract definitions, appropriate treatment of frameworks and amendments, inflation and currency context, procurement-law expertise, and an auditable methodology.
