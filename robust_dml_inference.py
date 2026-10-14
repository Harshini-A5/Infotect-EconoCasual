
import pandas as pd
import statsmodels.api as sm

from src.prepare_dml_residuals import prepare_dml_residuals
from src.model_config import RESULTS_DIR


def run_robust_dml_inference():
    residuals = prepare_dml_residuals()

    price_residual = residuals["Price_Residual"]
    demand_residual = residuals["Demand_Residual"]

    regression = sm.OLS(
        demand_residual,
        price_residual.to_frame(name="Price_Residual"),
    ).fit(cov_type="HC1")

    effect = regression.params["Price_Residual"]
    standard_error = regression.bse["Price_Residual"]
    confidence_interval = regression.conf_int().loc["Price_Residual"]

    results = pd.DataFrame([{
        "Observations": int(regression.nobs),
        "Estimated_Price_Effect": effect,
        "Robust_Standard_Error_HC1": standard_error,
        "CI_95_Lower": confidence_interval.iloc[0],
        "CI_95_Upper": confidence_interval.iloc[1],
        "P_Value": regression.pvalues["Price_Residual"],
    }])

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    output_path = RESULTS_DIR / "robust_dml_inference.csv"
    results.to_csv(output_path, index=False)

    print("Robust DML inference completed.")
    print(results.to_string(index=False))
    print(f"\nSaved to: {output_path}")

    return results


if __name__ == "__main__":
    run_robust_dml_inference()
