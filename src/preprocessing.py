
from pathlib import Path
import pandas as pd

# Find the project root directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Define input and output paths
RAW_DATA_PATH = PROJECT_ROOT / "data" / "raw" / "sales_data.csv"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
PROCESSED_DATA_PATH = PROCESSED_DIR / "cleaned_sales_data.csv"


def preprocess_data():
    """Clean the retail dataset and create date-based features."""

    print("Loading the raw dataset...")
    df = pd.read_csv(RAW_DATA_PATH)

    print(f"Original dataset shape: {df.shape}")

    # Remove fully duplicated rows
    duplicate_count = df.duplicated().sum()
    print(f"Duplicate rows found: {duplicate_count}")

    if duplicate_count > 0:
        df = df.drop_duplicates()

    # Convert Date to datetime
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    invalid_dates = df["Date"].isna().sum()
    print(f"Invalid or missing dates: {invalid_dates}")

    # Remove rows without a valid date
    if invalid_dates > 0:
        df = df.dropna(subset=["Date"]).copy()

    # Create date-based features
    df["Year"] = df["Date"].dt.year
    df["Month"] = df["Date"].dt.month
    df["Day"] = df["Date"].dt.day
    df["DayOfWeek"] = df["Date"].dt.dayofweek

    # Check missing values in remaining columns
    print("\nMissing values by column:")
    print(df.isnull().sum().to_string())

    # Create the output directory if necessary
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    # Save the processed dataset
    df.to_csv(PROCESSED_DATA_PATH, index=False)

    print("\nPreprocessing completed successfully!")
    print(f"Processed dataset shape: {df.shape}")
    print(f"Saved to: {PROCESSED_DATA_PATH}")


if __name__ == "__main__":
    preprocess_data()
