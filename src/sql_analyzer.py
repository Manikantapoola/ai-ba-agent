import sqlite3
import pandas as pd

def run_sql_kpis(df):
    """
    Loads the cleaned data into SQLite (in memory, no file created).
    Runs SQL GROUP BY queries - same as enterprise data warehouse usage.
    """
    conn = sqlite3.connect(":memory:")
    df.to_sql("sales", conn, index=False, if_exists="replace")

    results = {}

    try:
        r1 = pd.read_sql("""
            SELECT
                Region,
                ROUND(SUM(Revenue), 2)  AS total_revenue,
                ROUND(AVG(Revenue), 2)  AS avg_revenue,
                COUNT(*)                AS num_transactions
            FROM sales
            GROUP BY Region
            ORDER BY total_revenue DESC
        """, conn)
        results["by_region"] = r1.to_dict(orient="records")
    except Exception:
        pass

    try:
        r2 = pd.read_sql("""
            SELECT
                Sales_Rep,
                ROUND(SUM(Revenue), 2) AS total_revenue,
                COUNT(*) AS deals_closed
            FROM sales
            GROUP BY Sales_Rep
            ORDER BY total_revenue DESC
            LIMIT 5
        """, conn)
        results["top_reps"] = r2.to_dict(orient="records")
    except Exception:
        pass

    conn.close()
    return results