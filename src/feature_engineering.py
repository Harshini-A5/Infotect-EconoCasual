
from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent

INPUT_PATH = (
    PROJECT_ROOT / "data" / "processed" / "cleaned_sales_data.csv"
)

OUTPUT_PATH = (
    PROJECT_ROOT / "data" / "processed" / "featured_sales_data.csv"
)


def create_features():
    print("Loading cleaned dataset...")
    df = pd.read_csv(INPUT_PATH)

    print(f"Original shape: {df.shape}")

    # Calculate price difference from competitor pricing
    df["Price_Difference"] = (
        df["Price"] - df["Competitor Pricing"]
    )

    # Calculate price difference as a percentage of competitor pricing
    df["Price_Difference_Percent"] = (
        df["Price_Difference"]
        / df["Competitor Pricing"].replace(0, pd.NA)
    ) * 100

    # Create a discount indicator
    df["Has_Discount"] = (df["Discount"] > 0).astype(int)

    # Create a promotion indicator
    df["Has_Promotion"] = (df["Promotion"] > 0).astype(int)

    # Create a weekend indicator: Saturday = 5, Sunday = 6
    df["Is_Weekend"] = df["DayOfWeek"].isin([5, 6]).astype(int)

    # Create a season indicator for easier analysis
    df["Is_Summer"] = (
        df["Seasonality"].astype(str).str.lower() == "summer"
    ).astype(int)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_PATH, index=False)

    print("\nFeature engineering completed!")
    print(f"New shape: {df.shape}")
    print("\nNew features:")
    print(
        df[
            [
                "Price_Difference",
                "Price_Difference_Percent",
                "Has_Discount",
                "Has_Promotion",
                "Is_Weekend",
                "Is_Summer",
            ]
        ].head()
    )
    print(f"\nSaved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    create_features()

