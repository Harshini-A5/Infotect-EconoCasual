
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import KFold, cross_val_predict

from src.model_config import (
    DATA_PATH,
    TREATMENT,
    CONFOUNDERS,
    RANDOM_STATE,
)


def train_treatment_model():
    df = pd.read_csv(DATA_PATH)

    required_columns = [TREATMENT] + CONFOUNDERS
    missing_columns = [
        col for col in required_columns if col not in df.columns
    ]

    if missing_columns:
        raise ValueError(f"Missing columns: {missing_columns}")

    X = df[CONFOUNDERS]
    treatment = df[TREATMENT]

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

    predicted_price = cross_val_predict(
        model,
        X,
        treatment,
        cv=folds,
        n_jobs=1,
    )

    price_residuals = treatment.to_numpy() - predicted_price

    print("Treatment model completed successfully.")
    print(f"Actual price mean: {treatment.mean():.2f}")
    print(f"Predicted price mean: {predicted_price.mean():.2f}")
    print(f"Price residual mean: {price_residuals.mean():.4f}")
    print(f"Price residual standard deviation: {price_residuals.std():.4f}")

    return model, predicted_price, price_residuals


if __name__ == "__main__":
    train_treatment_model()
