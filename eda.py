
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Load dataset
df = pd.read_csv(Path("data/raw/sales_data.csv"))

# Create folder for EDA results
Path("reports/figures").mkdir(parents=True, exist_ok=True)

sns.set_theme(style="whitegrid")

# 1. Price vs Demand
plt.figure(figsize=(8, 5))
sns.scatterplot(data=df, x="Price", y="Demand", alpha=0.3)
plt.title("Price vs Demand")
plt.tight_layout()
plt.savefig("reports/figures/price_vs_demand.png", dpi=150)
plt.close()

# 2. Average demand by promotion status
plt.figure(figsize=(7, 5))
sns.barplot(data=df, x="Promotion", y="Demand", errorbar=None)
plt.title("Average Demand by Promotion Status")
plt.tight_layout()
plt.savefig("reports/figures/promotion_vs_demand.png", dpi=150)
plt.close()

# 3. Correlation among numerical variables
numeric_columns = [
    "Inventory Level", "Units Sold", "Units Ordered",
    "Price", "Discount", "Promotion",
    "Competitor Pricing", "Epidemic", "Demand"
]

plt.figure(figsize=(10, 7))
sns.heatmap(
    df[numeric_columns].corr(),
    annot=True,
    cmap="coolwarm",
    fmt=".2f"
)
plt.title("Correlation Heatmap")
plt.tight_layout()
plt.savefig("reports/figures/correlation_heatmap.png", dpi=150)
plt.close()

print("EDA completed successfully!")
print("Charts saved in reports/figures/")

print("\nAverage demand by promotion:")
print(df.groupby("Promotion")["Demand"].mean())

print("\nAverage demand by season:")
print(df.groupby("Seasonality")["Demand"].mean())

print("\nAverage price and demand by category:")
print(df.groupby("Category")[["Price", "Demand"]].mean())

