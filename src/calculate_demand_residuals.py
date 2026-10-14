
import numpy as np
import pandas as pd

from src.model_config import DATA_PATH, OUTCOME
from src.demand_model import train_demand_model


def calculate_demand_residuals():
    df = pd.read_csv(DATA_PATH)

    _, predicted_demand, demand_residuals = train_demand_model()

    results = pd.DataFrame({
        "Actual_Demand": df[OUTCOME].to_numpy(),
        "Predicted_Demand": predicted_demand,
        "Demand_Residual": demand_residuals,
    })

    print("Demand residual calculation completed.")
    print(f"Rows processed: {len(results)}")
    print(f"Residual mean: {np.mean(demand_residuals):.4f}")
    print(f"Residual standard deviation: {np.std(demand_residuals):.4f}")
    print("\nSample results:")
    print(results.head())

    return results


if __name__ == "__main__":
    calculate_demand_residuals()
