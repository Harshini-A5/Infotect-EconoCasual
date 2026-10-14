
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

RESULTS_DIR = Path(__file__).resolve().parent.parent / "reports" / "figures"
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

from src.model_config import (
    DATA_PATH,
    OUTCOME,
    CONFOUNDERS,
    RANDOM_STATE,
    TEST_SIZE,
)


def plot_demand_predictions():
    df = pd.read_csv(DATA_PATH)

    X = df[CONFOUNDERS]
    y = df[OUTCOME]

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

    # RESULTS_DIR = DATA_PATH.parent.parent / "reports" / "figures"
    RESULTS_DIR = Path(__file__).resolve().parent.parent / "reports" / "figures"   
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    plt.figure(figsize=(8, 6))
    plt.scatter(y_test, predictions, alpha=0.35)

    lower = min(y_test.min(), predictions.min())
    upper = max(y_test.max(), predictions.max())
    plt.plot([lower, upper], [lower, upper], linestyle="--")

    plt.xlabel("Actual Demand")
    plt.ylabel("Predicted Demand")
    plt.title("Actual vs Predicted Demand")
    plt.tight_layout()

    output_path = RESULTS_DIR / "actual_vs_predicted_demand.png"
    plt.savefig(output_path, dpi=150)
    plt.close()

    print("Demand prediction plot saved to:")
    print(output_path)


if __name__ == "__main__":
    plot_demand_predictions()
