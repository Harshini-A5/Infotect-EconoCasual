
import pandas as pd
from pathlib import Path

print("EconoCausal: Dataset Inspection Started")

file_path = Path("data/raw/sales_data.csv")

if not file_path.exists():
    print("ERROR: CSV file not found!")
    print("Expected location:", file_path.resolve())

else:
    df = pd.read_csv(file_path)

    print("\n1. Dataset Shape:")
    print(df.shape)

    print("\n2. Column Names:")
    print(df.columns.tolist())

    print("\n3. First 5 Rows:")
    print(df.head().to_string())

    print("\n4. Missing Values:")
    print(df.isnull().sum().to_string())

    print("\n5. Data Types:")
    print(df.dtypes.to_string())

    print("\n6. Summary Statistics:")
    print(df.describe(include="all").to_string())

    print("\nDataset inspection completed!")

print("\n--- COMPLETE COLUMN NAMES ---")

for i, column in enumerate(df.columns, start=1):
    print(f"{i}. {column}")

print("\n--- FIRST 3 ROWS ---")
print(df.head(3).to_string(index=False))
