import requests
import joblib
import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path
API_URL = "http://127.0.0.1:8000/predict"
# API_URL = "http://127.0.0.1:8001/predict"


def predict_demand_api(data):
    try:
        response = requests.post(
            API_URL,
            json=data,
            timeout=10
        )

        response.raise_for_status()
        result = response.json()

        if "predicted_demand" not in result:
            raise ValueError("Prediction missing from API response.")

        return result["predicted_demand"]

    except requests.exceptions.Timeout:
        st.error("The prediction service took too long to respond. Please try again.")
    except requests.exceptions.ConnectionError:
        st.error("Cannot connect to the prediction service. Please check whether FastAPI is running.")
    except requests.exceptions.HTTPError:
        st.error("The prediction service returned an error. Please try again.")
    except (ValueError, requests.exceptions.JSONDecodeError):
        st.error("The prediction service returned an invalid response.")
    except requests.exceptions.RequestException:
        st.error("A network error occurred while requesting the prediction.")

    return None

PROJECT_ROOT = Path(__file__).resolve().parent
MODEL_PATH = PROJECT_ROOT / "models" / "demand_prediction_model.joblib"
DML_RESULTS_PATH = (
    PROJECT_ROOT / "reports" / "results" / "robust_dml_inference.csv"
)

st.set_page_config(
    page_title="EconoCausal",
    page_icon="📊",
    layout="wide"
)

st.title("EconoCausal")
st.subheader("Dynamic Pricing and Demand Analysis")
st.write(
    "Explore predicted demand and the price-effect estimate "
    "calculated using Double Machine Learning (DML)."
)


# 1. Load the trained demand prediction model
@st.cache_resource
def load_model():
    saved = joblib.load(MODEL_PATH)

    if not isinstance(saved, dict) or "model" not in saved or "features" not in saved:
        raise ValueError(
            "Invalid model file. Please retrain the demand prediction model."
        )

    return saved["model"], saved["features"]


try:
    model, features = load_model()
except FileNotFoundError:
    st.error("Demand model not found. Please train the model first.")
    st.stop()
except Exception as exc:
    st.error(f"Could not load the demand model: {exc}")
    st.stop()


# 2. Load DML results
try:
    dml_results = pd.read_csv(DML_RESULTS_PATH)

    if dml_results.empty:
        st.error("The DML results file is empty.")
        st.stop()

    dml = dml_results.iloc[0]

except FileNotFoundError:
    st.error("DML results file not found in reports/results.")
    st.stop()
except (pd.errors.EmptyDataError, pd.errors.ParserError) as exc:
    st.error(f"Could not read the DML results file: {exc}")
    st.stop()


# 3. Demand prediction form
st.header("1. Demand Prediction")

with st.form("demand_prediction_form"):
    st.subheader("Product and Market Details")

    competitor_pricing = st.number_input(
        "Competitor Pricing",
        min_value=0.0,
        value=100.0,
        step=5.0
    )

    promotion = st.selectbox("Promotion", [0, 1])

    inventory_level = st.number_input(
        "Inventory Level",
        min_value=0,
        value=100,
        step=10
    )

    seasonality = st.selectbox(
        "Season",
        ["Autumn", "Spring", "Summer", "Winter"]
    )

    category = st.selectbox(
        "Product Category",
        ["Electronics", "Furniture", "Groceries", "Toys"]
    )

    region = st.selectbox(
        "Region",
        ["North", "South", "West"]
    )

    submitted = st.form_submit_button("Predict Demand")


# Always build the current inputs after the form.
# Both prediction features can use these inputs independently.
input_data = {
    "Competitor Pricing": competitor_pricing,
    "Promotion": promotion,
    "Inventory Level": inventory_level,
    "Seasonality_Spring": int(seasonality == "Spring"),
    "Seasonality_Summer": int(seasonality == "Summer"),
    "Seasonality_Winter": int(seasonality == "Winter"),
    "Category_Electronics": int(category == "Electronics"),
    "Category_Furniture": int(category == "Furniture"),
    "Category_Groceries": int(category == "Groceries"),
    "Category_Toys": int(category == "Toys"),
    "Region_North": int(region == "North"),
    "Region_South": int(region == "South"),
    "Region_West": int(region == "West"),
}

api_input = {
    "competitor_pricing": float(competitor_pricing),
    "promotion": int(promotion),
    "inventory_level": int(inventory_level),
    "seasonality": seasonality,
    "category": category,
    "region": region,
}


# 4. Prediction helper with input and output validation
def predict_demand(data_rows):
    input_frame = pd.DataFrame(data_rows)

    missing_features = [
        feature for feature in features
        if feature not in input_frame.columns
    ]

    if missing_features:
        raise ValueError(
            "Missing model features: " + ", ".join(missing_features)
        )

    input_frame = input_frame[features]
    predictions = np.asarray(model.predict(input_frame), dtype=float)

    if not np.isfinite(predictions).all():
        raise ValueError("The model returned an invalid prediction.")

    return predictions


# 5. Predict demand and compare promotion scenarios

if submitted:
    try:
        prediction = predict_demand_api(api_input)

        if prediction is None:
            st.stop()

        st.success(f"Estimated Demand: {prediction:.2f} units")

        st.caption(
            "This is a model-based estimate, not a guaranteed sales outcome."
        )

        no_promotion_data = input_data.copy()
        no_promotion_data["Promotion"] = 0

        promotion_data = input_data.copy()
        promotion_data["Promotion"] = 1

        comparison_predictions = predict_demand(
            [no_promotion_data, promotion_data]
        )

    except Exception as exc:
        st.error(f"Could not calculate demand prediction: {exc}")


# 6. Competitor pricing scenario comparison
st.header("2. Competitor Pricing vs. Predicted Demand")

st.write(
    "Compare predicted demand at different competitor-pricing levels "
    "while keeping the other selected product and market details unchanged."
)

price_range = st.slider(
    "Competitor Pricing Range",
    min_value=10,
    max_value=250,
    value=(50, 200),
    step=10
)

number_of_scenarios = st.slider(
    "Number of Price Scenarios",
    min_value=3,
    max_value=10,
    value=6
)

if st.button("Compare Price Scenarios"):
    try:
        scenario_prices = np.linspace(
            price_range[0],
            price_range[1],
            number_of_scenarios
        ).round(2).tolist()

        scenario_inputs = []

        for price in scenario_prices:
            scenario = input_data.copy()
            scenario["Competitor Pricing"] = float(price)
            scenario_inputs.append(scenario)

        scenario_predictions = predict_demand(scenario_inputs)

        price_comparison_df = pd.DataFrame({
            "Competitor Pricing": scenario_prices,
            "Predicted Demand": np.round(scenario_predictions, 2),
        })

        price_comparison_df["Demand Difference from First Scenario"] = (
            price_comparison_df["Predicted Demand"]
            - price_comparison_df["Predicted Demand"].iloc[0]
        ).round(2)

        st.subheader("Predicted Demand Across Pricing Scenarios")

        st.line_chart(
            price_comparison_df.set_index("Competitor Pricing")[
                "Predicted Demand"
            ]
        )

        best_scenario = price_comparison_df.loc[
            price_comparison_df["Predicted Demand"].idxmax()
        ]

        worst_scenario = price_comparison_df.loc[
            price_comparison_df["Predicted Demand"].idxmin()
        ]

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Highest Predicted Demand",
                f'{best_scenario["Predicted Demand"]:.2f}',
                f'Competitor Price: {best_scenario["Competitor Pricing"]:.2f}'
            )

        with col2:
            st.metric(
                "Lowest Predicted Demand",
                f'{worst_scenario["Predicted Demand"]:.2f}',
                f'Competitor Price: {worst_scenario["Competitor Pricing"]:.2f}'
            )

        st.caption(
            "These are model predictions under different competitor-pricing "
            "inputs. They do not establish the causal effect of your own "
            "product's selling price."
        )

    except Exception as exc:
        st.error(f"Could not compare pricing scenarios: {exc}")


# 7. Double Machine Learning results
st.header("3. Double Machine Learning (DML) Price Effect")

required_columns = [
    "Estimated_Price_Effect",
    "Robust_Standard_Error_HC1",
    "CI_95_Lower",
    "CI_95_Upper",
    "Observations",
    "P_Value"
]

missing_columns = [
    column for column in required_columns
    if column not in dml_results.columns
]

if missing_columns:
    st.warning(
        "DML summary is missing required columns: "
        + ", ".join(missing_columns)
    )

else:
    try:
        effect = float(dml["Estimated_Price_Effect"])
        standard_error = float(dml["Robust_Standard_Error_HC1"])
        ci_lower = float(dml["CI_95_Lower"])
        ci_upper = float(dml["CI_95_Upper"])
        observations = int(dml["Observations"])
        p_value = float(dml["P_Value"])

        values = [
            effect, standard_error, ci_lower, ci_upper, p_value
        ]

        if not np.isfinite(values).all():
            raise ValueError("Some DML results contain invalid numbers.")

        col1, col2, col3 = st.columns(3)

        col1.metric("Estimated Price Effect", f"{effect:.4f}")
        col2.metric("Robust Standard Error", f"{standard_error:.4f}")
        col3.metric("Observations", f"{observations:,}")

        st.write(
            f"**95% Confidence Interval:** "
            f"{ci_lower:.4f} to {ci_upper:.4f}"
        )

        if p_value == 0:
            st.write("**P-value:** Below the CSV's displayed precision")
        else:
            st.write(f"**P-value:** {p_value:.6g}")

        st.caption(
            "Interpretation depends on the data and model assumptions. "
            "Statistical significance alone does not prove causality. "
            "This is a dataset-level estimate."
        )

    except (ValueError, TypeError, OverflowError) as exc:
        st.warning(f"Could not display the DML results: {exc}")
