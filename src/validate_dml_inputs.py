
import pandas as pd

from src.model_config import (
    DATA_PATH,
    TREATMENT,
    OUTCOME,
    CONFOUNDERS,
)


def validate_dml_inputs():
    df = pd.read_csv(DATA_PATH)

    required_columns = [TREATMENT, OUTCOME] + CONFOUNDERS
    missing = [col for col in required_columns if col not in df.columns]

    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    if df.empty:
        raise ValueError("The dataset is empty.")

    if df[required_columns].isnull().any().any():
        raise ValueError("Missing values found in DML input columns.")

    if not all(
        pd.api.types.is_numeric_dtype(df[col])
        for col in required_columns
    ):
        raise ValueError("All DML input columns must be numeric.")

    if df[TREATMENT].nunique() < 2:
        raise ValueError("Price has insufficient variation.")

    if df[OUTCOME].nunique() < 2:
        raise ValueError("Demand has insufficient variation.")

    print("DML input validation passed.")
    print(f"Rows: {len(df)}")
    print(f"Treatment: {TREATMENT}")
    print(f"Outcome: {OUTCOME}")
    print(f"Confounder count: {len(CONFOUNDERS)}")
    print(f"Price range: {df[TREATMENT].min():.2f} to {df[TREATMENT].max():.2f}")
    print(f"Demand range: {df[OUTCOME].min():.2f} to {df[OUTCOME].max():.2f}")


if __name__ == "__main__":
    validate_dml_inputs()
