import pandas as pd

def compute_kpis(df):
    kpis = {}
    num_cols = df.select_dtypes(include="number").columns.tolist()
    rev_col  = next((c for c in num_cols if "rev" in c.lower()), None)
    if rev_col is None and num_cols:
        rev_col = num_cols[0]

    if rev_col:
        kpis["total_revenue"]      = round(float(df[rev_col].sum()), 2)
        kpis["avg_transaction"]    = round(float(df[rev_col].mean()), 2)
        kpis["median_transaction"] = round(float(df[rev_col].median()), 2)
        kpis["revenue_column"]     = rev_col

        if "Region" in df.columns:
            kpis["revenue_by_region"] = df.groupby("Region")[rev_col].sum().round(2).to_dict()

        if "Product" in df.columns:
            kpis["revenue_by_product"] = df.groupby("Product")[rev_col].sum().round(2).to_dict()

        date_col = next((c for c in df.columns if pd.api.types.is_datetime64_any_dtype(df[c])), None)
        if date_col:
            df = df.copy()
            df["_month"] = df[date_col].dt.to_period("M").astype(str)
            kpis["monthly_trend"] = df.groupby("_month")[rev_col].sum().round(2).to_dict()

        if "Customer_Type" in df.columns:
            kpis["revenue_by_customer_type"] = df.groupby("Customer_Type")[rev_col].sum().round(2).to_dict()

    kpis["total_rows"]   = int(len(df))
    kpis["column_names"] = df.columns.tolist()
    return kpis