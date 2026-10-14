
import pandas as pd

from src.model_config import RESULTS_DIR


def export_results():
    estimate_path = RESULTS_DIR / "dml_estimate.csv"
    diagnostics_path = RESULTS_DIR / "model_diagnostics.csv"

    if not estimate_path.exists():
        raise FileNotFoundError(
            "DML estimate not found. Run python -m src.dml_estimator first."
        )

    if not diagnostics_path.exists():
        raise FileNotFoundError(
            "Diagnostics not found. Run python -m src.model_diagnostics first."
        )

    estimate = pd.read_csv(estimate_path)
    diagnostics = pd.read_csv(diagnostics_path)

    report = estimate.merge(
        diagnostics,
        on="Estimated_Price_Effect",
        how="left",
        suffixes=("_estimate", "_diagnostics"),
    )

    output_path = RESULTS_DIR / "final_dml_report.csv"
    report.to_csv(output_path, index=False)

    print("Final results report exported successfully.")
    print(f"Report location: {output_path}")
    print("\nReport preview:")
    print(report.to_string(index=False))


if __name__ == "__main__":
    export_results()

