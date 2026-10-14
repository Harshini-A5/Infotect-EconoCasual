
import numpy as np
import pandas as pd

from src.model_config import DATA_PATH, TREATMENT
from src.treatment_model import train_treatment_model


def calculate_price_residuals():
    df = pd.read_csv(DATA_PATH)

    _, predicted_price, price_residuals = train_treatment_model()

    results = pd.DataFrame({
        "Actual_Price": df[TREATMENT].to_numpy(),
        "Predicted_Price": predicted_price,
        "Price_Residual": price_residuals,
    })

    print("Price residual calculation completed.")
    print(f"Rows processed: {len(results)}")
    print(f"Residual mean: {np.mean(price_residuals):.4f}")
    print(f"Residual standard deviation: {np.std(price_residuals):.4f}")
    print("\nSample results:")
    print(results.head())

    return results


if __name__ == "__main__":
    calculate_price_residuals()
