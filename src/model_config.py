
from pathlib import Path

# Project paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "dml_ready_data.csv"
)

RESULTS_DIR = PROJECT_ROOT / "reports" / "results"

# Double Machine Learning variables
TREATMENT = "Price"
OUTCOME = "Demand"

# Candidate observed confounders
CONFOUNDERS = [
    "Competitor Pricing",
    "Promotion",
    "Inventory Level",
    "Seasonality_Spring",
    "Seasonality_Summer",
    "Seasonality_Winter",
    "Category_Electronics",
    "Category_Furniture",
    "Category_Groceries",
    "Category_Toys",
    "Region_North",
    "Region_South",
    "Region_West",
]

RANDOM_STATE = 42
TEST_SIZE = 0.2
