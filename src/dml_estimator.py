
import numpy as np
import pandas as pd

from src.prepare_dml_residuals import prepare_dml_residuals
from src.model_config import RESULTS_DIR


def estimate_price_effect():
    residuals = prepare_dml_residuals()

    price_residual = residuals["Price_Residual"].to_numpy()
    demand_residual = residuals["Demand_Residual"].to_numpy()

    denominator = np.sum(price_residual ** 2)

    if denominator < 1e-10:
        raise ValueError(
            "Price residuals have almost no variation. "
            "The causal effect cannot be estimated reliably."
        )

    # DML partial-linear estimate
    effect = np.sum(
        price_residual * demand_residual
    ) / denominator

    predicted_effect = effect * price_residual
    estimation_error = demand_residual - predicted_effect

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    summary = pd.DataFrame([{
        "Estimated_Price_Effect": effect,
        "Residual_Price_Variance": np.var(price_residual),
        "Residual_Demand_Std": np.std(demand_residual),
        "Observations": len(residuals),
    }])

    output_path = RESULTS_DIR / "dml_estimate.csv"
    summary.to_csv(output_path, index=False)

    print("\nDML estimation completed.")
    print(f"Estimated effect per price unit: {effect:.6f}")
    print(
        "Interpretation: A one-unit increase in price is associated "
        f"with an estimated {effect:.4f}-unit change in demand."
    )
    print(f"Observations: {len(residuals)}")
    print(f"Results saved to: {output_path}")

    return effect, estimation_error


if __name__ == "__main__":
    estimate_price_effect()
