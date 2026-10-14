
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import KFold, cross_val_predict

from src.model_config import (
    DATA_PATH,
    OUTCOME,
    CONFOUNDERS,
    RANDOM_STATE,
)


def train_demand_model():
    df = pd.read_csv(DATA_PATH)

    required_columns = [OUTCOME] + CONFOUNDERS
    missing_columns = [
        col for col in required_columns if col not in df.columns
    ]

    if missing_columns:
        raise ValueError(f"Missing columns: {missing_columns}")

    X = df[CONFOUNDERS]
    demand = df[OUTCOME]

    model = RandomForestRegressor(
        n_estimators=100,
        min_samples_leaf=10,
        random_state=RANDOM_STATE,
        n_jobs=-1,
    )

    folds = KFold(
        n_splits=5,
        shuffle=True,
        random_state=RANDOM_STATE,
    )

    predicted_demand = cross_val_predict(
        model,
        X,
        demand,
        cv=folds,
        n_jobs=1,
    )

    demand_residuals = demand.to_numpy() - predicted_demand

    print("Demand model completed successfully.")
    print(f"Actual demand mean: {demand.mean():.2f}")
    print(f"Predicted demand mean: {predicted_demand.mean():.2f}")
    print(f"Demand residual mean: {demand_residuals.mean():.4f}")
    print(
        "Demand residual standard deviation: "
        f"{demand_residuals.std():.4f}"
    )

    return model, predicted_demand, demand_residuals


if __name__ == "__main__":
    train_demand_model()
