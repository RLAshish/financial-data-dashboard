-- Import outputs/clean_financial_sample.csv into a table named financial_sample.
-- SQL below uses common SQL syntax; date functions may vary by database.

-- 1. Executive KPIs
SELECT SUM(gross_sales) AS gross_sales,
       SUM(discounts) AS total_discounts,
       SUM(sales) AS net_sales,
       SUM(cogs) AS total_cogs,
       SUM(profit) AS total_profit,
       ROUND(100.0 * SUM(profit) / NULLIF(SUM(sales), 0), 2) AS profit_margin_pct
FROM financial_sample;

-- 2. Monthly sales and profit trend
SELECT year_month, SUM(sales) AS net_sales, SUM(profit) AS profit,
       ROUND(100.0 * SUM(profit) / NULLIF(SUM(sales), 0), 2) AS profit_margin_pct
FROM financial_sample
GROUP BY year_month
ORDER BY year_month;

-- 3. Product performance
SELECT product, SUM(units_sold) AS units_sold,
       SUM(sales) AS net_sales, SUM(profit) AS profit,
       ROUND(100.0 * SUM(profit) / NULLIF(SUM(sales), 0), 2) AS profit_margin_pct
FROM financial_sample
GROUP BY product
ORDER BY profit DESC;

-- 4. Country contribution
SELECT country, SUM(sales) AS net_sales, SUM(profit) AS profit,
       ROUND(100.0 * SUM(profit) / NULLIF(SUM(sales), 0), 2) AS profit_margin_pct
FROM financial_sample
GROUP BY country
ORDER BY net_sales DESC;

-- 5. Segment profitability
SELECT segment, SUM(sales) AS net_sales, SUM(profit) AS profit,
       ROUND(100.0 * SUM(profit) / NULLIF(SUM(sales), 0), 2) AS profit_margin_pct
FROM financial_sample
GROUP BY segment
ORDER BY profit DESC;

-- 6. Discount band analysis
SELECT discount_band, SUM(gross_sales) AS gross_sales,
       SUM(discounts) AS discounts, SUM(sales) AS net_sales,
       SUM(profit) AS profit,
       ROUND(100.0 * SUM(profit) / NULLIF(SUM(sales), 0), 2) AS profit_margin_pct
FROM financial_sample
GROUP BY discount_band
ORDER BY discount_band;
