# PYTHON LIBRARIES
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
from pandasql import sqldf

# SETUP
sns.set_theme(style="whitegrid")
pysql = lambda q: sqldf(q, globals())

print("Setup complete.")

# GENERATE DATA
np.random.seed(42)
n = 300

df = pd.DataFrame(
    {
        "order_id": range(1, n + 1),
        "order_date": pd.date_range("2024-01-01", periods=n, freq="D"),
        "region": np.random.choice(["West", "East", "South", "North"], n),
        "category": np.random.choice(["Electronics", "Clothing", "Grocery"], n),
        "sales": np.random.randint(100, 5000, n),
        "discount": np.random.choice([0, 0.1, 0.2, np.nan], n),
    }
)
# CLEAN AND TRANSFORM DATA
df["discount"] = df["discount"].fillna(0)
df["net_sales"] = (df["sales"] * (1 - df["discount"])).round(2)
df["quarter"] = df["order_date"].dt.to_period("Q").astype(str)
df = df.drop_duplicates(subset=["order_id"])

# SQL
region_q = pysql("""
    SELECT region,
            ROUND(SUM(net_sales), 2) AS total_sales,
            COUNT(*) AS orders
    FROM df
    GROUP BY region
    ORDER BY total_sales DESC
""")

print(region_q)

print("Added columns: net_sales, quarter")
print("DataFrame created and cleaned. Shape:", df.shape)
