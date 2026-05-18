import pandas as pd

def compute_kpis(df):
    kpis = {}

    # Find revenue column automatically
    num_cols = df.select_dtypes(include="number").columns.tolist()
    rev_col  = next((c for c in num_cols if "rev" in c.lower()), None)
    if rev_col is None and num_cols:
        rev_col = num_cols[0]

    if rev_col:
        kpis["total_revenue"]      = round(float(df[rev_col].sum()), 2)
        kpis["avg_transaction"]    = round(float(df[rev_col].mean()), 2)
        kpis["median_transaction"] = round(float(df[rev_col].median()), 2)
        kpis["revenue_column"]     = rev_col
        company_avg                = kpis["avg_transaction"]

        # Revenue by Region with delta vs company average
        if "Region" in df.columns:
            by_region = df.groupby("Region")[rev_col].sum().round(2)
            region_avg = by_region.mean()
            kpis["revenue_by_region"] = by_region.to_dict()
            kpis["region_vs_average"] = {
                r: round(((v - region_avg) / region_avg) * 100, 1)
                for r, v in by_region.items()
            }
            # Top and bottom regions
            sorted_regions = by_region.sort_values(ascending=False)
            kpis["top_region"]    = sorted_regions.index[0]
            kpis["bottom_region"] = sorted_regions.index[-1]
            kpis["top_region_revenue"]    = round(float(sorted_regions.iloc[0]), 2)
            kpis["bottom_region_revenue"] = round(float(sorted_regions.iloc[-1]), 2)

        # Revenue by Product
        if "Product" in df.columns:
            by_product = df.groupby("Product")[rev_col].sum().round(2)
            kpis["revenue_by_product"] = by_product.to_dict()
            sorted_products = by_product.sort_values(ascending=False)
            kpis["top_product"]    = sorted_products.index[0]
            kpis["bottom_product"] = sorted_products.index[-1]

        # Monthly trend with month over month growth rate
        date_col = next(
            (c for c in df.columns if pd.api.types.is_datetime64_any_dtype(df[c])),
            None
        )
        if date_col:
            df = df.copy()
            df["_month"] = df[date_col].dt.to_period("M").astype(str)
            monthly = df.groupby("_month")[rev_col].sum().round(2)
            kpis["monthly_trend"] = monthly.to_dict()

            # Month over month growth rate
            monthly_list = monthly.tolist()
            mom_growth = []
            for i in range(1, len(monthly_list)):
                if monthly_list[i-1] != 0:
                    growth = round(
                        ((monthly_list[i] - monthly_list[i-1]) / monthly_list[i-1]) * 100,
                        1
                    )
                else:
                    growth = 0
                mom_growth.append(growth)
            kpis["mom_growth_rates"] = dict(
                zip(list(monthly.index)[1:], mom_growth)
            )
            # Best and worst month
            kpis["best_month"]  = monthly.idxmax()
            kpis["worst_month"] = monthly.idxmin()
            kpis["best_month_revenue"]  = round(float(monthly.max()), 2)
            kpis["worst_month_revenue"] = round(float(monthly.min()), 2)

        # New vs Repeat customer split
        if "Customer_Type" in df.columns:
            by_ctype = df.groupby("Customer_Type")[rev_col].sum().round(2)
            kpis["revenue_by_customer_type"] = by_ctype.to_dict()
            total = sum(by_ctype.values)
            kpis["customer_type_pct"] = {
                k: round((v / total) * 100, 1)
                for k, v in by_ctype.items()
            }

        # Top and bottom sales reps
        if "Sales_Rep" in df.columns:
            by_rep = df.groupby("Sales_Rep")[rev_col].sum().round(2)
            rep_avg = by_rep.mean()
            sorted_reps = by_rep.sort_values(ascending=False)
            top3 = sorted_reps.head(3)
            bot3 = sorted_reps.tail(3)
            kpis["top_reps"] = [
                {
                    "name": name,
                    "revenue": round(float(rev), 2),
                    "vs_average": f"+{round(((rev - rep_avg)/rep_avg)*100, 1)}%"
                    if rev >= rep_avg
                    else f"{round(((rev - rep_avg)/rep_avg)*100, 1)}%"
                }
                for name, rev in top3.items()
            ]
            kpis["bottom_reps"] = [
                {
                    "name": name,
                    "revenue": round(float(rev), 2),
                    "vs_average": f"+{round(((rev - rep_avg)/rep_avg)*100, 1)}%"
                    if rev >= rep_avg
                    else f"{round(((rev - rep_avg)/rep_avg)*100, 1)}%"
                }
                for name, rev in bot3.items()
            ]

        # Units sold stats
        units_col = next((c for c in num_cols if "unit" in c.lower()), None)
        if units_col:
            kpis["total_units"]   = int(df[units_col].sum())
            kpis["avg_units"]     = round(float(df[units_col].mean()), 1)

    kpis["total_rows"]   = int(len(df))
    kpis["column_names"] = df.columns.tolist()
    return kpis