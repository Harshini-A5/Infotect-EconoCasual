
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


def estimate_effect(df):
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

    price_pred = cross_val_predict(
        price_model, X, price, cv=folds, n_jobs=1
    )
    demand_pred = cross_val_predict(
        demand_model, X, demand, cv=folds, n_jobs=1
    )

    price_resid = price.to_numpy() - price_pred
    demand_resid = demand.to_numpy() - demand_pred

    denominator = (price_resid ** 2).sum()
    if denominator < 1e-10:
        raise ValueError("Insufficient residual price variation.")

    return (price_resid * demand_resid).sum() / denominator


def run_stability_check():
    df = pd.read_csv(DATA_PATH)

    required = [TREATMENT, OUTCOME] + CONFOUNDERS
    missing = [col for col in required if col not in df.columns]
    if missing:
        raise ValueError(f"Missing columns: {missing}")

    # Compare the full dataset with two reproducible random samples.
    samples = {
        "Full dataset": df,
        "Sample 80% A": df.sample(frac=0.8, random_state=21),
        "Sample 80% B": df.sample(frac=0.8, random_state=84),
    }

    rows = []
    for name, sample in samples.items():
        effect = estimate_effect(sample)
        rows.append({
            "Sample": name,
            "Observations": len(sample),
            "Estimated_Price_Effect": effect,
        })

    results = pd.DataFrame(rows)
    print(results.to_string(index=False))
    print(
        "\nNote: These are sensitivity checks, not independent "
        "confirmations of causality."
    )
    return results


if __name__ == "__main__":
    run_stability_check()
