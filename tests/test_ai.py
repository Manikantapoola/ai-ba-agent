import sys, json
sys.path.insert(0, ".")
import pandas as pd
from src.data_cleaner import clean_data
from src.kpi_engine   import compute_kpis
from src.ai_agent     import run_analysis

df            = pd.read_csv("data\\sample_sales.csv")
clean_df, rep = clean_data(df)
kpis          = compute_kpis(clean_df)

print("Sending to Claude AI... (takes about 10 seconds)")
result = run_analysis(kpis, rep)

if "error" in result:
    print(f"ERROR: {result['error']}")
else:
    print(f"\nSummary: {result.get('summary')}")
    print(f"\nInsights:")
    for i, x in enumerate(result.get("insights",[]), 1):
        print(f"  {i}. {x}")
    print(f"\nRisks:")
    for x in result.get("risks",[]):
        print(f"  - {x}")
    print(f"\nRecommendations:")
    for x in result.get("recommendations",[]):
        print(f"  > {x}")