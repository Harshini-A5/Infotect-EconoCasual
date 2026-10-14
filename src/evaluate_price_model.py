
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

from src.model_config import (
    DATA_PATH,
    TREATMENT,
    CONFOUNDERS,
    RANDOM_STATE,
    TEST_SIZE,
)


def evaluate_price_model():
    df = pd.read_csv(DATA_PATH)

    X = df[CONFOUNDERS]
    y = df[TREATMENT]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE,
    )

    model = RandomForestRegressor(
        n_estimators=100,
        min_samples_leaf=10,
        random_state=RANDOM_STATE,
        n_jobs=-1,
    )

    model.fit(X_train, y_train)
    predictions = model.predict(X_test)

    mae = mean_absolute_error(y_test, predictions)
    rmse = mean_squared_error(y_test, predictions) ** 0.5
    r2 = r2_score(y_test, predictions)

    print("Price model evaluation completed.")
    print(f"Test observations: {len(y_test)}")
    print(f"MAE: {mae:.4f}")
    print(f"RMSE: {rmse:.4f}")
    print(f"R² score: {r2:.4f}")


if __name__ == "__main__":
    evaluate_price_model()

