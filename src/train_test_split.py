
from sklearn.model_selection import train_test_split

from src.model_config import (
    DATA_PATH,
    TREATMENT,
    OUTCOME,
    CONFOUNDERS,
    RANDOM_STATE,
    TEST_SIZE,
)

import pandas as pd


def load_and_split_data():
    df = pd.read_csv(DATA_PATH)

    required_columns = [TREATMENT, OUTCOME] + CONFOUNDERS
    missing_columns = [
        column for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing columns in dataset: {missing_columns}"
        )

    X = df[CONFOUNDERS]
    treatment = df[TREATMENT]
    outcome = df[OUTCOME]

    X_train, X_test, treatment_train, treatment_test, outcome_train, outcome_test = (
        train_test_split(
            X,
            treatment,
            outcome,
            test_size=TEST_SIZE,
            random_state=RANDOM_STATE,
        )
    )

    print("Dataset loaded successfully.")
    print(f"Total rows: {len(df)}")
    print(f"Training rows: {len(X_train)}")
    print(f"Testing rows: {len(X_test)}")
    print(f"Confounder features: {X.shape[1]}")

    return (
        X_train,
        X_test,
        treatment_train,
        treatment_test,
        outcome_train,
        outcome_test,
    )


if __name__ == "__main__":
    load_and_split_data()
