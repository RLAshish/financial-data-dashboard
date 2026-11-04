from pathlib import Path

import pandas as pd
import requests

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT = ROOT / "outputs"
DATA.mkdir(exist_ok=True)
OUT.mkdir(exist_ok=True)

WORKBOOK_URL = "https://go.microsoft.com/fwlink/?LinkID=521962"
WORKBOOK = DATA / "Financial Sample.xlsx"


def main():
    if not WORKBOOK.exists():
        response = requests.get(WORKBOOK_URL, timeout=90, allow_redirects=True)
        response.raise_for_status()
        WORKBOOK.write_bytes(response.content)

    df = pd.read_excel(WORKBOOK)
    df.columns = [str(column).strip().lower().replace(" ", "_") for column in df.columns]

    required = {
        "segment", "country", "product", "discount_band", "units_sold",
        "manufacturing_price", "sale_price", "gross_sales", "discounts",
        "sales", "cogs", "profit", "date", "month_number", "month_name", "year",
    }
    missing = required.difference(df.columns)
    if missing:
        raise ValueError(f"Workbook schema mismatch; missing: {sorted(missing)}")

    money_columns = [
        "manufacturing_price", "sale_price", "gross_sales",
        "discounts", "sales", "cogs", "profit",
    ]
    for column in money_columns + ["units_sold", "month_number", "year"]:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["date", "sales", "profit", "cogs"]).copy()
    df["year_month"] = df["date"].dt.to_period("M").astype(str)
    df["profit_margin_pct"] = (
        df["profit"].div(df["sales"].where(df["sales"].ne(0))).mul(100)
    )
    df["discount_rate_pct"] = (
        df["discounts"].div(df["gross_sales"].where(df["gross_sales"].ne(0))).mul(100)
    )

    if not (df["sales"] - (df["gross_sales"] - df["discounts"])).abs().le(0.02).all():
        print("Warning: some rows differ from gross sales minus discounts by more than 0.02.")

    kpis = pd.DataFrame([{
        "records": len(df),
        "total_units_sold": round(df["units_sold"].sum(), 2),
        "gross_sales": round(df["gross_sales"].sum(), 2),
        "total_discounts": round(df["discounts"].sum(), 2),
        "net_sales": round(df["sales"].sum(), 2),
        "total_cogs": round(df["cogs"].sum(), 2),
        "total_profit": round(df["profit"].sum(), 2),
        "overall_profit_margin_pct": round(100 * df["profit"].sum() / df["sales"].sum(), 2),
        "average_discount_rate_pct": round(100 * df["discounts"].sum() / df["gross_sales"].sum(), 2),
    }])

    def summarize(column):
        return df.groupby(column, dropna=False).agg(
            records=("sales", "size"),
            units_sold=("units_sold", "sum"),
            net_sales=("sales", "sum"),
            discounts=("discounts", "sum"),
            cogs=("cogs", "sum"),
            profit=("profit", "sum"),
        ).assign(
            profit_margin_pct=lambda table: 100 * table["profit"] / table["net_sales"]
        ).reset_index().sort_values("profit", ascending=False)

    monthly = summarize("year_month")
    by_product = summarize("product")
    by_country = summarize("country")
    by_segment = summarize("segment")
    by_discount = summarize("discount_band")

    df.to_csv(OUT / "clean_financial_sample.csv", index=False)
    with pd.ExcelWriter(OUT / "financial_performance_analysis.xlsx", engine="openpyxl") as writer:
        kpis.to_excel(writer, sheet_name="KPIs", index=False)
        monthly.to_excel(writer, sheet_name="Monthly Trend", index=False)
        by_product.to_excel(writer, sheet_name="By Product", index=False)
        by_country.to_excel(writer, sheet_name="By Country", index=False)
        by_segment.to_excel(writer, sheet_name="By Segment", index=False)
        by_discount.to_excel(writer, sheet_name="By Discount", index=False)

    print(kpis.to_string(index=False))
    print(f"\nAnalysis files saved to: {OUT}")


if __name__ == "__main__":
    main()
