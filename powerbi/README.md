# Power BI dashboard guide

Download the Microsoft Financial Sample workbook and run `python src/analyze.py`. Import `outputs/clean_financial_sample.csv` into Power BI Desktop.

## Core DAX measures
```DAX
Gross Sales = SUM(financial_sample[gross_sales])
Discounts = SUM(financial_sample[discounts])
Net Sales = SUM(financial_sample[sales])
Total COGS = SUM(financial_sample[cogs])
Total Profit = SUM(financial_sample[profit])
Profit Margin = DIVIDE([Total Profit], [Net Sales])
Units Sold = SUM(financial_sample[units_sold])
Discount Rate = DIVIDE([Discounts], [Gross Sales])
```

Format Profit Margin and Discount Rate as percentages. Create a proper calendar table and relate it to the fact table's date column for robust time intelligence.

## Suggested report pages
1. **Executive overview:** Net Sales, Total Profit, Profit Margin, Discounts and Units Sold cards; monthly sales/profit trend.
2. **Product & segment performance:** net sales and profit by product; profitability by segment; units sold.
3. **Geographic performance:** sales and profit by country; country-level margin comparison.
4. **Discount effectiveness:** discount rate and profit margin by discount band; investigate high-discount / low-margin combinations.

Add slicers for year, country, segment, product and discount band. Reconcile Power BI totals with the Python-generated Excel workbook. Save your finished `.pbix` file in this folder.
