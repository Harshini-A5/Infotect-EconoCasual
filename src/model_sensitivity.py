from pathlib import Path
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


def estimate_effect(df, n_estimators, min_samples_leaf):
    X = df[CONFOUNDERS]
    price = df[TREATMENT]
    demand = df[OUTCOME]

    folds = KFold(
        n_splits=5,
        shuffle=True,
        random_state=RANDOM_STATE,
    )

    price_model = RandomForestRegressor(
        n_estimators=n_estimators,
        min_samples_leaf=min_samples_leaf,
        random_state=RANDOM_STATE,
        n_jobs=-1,
    )

    demand_model = RandomForestRegressor(
        n_estimators=n_estimators,
        min_samples_leaf=min_samples_leaf,
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


def run_sensitivity_analysis():
    df = pd.read_csv(DATA_PATH)

    configurations = [
        (100, 5),
        (100, 10),
        (100, 20),
    ]

    rows = []

    for n_estimators, min_samples_leaf in configurations:
        effect = estimate_effect(
            df,
            n_estimators=n_estimators,
            min_samples_leaf=min_samples_leaf,
        )

        rows.append({
            "Trees": n_estimators,
            "Min_Samples_Leaf": min_samples_leaf,
            "Estimated_Price_Effect": effect,
        })

    results = pd.DataFrame(rows)
    print(results.to_string(index=False))

    output_path = (
        DATA_PATH.parent.parent
        / "reports"
        / "results"
        / "model_sensitivity.csv"
    )
    # output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path = (
    Path(__file__).resolve().parent.parent
    / "reports"
    / "results"
    / "model_sensitivity.csv"
)
    results.to_csv(output_path, index=False)

    print(f"\nResults saved to: {output_path}")


if __name__ == "__main__":
    run_sensitivity_analysis()
