# Financial Performance Dashboard

An end-to-end financial performance analysis using Python, SQL, Excel and Power BI. The project explores revenue, discounts, cost of goods sold, profit and margin across products, countries, segments and months.

## Business questions
- How are sales and profit trending over time?
- Which products, countries and customer segments contribute most to revenue and profit?
- How do discounts relate to sales and profitability?
- Which areas have low or negative profit margins?
- Where should a business investigate pricing or cost improvements?

## Dataset and attribution
This project uses Microsoft's **Financial Sample** workbook, a fictional demonstration dataset commonly used in Power BI learning materials. It is not audited financial data and does not represent an actual company's results.

Download source: [Microsoft Financial Sample workbook](https://go.microsoft.com/fwlink/?LinkID=521962). Save the workbook as `data/Financial Sample.xlsx`.

## Run locally
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
pip install -r requirements.txt
python src/analyze.py
```

The script reads the workbook and creates cleaned CSV and Excel analysis outputs in `outputs/`.

## Repository structure
- `src/analyze.py` — cleaning, KPI calculations and exports.
- `sql/analysis.sql` — reusable business analysis queries.
- `powerbi/README.md` — model setup, DAX measures and report layout.
- `data/` — place the downloaded source workbook here.
- `outputs/` — generated analysis files; excluded from Git.

## Metric definitions
- **Net sales:** gross sales minus discounts.
- **Profit margin:** profit divided by net sales.
- **Discount rate:** discounts divided by gross sales.
- **Profit:** net sales minus cost of goods sold (as supplied by the sample).

The script checks the identity between calculated net sales and the source `Sales` field, allowing small rounding differences.

## Limitations
This is a fictional teaching dataset. Treat all insights as practice analysis, not investment advice or real company financial reporting. Correlation between discounts and profit does not establish causation.
