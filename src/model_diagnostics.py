
import numpy as np
import pandas as pd
from math import erfc, sqrt
from scipy.stats import norm
from src.prepare_dml_residuals import prepare_dml_residuals
from src.model_config import RESULTS_DIR


def run_model_diagnostics():
    results = prepare_dml_residuals()

    price_residual = results["Price_Residual"].to_numpy()
    demand_residual = results["Demand_Residual"].to_numpy()

    denominator = np.sum(price_residual ** 2)

    if denominator <= 1e-10:
        raise ValueError("Insufficient variation in price residuals.")

    effect = np.sum(price_residual * demand_residual) / denominator

    errors = demand_residual - effect * price_residual
    n = len(errors)

    # Approximate standard error for the residual regression.
    # variance = np.sum(errors ** 2) / max(n - 1, 1)
    # standard_error = np.sqrt(variance / denominator)
    # Influence-function-based standard error for the DML estimate.
    score = price_residual * errors
    score_mean = np.mean(score)
    score_variance = np.sum((score - score_mean) ** 2) / (n - 1)

    mean_price_residual_squared = denominator / n
    standard_error = (
    np.sqrt(score_variance / n)
    / mean_price_residual_squared
    )
    ci_lower = effect - 1.96 * standard_error
    ci_upper = effect + 1.96 * standard_error
    # Approximate z-statistic and two-sided p-value.
    z_statistic = effect / standard_error
    log_p_value = np.log(2) + norm.logsf(abs(z_statistic))
    p_value = np.exp(log_p_value)
    diagnostics = pd.DataFrame([{
        "Observations": n,
        "Estimated_Price_Effect": effect,
        "Approx_Standard_Error": standard_error,
        "Approx_Z_Statistic": z_statistic,
        "Approx_P_Value": p_value,
        "Approx_Log_P_Value": log_p_value,
        "Approx_95CI_Lower": ci_lower,
        "Approx_95CI_Upper": ci_upper,
        "Price_Residual_Std": np.std(price_residual),
        "Demand_Residual_Std": np.std(demand_residual),
    }])

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    output_path = RESULTS_DIR / "model_diagnostics.csv"
    diagnostics.to_csv(output_path, index=False)

    print("\nModel diagnostics completed.")
    print(diagnostics.to_string(index=False))
    print(f"\nDiagnostics saved to: {output_path}")

    return diagnostics


if __name__ == "__main__":
    run_model_diagnostics()
