import pandas as pd

def clean_data(df):
    report = {}
    original_rows = len(df)

    df = df.drop_duplicates()
    report["duplicates_removed"] = original_rows - len(df)

    null_counts = df.isnull().sum()
    report["nulls_found"] = {col: int(v) for col, v in null_counts.items() if v > 0}

    df = df.dropna(how="all")

    for col in df.select_dtypes(include="number").columns:
        df[col] = df[col].fillna(df[col].median())

    for col in df.columns:
        if any(word in col.lower() for word in ["date", "time", "dt"]):
            try:
                df[col] = pd.to_datetime(df[col], errors="coerce")
            except Exception:
                pass

    str_cols = df.select_dtypes(include="object").columns
    df[str_cols] = df[str_cols].apply(lambda c: c.str.strip())

    report["final_rows"] = len(df)
    return df, report