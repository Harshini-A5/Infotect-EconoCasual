
import joblib
import pandas as pd
from pathlib import Path
from sklearn.ensemble import RandomForestRegressor

from src.model_config import (
    DATA_PATH,
    OUTCOME,
    CONFOUNDERS,
    RANDOM_STATE,
)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
MODEL_DIR = PROJECT_ROOT / "models"
MODEL_PATH = MODEL_DIR / "demand_prediction_model.joblib"


def main():
    df = pd.read_csv(DATA_PATH)

    required_columns = CONFOUNDERS + [OUTCOME]
    missing = [col for col in required_columns if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    X = df[CONFOUNDERS]
    y = df[OUTCOME]

    model = RandomForestRegressor(
        n_estimators=100,
        min_samples_leaf=10,
        random_state=RANDOM_STATE,
        n_jobs=-1,
    )

    model.fit(X, y)

    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(
        {"model": model, "features": CONFOUNDERS},
        MODEL_PATH,
    )

    print("Demand prediction model trained successfully.")
    print(f"Training rows: {len(df)}")
    print(f"Input features: {len(CONFOUNDERS)}")
    print(f"Model saved to: {MODEL_PATH}")


if __name__ == "__main__":
    main()
