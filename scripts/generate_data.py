import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

random.seed(42)
np.random.seed(42)
n = 500

regions  = ["North", "South", "East", "West"]
products = ["Widget A", "Widget B", "Widget C", "Premium Pack"]
reps     = [f"Rep_{i}" for i in range(1, 11)]

data = {
    "Date":          [datetime(2024,1,1) + timedelta(days=random.randint(0,364)) for _ in range(n)],
    "Region":        [random.choice(regions) for _ in range(n)],
    "Sales_Rep":     [random.choice(reps) for _ in range(n)],
    "Product":       [random.choice(products) for _ in range(n)],
    "Units_Sold":    np.random.randint(1, 50, n),
    "Unit_Price":    np.random.uniform(10, 200, n).round(2),
    "Customer_Type": [random.choice(["New", "Repeat"]) for _ in range(n)]
}

df = pd.DataFrame(data)
df["Revenue"] = (df["Units_Sold"] * df["Unit_Price"]).round(2)

mask = (df["Region"] == "West") & (df["Date"].dt.month >= 9)
df.loc[mask, "Revenue"] *= 0.6

df.to_csv("data\\sample_sales.csv", index=False)
print("Done! Created data\\sample_sales.csv with 500 rows")