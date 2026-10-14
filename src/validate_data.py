
from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = PROJECT_ROOT / "data" / "processed" / "cleaned_sales_data.csv"

REQUIRED_COLUMNS = [
    "Date",
    "Store ID",
    "Product ID",
    "Category",
    "Region",
    "Inventory Level",
    "Units Sold",
    "Units Ordered",
    "Price",
    "Discount",
    "Promotion",
    "Competitor Pricing",
    "Demand",
    "Year",
    "Month",
    "Day",
    "DayOfWeek",
]


def validate_data():
    print("Starting data validation...\n")

    if not DATA_PATH.exists():
        print(f"ERROR: Dataset not found at {DATA_PATH}")
        print("Run: python src/preprocessing.py")
        return

    df = pd.read_csv(DATA_PATH)
    print(f"Dataset shape: {df.shape}")

    missing_columns = [
        column for column in REQUIRED_COLUMNS
        if column not in df.columns
    ]

    if missing_columns:
        print(f"Missing required columns: {missing_columns}")
    else:
        print("All required columns are present.")

    missing_values = df.isnull().sum().sum()
    duplicate_rows = df.duplicated().sum()
    invalid_prices = (df["Price"] <= 0).sum()
    invalid_demand = (df["Demand"] < 0).sum()
    invalid_dates = pd.to_datetime(
        df["Date"], errors="coerce"
    ).isna().sum()

    print(f"Missing values: {missing_values}")
    print(f"Duplicate rows: {duplicate_rows}")
    print(f"Prices less than or equal to zero: {invalid_prices}")
    print(f"Negative demand values: {invalid_demand}")
    print(f"Invalid dates: {invalid_dates}")

    if (
        not missing_columns
        and missing_values == 0
        and duplicate_rows == 0
        and invalid_prices == 0
        and invalid_demand == 0
        and invalid_dates == 0
    ):
        print("\nRESULT: Data validation passed!")
    else:
        print("\nRESULT: Data validation found issues. Review the results above.")


if __name__ == "__main__":
    validate_data()
