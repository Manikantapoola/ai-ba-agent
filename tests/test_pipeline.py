import sys, json
sys.path.insert(0, ".")
import pandas as pd
from src.data_cleaner import clean_data
from src.kpi_engine   import compute_kpis

df = pd.read_csv("data\\sample_sales.csv")
print(f"Loaded: {len(df)} rows")

clean_df, report = clean_data(df)
print(f"Cleaning report: {report}")

kpis = compute_kpis(clean_df)
print(json.dumps(kpis, indent=2, default=str))
print("All good! Ready for AI step.")