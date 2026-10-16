import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RESULTS_DIR = PROJECT_ROOT / "reports" / "results"
FIGURES_DIR = PROJECT_ROOT / "reports" / "figures"


def main():
    input_path = RESULTS_DIR / "model_sensitivity.csv"

    if not input_path.exists():
        raise FileNotFoundError(
            f"Results file not found: {input_path}. "
            "Run python -m src.model_sensitivity first."
        )

    df = pd.read_csv(input_path)

    required = ["Min_Samples_Leaf", "Estimated_Price_Effect"]
    missing = [column for column in required if column not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    df = df.sort_values("Min_Samples_Leaf")

    FIGURES_DIR.mkdir(parents=True, exist_ok=True)

    plt.figure(figsize=(8, 5))
    plt.plot(
        df["Min_Samples_Leaf"],
        df["Estimated_Price_Effect"],
        marker="o",
    )
    plt.xlabel("Minimum Samples per Leaf")
    plt.ylabel("Estimated Price Effect")
    plt.title("DML Price Effect Sensitivity to Model Configuration")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    output_path = FIGURES_DIR / "price_effect_sensitivity.png"
    plt.savefig(output_path, dpi=300)
    plt.close()

    print(f"Sensitivity chart saved to: {output_path}")


if __name__ == "__main__":
    main()