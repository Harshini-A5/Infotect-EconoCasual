
# import joblib
# import streamlit as st
# import pandas as pd
# from pathlib import Path

# PROJECT_ROOT = Path(__file__).resolve().parent
# MODEL_PATH = PROJECT_ROOT / "models" / "demand_prediction_model.joblib"

# st.set_page_config(
#     page_title="EconoCausal",
#     page_icon="📊",
#     layout="centered"
# )

# st.title("EconoCausal")
# st.subheader("Demand Prediction Dashboard")
# st.write(
#     "Enter market and product details to estimate customer demand."
# )

# @st.cache_resource
# def load_model():
#     saved = joblib.load(MODEL_PATH)
#     return saved["model"], saved["features"]

# try:
#     model, features = load_model()
# except FileNotFoundError:
#     st.error("Model file not found. Please train the model first.")
#     st.stop()

# with st.form("demand_prediction_form"):
#     st.subheader("Product and Market Details")

#     competitor_pricing = st.number_input(
#         "Competitor Pricing", min_value=0.0, value=100.0
#     )
#     promotion = st.selectbox("Promotion", [0, 1])
#     inventory_level = st.number_input(
#         "Inventory Level", min_value=0, value=100
#     )

#     seasonality = st.selectbox(
#         "Season", ["Autumn", "Spring", "Summer", "Winter"]
#     )
#     category = st.selectbox(
#         "Product Category",
#         ["Electronics", "Furniture", "Groceries", "Toys"]
#     )
#     region = st.selectbox(
#         "Region", ["North", "South", "West"]
#     )

#     submitted = st.form_submit_button("Predict Demand")

# if submitted:
#     input_data = {
#         "Competitor Pricing": competitor_pricing,
#         "Promotion": promotion,
#         "Inventory Level": inventory_level,
#         "Seasonality_Spring": int(seasonality == "Spring"),
#         "Seasonality_Summer": int(seasonality == "Summer"),
#         "Seasonality_Winter": int(seasonality == "Winter"),
#         "Category_Electronics": int(category == "Electronics"),
#         "Category_Furniture": int(category == "Furniture"),
#         "Category_Groceries": int(category == "Groceries"),
#         "Category_Toys": int(category == "Toys"),
#         "Region_North": int(region == "North"),
#         "Region_South": int(region == "South"),
#         "Region_West": int(region == "West"),
#     }

#     input_df = pd.DataFrame([input_data])[features]
#     prediction = model.predict(input_df)[0]

#     st.success(f"Estimated Demand: {prediction:.2f} units")
#     st.caption(
#         "This is a model-based estimate, not a guaranteed sales outcome."
#     )


import joblib
import streamlit as st
import pandas as pd
from pathlib import Path

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

# Load the demand prediction model
@st.cache_resource
def load_model():
    saved = joblib.load(MODEL_PATH)
    return saved["model"], saved["features"]

try:
    model, features = load_model()
except FileNotFoundError:
    st.error("Demand model not found. Please train the model first.")
    st.stop()

# Load the exported DML results
try:
    dml_results = pd.read_csv(DML_RESULTS_PATH)
    dml = dml_results.iloc[0]
except FileNotFoundError:
    st.error("DML results file not found in reports/results.")
    st.stop()
except (pd.errors.EmptyDataError, IndexError):
    st.error("The DML results file is empty.")
    st.stop()

# Demand prediction section
st.header("1. Demand Prediction")

with st.form("demand_prediction_form"):
    st.subheader("Product and Market Details")

    competitor_pricing = st.number_input(
        "Competitor Pricing",
        min_value=0.0,
        value=100.0
    )
    promotion = st.selectbox("Promotion", [0, 1])
    inventory_level = st.number_input(
        "Inventory Level",
        min_value=0,
        value=100
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

if submitted:
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

    input_df = pd.DataFrame([input_data])[features]
    prediction = model.predict(input_df)[0]

    st.success(f"Estimated Demand: {prediction:.2f} units")
    st.caption(
        "This is a model-based estimate, not a guaranteed sales outcome."
    )

# DML analysis section
st.divider()
st.header("2. DML Price-Effect Analysis")

st.write(
    "These statistics come from the saved DML analysis of your dataset. "
    "They are not recalculated for each form submission."
)

col1, col2, col3 = st.columns(3)

col1.metric(
    "Estimated Price Effect",
    f"{dml['Estimated_Price_Effect']:.4f}"
)
col2.metric(
    "Robust Standard Error",
    f"{dml['Robust_Standard_Error_HC1']:.4f}"
)
col3.metric(
    "Observations",
    f"{int(dml['Observations']):,}"
)

st.subheader("95% Confidence Interval")

lower = float(dml["CI_95_Lower"])
upper = float(dml["CI_95_Upper"])
estimate = float(dml["Estimated_Price_Effect"])

st.write(f"Lower bound: **{lower:.4f}**")
st.write(f"Estimated effect: **{estimate:.4f}**")
st.write(f"Upper bound: **{upper:.4f}**")

st.progress(1.0 if lower > 0 or upper < 0 else 0.0)

p_value = float(dml["P_Value"])
st.write(
    "P-value: **"
    + (f"{p_value:.2e}" if p_value != 0 else "Below the CSV's displayed precision")
    + "**"
)

st.caption(
    "Interpretation depends on how price treatment and demand outcome "
    "are defined. Statistical significance alone does not prove causality. "
    "The DML estimate is a dataset-level result, not a personalized "
    "price recommendation for the selected inputs."
)
