
from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent

INPUT_PATH = (
    PROJECT_ROOT / "data" / "processed" / "featured_sales_data.csv"
)

OUTPUT_PATH = (
    PROJECT_ROOT / "data" / "processed" / "dml_ready_data.csv"
)

TREATMENT = "Price"
OUTCOME = "Demand"

CONFOUNDERS = [
    "Competitor Pricing",
    "Promotion",
    "Inventory Level",
    "Seasonality",
    "Category",
    "Region",
]


def prepare_dml_data():
    print("Loading feature-engineered dataset...")
    df = pd.read_csv(INPUT_PATH)

    required_columns = [TREATMENT, OUTCOME] + CONFOUNDERS
    missing_columns = [
        column for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Required columns are missing: {missing_columns}"
        )

    # Keep only variables selected for the initial DML dataset.
    selected_columns = required_columns
    dml_df = df[selected_columns].copy()

    # Convert categorical confounders into numeric indicator columns.
    dml_df = pd.get_dummies(
        dml_df,
        columns=["Seasonality", "Category", "Region"],
        drop_first=True,
        dtype=int,
    )

    # Ensure treatment and outcome are numeric.
    dml_df[TREATMENT] = pd.to_numeric(
        dml_df[TREATMENT], errors="coerce"
    )
    dml_df[OUTCOME] = pd.to_numeric(
        dml_df[OUTCOME], errors="coerce"
    )

    # Remove rows with missing or non-finite values.
    dml_df = dml_df.replace([float("inf"), float("-inf")], pd.NA)
    original_rows = len(dml_df)
    dml_df = dml_df.dropna().copy()
    removed_rows = original_rows - len(dml_df)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    dml_df.to_csv(OUTPUT_PATH, index=False)

    print("\nDML dataset preparation completed.")
    print(f"Rows saved: {len(dml_df)}")
    print(f"Rows removed due to invalid values: {removed_rows}")
    print(f"Treatment: {TREATMENT}")
    print(f"Outcome: {OUTCOME}")
    print(f"Number of model columns: {len(dml_df.columns)}")
    print(f"Missing values remaining: {dml_df.isnull().sum().sum()}")
    print(f"Saved to: {OUTPUT_PATH}")
    print("\nFirst five rows:")
    print(dml_df.head().to_string(index=False))


if __name__ == "__main__":
    prepare_dml_data()
