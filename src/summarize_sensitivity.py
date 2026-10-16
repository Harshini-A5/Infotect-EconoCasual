import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RESULTS_DIR = PROJECT_ROOT / "reports" / "results"


def main():
    model_path = RESULTS_DIR / "model_sensitivity.csv"
    stability_path = RESULTS_DIR / "effect_stability.csv"

    if not model_path.exists() or not stability_path.exists():
        raise FileNotFoundError(
            "Required sensitivity CSV files were not found in reports/results."
        )

    model_results = pd.read_csv(model_path)
    stability_results = pd.read_csv(stability_path)

    print("\nMODEL CONFIGURATION SENSITIVITY")
    print(model_results.to_string(index=False))

    print("\nSAMPLE STABILITY")
    print(stability_results.to_string(index=False))

    combined_path = RESULTS_DIR / "combined_sensitivity_report.csv"

    model_results.insert(0, "Analysis_Type", "Model Configuration")
    stability_results.insert(0, "Analysis_Type", "Sample Stability")

    combined_results = pd.concat(
        [model_results, stability_results],
        ignore_index=True,
        sort=False,
    )

    combined_results.to_csv(combined_path, index=False)
    print(f"\nCombined report saved to: {combined_path}")


if __name__ == "__main__":
    main()