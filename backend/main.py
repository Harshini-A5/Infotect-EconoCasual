
from pathlib import Path

import joblib
import pandas as pd
import numpy as np
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

PROJECT_ROOT = Path(__file__).resolve().parent.parent
MODEL_PATH = PROJECT_ROOT / "models" / "demand_prediction_model.joblib"

app = FastAPI(
    title="EconoCausal API",
    description="Demand prediction API for the EconoCausal project",
    version="1.0.0",
)


def load_model():
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Trained model not found at: {MODEL_PATH}"
        )

    saved = joblib.load(MODEL_PATH)

    if not isinstance(saved, dict) or "model" not in saved or "features" not in saved:
        raise ValueError(
            "Invalid model file. Expected a dictionary with model and features."
        )

    return saved["model"], saved["features"]


try:
    model, features = load_model()
except Exception as exc:
    model = None
    features = None
    MODEL_LOAD_ERROR = str(exc)
else:
    MODEL_LOAD_ERROR = None


class DemandInput(BaseModel):
    competitor_pricing: float = Field(ge=0)
    promotion: int = Field(ge=0, le=1)
    inventory_level: int = Field(ge=0)
    seasonality: str
    category: str
    region: str


@app.get("/")
def home():
    return {
        "message": "Welcome to the EconoCausal API",
        "docs": "/docs",
    }


# @app.get("/debug-model")
def debug_model():
    return {
        "project_root": str(PROJECT_ROOT),
        "model_path": str(MODEL_PATH),
        "project_root_exists": PROJECT_ROOT.exists(),
        "model_exists": MODEL_PATH.exists(),
        "models_folder_exists": MODEL_PATH.parent.exists(),
        "root_files": [p.name for p in PROJECT_ROOT.iterdir()],
    }

@app.post("/predict")
def predict_demand(data: DemandInput):
    if model is None or features is None:
        raise HTTPException(
            status_code=503,
            detail=f"Demand model is unavailable: {MODEL_LOAD_ERROR}",
        )

    valid_seasons = {"Autumn", "Spring", "Summer", "Winter"}
    valid_categories = {"Electronics", "Furniture", "Groceries", "Toys"}
    valid_regions = {"North", "South", "West"}

    if data.seasonality not in valid_seasons:
        raise HTTPException(status_code=422, detail="Invalid seasonality value.")

    if data.category not in valid_categories:
        raise HTTPException(status_code=422, detail="Invalid category value.")

    if data.region not in valid_regions:
        raise HTTPException(status_code=422, detail="Invalid region value.")

    input_data = {
        "Competitor Pricing": data.competitor_pricing,
        "Promotion": data.promotion,
        "Inventory Level": data.inventory_level,
        "Seasonality_Spring": int(data.seasonality == "Spring"),
        "Seasonality_Summer": int(data.seasonality == "Summer"),
        "Seasonality_Winter": int(data.seasonality == "Winter"),
        "Category_Electronics": int(data.category == "Electronics"),
        "Category_Furniture": int(data.category == "Furniture"),
        "Category_Groceries": int(data.category == "Groceries"),
        "Category_Toys": int(data.category == "Toys"),
        "Region_North": int(data.region == "North"),
        "Region_South": int(data.region == "South"),
        "Region_West": int(data.region == "West"),
    }

    try:
        input_frame = pd.DataFrame([input_data])

        missing_features = [
            feature for feature in features
            if feature not in input_frame.columns
        ]

        if missing_features:
            raise ValueError(
                "Missing model features: " + ", ".join(missing_features)
            )

        input_frame = input_frame[features]
        prediction = float(np.asarray(model.predict(input_frame))[0])

        if not np.isfinite(prediction):
            raise ValueError("Model returned an invalid prediction.")

        return {
            "predicted_demand": round(prediction, 2),
            "unit": "units",
            "note": "This is a model-based estimate, not a guaranteed sales outcome.",
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Demand prediction failed: {exc}",
        ) from exc
