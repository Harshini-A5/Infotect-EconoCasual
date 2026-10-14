
import numpy as np
import pandas as pd

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import KFold, cross_val_predict

from src.model_config import (
    DATA_PATH,
    TREATMENT,
    OUTCOME,
    CONFOUNDERS,
    RANDOM_STATE,
)


def prepare_dml_residuals():
    df = pd.read_csv(DATA_PATH)

    required = [TREATMENT, OUTCOME] + CONFOUNDERS
    missing = [col for col in required if col not in df.columns]

    if missing:
        raise ValueError(f"Missing columns: {missing}")

    X = df[CONFOUNDERS]
    price = df[TREATMENT]
    demand = df[OUTCOME]

    folds = KFold(
        n_splits=5,
        shuffle=True,
        random_state=RANDOM_STATE,
    )

    price_model = RandomForestRegressor(
        n_estimators=100,
        min_samples_leaf=10,
        random_state=RANDOM_STATE,
        n_jobs=-1,
    )

    demand_model = RandomForestRegressor(
        n_estimators=100,
        min_samples_leaf=10,
        random_state=RANDOM_STATE,
        n_jobs=-1,
    )

    predicted_price = cross_val_predict(
        price_model, X, price, cv=folds, n_jobs=1
    )

    predicted_demand = cross_val_predict(
        demand_model, X, demand, cv=folds, n_jobs=1
    )

    results = pd.DataFrame({
        "Actual_Price": price.to_numpy(),
        "Predicted_Price": predicted_price,
        "Price_Residual": price.to_numpy() - predicted_price,
        "Actual_Demand": demand.to_numpy(),
        "Predicted_Demand": predicted_demand,
        "Demand_Residual": demand.to_numpy() - predicted_demand,
    })

    print("DML residual preparation completed.")
    print(f"Rows: {len(results)}")
    print(
        "Price residual standard deviation:",
        round(results["Price_Residual"].std(), 4),
    )
    print(
        "Demand residual standard deviation:",
        round(results["Demand_Residual"].std(), 4),
    )
    print("\nSample residuals:")
    print(results.head())

    return results


if __name__ == "__main__":
    prepare_dml_residuals()
