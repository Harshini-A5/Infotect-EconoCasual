import os
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import requests
import streamlit as st
import matplotlib.pyplot as plt


# =========================================================
# 1. PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="EconoCausal Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

PROJECT_ROOT = Path(__file__).resolve().parent

MODEL_PATH = PROJECT_ROOT / "models" / "demand_prediction_model.joblib"

DML_RESULTS_PATH = (
    PROJECT_ROOT / "reports" / "results" / "robust_dml_inference.csv"
)

API_URL = os.getenv(
    "API_URL",
    "https://econocausal-api.onrender.com/predict",
)


# =========================================================
# 2. PROFESSIONAL DASHBOARD DESIGN
# =========================================================

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    :root {
        --navy: #102a43;
        --navy-2: #173f5f;
        --blue: #246b9e;
        --blue-soft: #eaf3fa;
        --ink: #172b3a;
        --muted: #647789;
        --line: #e2e9f0;
        --surface: #ffffff;
        --canvas: #f5f7fa;
    }

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background: var(--canvas);
        color: var(--ink);
    }

    [data-testid="stHeader"] {
        background: rgba(245, 247, 250, 0.96);
    }

    .block-container {
        max-width: 1440px;
        padding-top: 1.35rem;
        padding-bottom: 2.5rem;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: #102a43;
        border-right: 1px solid rgba(255,255,255,0.08);
    }

    [data-testid="stSidebar"] > div:first-child {
        padding-top: 1.5rem;
    }

    [data-testid="stSidebar"] * {
        color: #edf4fa;
    }

    .brand {
        padding: 9px 7px 23px 7px;
    }

    .brand-name {
        font-size: 23px;
        font-weight: 800;
        letter-spacing: -0.7px;
        color: #ffffff;
    }

    .brand-subtitle {
        color: #b8cbd9;
        font-size: 11px;
        letter-spacing: 0.35px;
        margin-top: 6px;
    }

    [data-testid="stSidebar"] [data-testid="stRadio"] > label {
        color: #a9bfd0;
        font-size: 10px;
        font-weight: 700;
        letter-spacing: 1.2px;
        margin-bottom: 10px;
    }

    [data-testid="stSidebar"] [data-testid="stRadio"] div[role="radiogroup"] {
        gap: 6px;
    }

    [data-testid="stSidebar"] [data-testid="stRadio"] div[role="radiogroup"] label {
        border-radius: 8px;
        padding: 9px 11px;
        transition: background 0.15s ease;
    }

    [data-testid="stSidebar"] [data-testid="stRadio"] div[role="radiogroup"] label:hover {
        background: rgba(255,255,255,0.09);
    }

    [data-testid="stSidebar"] [data-testid="stRadio"] div[role="radiogroup"] label:has(input:checked) {
        background: #245779;
        border-left: 3px solid #80c4ee;
    }

    [data-testid="stSidebar"] [data-testid="stRadio"] div[role="radiogroup"] label p {
        font-size: 13px;
        font-weight: 600;
    }

    [data-testid="stSidebar"] hr {
        border-color: rgba(255,255,255,0.14);
    }

    [data-testid="stSidebar"] [data-testid="stCaptionContainer"] p {
        color: #9fb5c7;
        font-size: 10px;
        letter-spacing: 0.8px;
        font-weight: 700;
    }

    /* Main page header */
    .hero {
        position: relative;
        overflow: hidden;
        background: linear-gradient(112deg, #102a43 0%, #174a70 62%, #236b96 100%);
        padding: 30px 34px;
        border-radius: 15px;
        color: white;
        margin-bottom: 27px;
        box-shadow: 0 8px 24px rgba(16,42,67,0.12);
    }

    .hero:after {
        content: "";
        position: absolute;
        width: 230px;
        height: 230px;
        right: -65px;
        top: -125px;
        border: 1px solid rgba(255,255,255,0.13);
        border-radius: 50%;
        box-shadow: 0 0 0 24px rgba(255,255,255,0.035),
                    0 0 0 50px rgba(255,255,255,0.025);
    }

    .hero-eyebrow {
        color: #b9d8ec;
        font-size: 10px;
        font-weight: 700;
        letter-spacing: 1.6px;
        text-transform: uppercase;
        margin-bottom: 9px;
    }

    .hero h1 {
        color: #ffffff;
        font-size: clamp(24px, 3vw, 31px);
        font-weight: 800;
        letter-spacing: -0.9px;
        line-height: 1.2;
        margin: 0 0 9px 0;
    }

    .hero p {
        color: #dceaf4;
        font-size: 12px;
        line-height: 1.6;
        margin: 0;
        max-width: 760px;
    }

    /* Page hierarchy */
    .page-heading {
        font-size: 24px;
        font-weight: 750;
        letter-spacing: -0.55px;
        color: var(--navy);
        margin-bottom: 5px;
    }

    .page-description {
        color: var(--muted);
        font-size: 12px;
        line-height: 1.6;
        margin-bottom: 21px;
    }

    .section-heading {
        font-size: 17px;
        font-weight: 700;
        letter-spacing: -0.25px;
        color: var(--navy);
        margin-top: 19px;
        margin-bottom: 13px;
    }

    h3, h4 {
        color: var(--navy) !important;
        font-weight: 700 !important;
        letter-spacing: -0.25px !important;
    }

    /* KPI cards */
    div[data-testid="stMetric"] {
        background: var(--surface);
        border: 1px solid var(--line);
        border-radius: 11px;
        padding: 17px 18px;
        min-height: 98px;
        box-shadow: 0 2px 7px rgba(16,42,67,0.035);
        transition: box-shadow 0.15s ease, transform 0.15s ease;
    }

    div[data-testid="stMetric"]:hover {
        box-shadow: 0 5px 15px rgba(16,42,67,0.075);
        transform: translateY(-1px);
    }

    div[data-testid="stMetric"] label {
        color: var(--muted) !important;
        font-weight: 600 !important;
        font-size: 11px !important;
    }

    div[data-testid="stMetric"] [data-testid="stMetricValue"] {
        color: var(--navy) !important;
        font-weight: 750 !important;
        font-size: clamp(19px, 2vw, 25px) !important;
        letter-spacing: -0.6px;
        line-height: 1.25;
        overflow-wrap: anywhere;
    }

    div[data-testid="stMetric"] [data-testid="stMetricDelta"] {
        font-size: 11px;
    }

    /* Content surfaces */
    div[data-testid="stForm"] {
        background: var(--surface);
        border: 1px solid var(--line);
        border-radius: 13px;
        padding: 22px 23px;
        box-shadow: 0 2px 8px rgba(16,42,67,0.025);
    }

    div[data-testid="stTextInput"] input,
    div[data-testid="stNumberInput"] input,
    div[data-testid="stSelectbox"] > div > div {
        border-radius: 7px;
    }

    div.stButton > button,
    div[data-testid="stFormSubmitButton"] > button {
        background: var(--navy-2);
        color: white;
        border: 1px solid var(--navy-2);
        border-radius: 7px;
        min-height: 42px;
        font-size: 13px;
        font-weight: 650;
        transition: background 0.15s ease, border-color 0.15s ease;
    }

    div.stButton > button:hover,
    div[data-testid="stFormSubmitButton"] > button:hover {
        background: var(--blue);
        color: white;
        border-color: var(--blue);
    }

    div[data-testid="stDataFrame"] {
        border: 1px solid var(--line);
        border-radius: 9px;
        overflow: hidden;
    }

    div[data-testid="stAlert"] {
        border-radius: 9px;
    }

    /* Insight cards */
    .insight-card {
        background: var(--surface);
        padding: 17px 19px;
        border: 1px solid var(--line);
        border-left: 3px solid #5b9bc4;
        border-radius: 9px;
        margin-bottom: 11px;
        box-shadow: 0 2px 7px rgba(16,42,67,0.025);
    }

    .insight-title {
        color: var(--navy-2);
        font-weight: 700;
        font-size: 12px;
        letter-spacing: 0.1px;
        margin-bottom: 6px;
    }

    .insight-text {
        color: #5d7081;
        font-size: 11px;
        line-height: 1.65;
    }

    /* Charts and separators */
    [data-testid="stVerticalBlock"] > [data-testid="stElementContainer"] hr {
        border-color: var(--line);
        margin-top: 1.25rem;
        margin-bottom: 1.25rem;
    }

    [data-testid="stCaptionContainer"] p {
        color: #8291a0;
        font-size: 10px;
        line-height: 1.5;
    }

    .footer {
        color: #8795a3;
        text-align: center;
        font-size: 10px;
        padding-top: 30px;
        letter-spacing: 0.15px;
    }

    @media (max-width: 800px) {
        .block-container {
            padding-top: 1rem;
            padding-left: 1rem;
            padding-right: 1rem;
        }
        .hero {
            padding: 23px 22px;
        }
        div[data-testid="stMetric"] {
            padding: 13px;
            min-height: 86px;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# 3. LOAD MODEL AND DML RESULTS
# =========================================================

@st.cache_resource
def load_model():

    saved = joblib.load(MODEL_PATH)

    if (
        not isinstance(saved, dict)
        or "model" not in saved
        or "features" not in saved
    ):
        raise ValueError("Invalid demand prediction model.")

    return saved["model"], saved["features"]


@st.cache_data
def load_dml_results():

    results = pd.read_csv(DML_RESULTS_PATH)

    if results.empty:
        raise ValueError("DML results file is empty.")

    return results


try:
    model, features = load_model()

except FileNotFoundError:
    st.error("Demand prediction model not found.")
    st.stop()

except Exception as exc:
    st.error(f"Model loading error: {exc}")
    st.stop()


try:
    dml_results = load_dml_results()
    dml = dml_results.iloc[0]

except FileNotFoundError:
    st.error("DML results file not found.")
    st.stop()

except Exception as exc:
    st.error(f"DML results loading error: {exc}")
    st.stop()


# =========================================================
# 4. VALIDATE DML VALUES
# =========================================================

required_columns = [
    "Estimated_Price_Effect",
    "Robust_Standard_Error_HC1",
    "CI_95_Lower",
    "CI_95_Upper",
    "Observations",
    "P_Value",
]

missing_columns = [
    column for column in required_columns
    if column not in dml_results.columns
]

if missing_columns:
    st.error(
        "Missing DML result columns: "
        + ", ".join(missing_columns)
    )
    st.stop()


try:
    effect = float(dml["Estimated_Price_Effect"])
    standard_error = float(dml["Robust_Standard_Error_HC1"])
    ci_lower = float(dml["CI_95_Lower"])
    ci_upper = float(dml["CI_95_Upper"])
    observations = int(dml["Observations"])
    p_value = float(dml["P_Value"])

    if not np.isfinite([
        effect,
        standard_error,
        ci_lower,
        ci_upper,
        p_value,
    ]).all():
        raise ValueError("DML results contain invalid numerical values.")

    if ci_lower > effect or effect > ci_upper:
        raise ValueError("Invalid DML confidence interval.")

except (ValueError, TypeError, OverflowError) as exc:
    st.error(f"Invalid DML results: {exc}")
    st.stop()


# =========================================================
# 5. PREDICTION FUNCTIONS
# =========================================================

def predict_demand_api(data):

    try:
        response = requests.post(
            API_URL,
            json=data,
            timeout=60,
        )

        response.raise_for_status()

        result = response.json()

        if "predicted_demand" not in result:
            raise ValueError("Prediction missing from API response.")

        prediction = float(result["predicted_demand"])

        if not np.isfinite(prediction):
            raise ValueError("Invalid prediction returned by API.")

        return prediction

    except requests.exceptions.Timeout:
        st.error("Prediction service timed out. Please try again.")

    except requests.exceptions.ConnectionError:
        st.error("Cannot connect to the prediction service.")

    except requests.exceptions.HTTPError as exc:
        status = (
            exc.response.status_code
            if exc.response is not None
            else "Unknown"
        )
        detail = (
            exc.response.text[:500]
            if exc.response is not None
            else str(exc)
        )
        st.error(f"API error ({status}): {detail}")

    except (ValueError, requests.exceptions.JSONDecodeError) as exc:
        st.error(f"Invalid API response: {exc}")

    except requests.exceptions.RequestException as exc:
        st.error(f"Network error: {exc}")

    return None


def predict_demand(data_rows):

    input_frame = pd.DataFrame(data_rows)

    missing = [
        feature for feature in features
        if feature not in input_frame.columns
    ]

    if missing:
        raise ValueError(
            "Missing model features: " + ", ".join(missing)
        )

    input_frame = input_frame[features]

    predictions = np.asarray(
        model.predict(input_frame),
        dtype=float,
    )

    if not np.isfinite(predictions).all():
        raise ValueError("Model returned invalid predictions.")

    return predictions


# =========================================================
# 6. SESSION STATE
# =========================================================

if "last_prediction" not in st.session_state:
    st.session_state.last_prediction = None

if "last_promotion_comparison" not in st.session_state:
    st.session_state.last_promotion_comparison = None

if "scenario_results" not in st.session_state:
    st.session_state.scenario_results = None

if "prediction_inputs" not in st.session_state:
    st.session_state.prediction_inputs = None


# =========================================================
# 7. SIDEBAR NAVIGATION
# =========================================================

with st.sidebar:

    st.markdown(
        """
        <div class="brand">
            <div class="brand-name">📊 EconoCausal</div>
            <div class="brand-subtitle">
                Dynamic Pricing Analytics
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("---")

    page = st.radio(
        "MAIN MENU",
        [
            "Overview",
            "Demand Prediction",
            "Scenario Analysis",
            "Causal Insights",
        ],
        label_visibility="visible",
    )

    st.markdown("---")

    st.caption("PROJECT")

    st.write("Double Machine Learning")

    st.caption("Retail Demand Analysis")


# =========================================================
# 8. DASHBOARD HEADER
# =========================================================

st.markdown(
    """
    <div class="hero">
        <div class="hero-eyebrow">EconoCausal Analytics Platform</div>
        <h1>Dynamic Pricing &amp; Demand Analytics</h1>
        <p>
            Understand demand patterns, evaluate pricing scenarios,
            and explore causal evidence with machine learning.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# 9. OVERVIEW PAGE
# =========================================================

if page == "Overview":

    st.markdown(
        '<div class="page-heading">Dashboard Overview</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="page-description">'
        'A summary of the demand forecasting and causal analysis results.'
        '</div>',
        unsafe_allow_html=True,
    )

    # Main KPI cards

    kpi1, kpi2, kpi3, kpi4 = st.columns(4)

    kpi1.metric(
        "Dataset Observations",
        f"{observations:,}",
    )

    kpi2.metric(
        "Estimated Price Effect",
        f"{effect:.4f}",
    )

    kpi3.metric(
        "Robust Standard Error",
        f"{standard_error:.4f}",
    )

    p_value_text = (
        "Below displayed precision"
        if p_value == 0
        else f"{p_value:.4g}"
    )

    kpi4.metric(
        "P-value",
        p_value_text,
    )

    st.markdown(
        '<div class="section-heading">Analysis Overview</div>',
        unsafe_allow_html=True,
    )

    left, right = st.columns([1.4, 1])

    with left:

        st.markdown("#### Price Effect with 95% Confidence Interval")

        fig, ax = plt.subplots(figsize=(8, 3))

        ax.errorbar(
            effect,
            0,
            xerr=[
                [effect - ci_lower],
                [ci_upper - effect],
            ],
            fmt="o",
            markersize=10,
            capsize=9,
            linewidth=3,
            color="#2878A8",
        )

        ax.axvline(
            0,
            linestyle="--",
            color="#d9534f",
            alpha=0.8,
        )

        ax.set_yticks([0])
        ax.set_yticklabels(["Price effect"])

        ax.set_xlabel("Estimated effect")
        ax.grid(axis="x", alpha=0.2)

        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_visible(False)

        fig.tight_layout()

        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

        st.caption(
            f"95% CI: {ci_lower:.4f} to {ci_upper:.4f}"
        )

    with right:

        st.markdown("#### Key Project Insights")

        st.markdown(
            f"""
            <div class="insight-card">
                <div class="insight-title">
                    Price Effect
                </div>
                <div class="insight-text">
                    Estimated price effect is {effect:.4f}.
                    This is the DML estimate from the project analysis.
                </div>
            </div>

            <div class="insight-card">
                <div class="insight-title">
                    Statistical Evidence
                </div>
                <div class="insight-text">
                    P-value: {p_value_text}.
                    Statistical significance should be interpreted
                    alongside the model assumptions.
                </div>
            </div>

            <div class="insight-card">
                <div class="insight-title">
                    Data Coverage
                </div>
                <div class="insight-text">
                    The DML analysis uses {observations:,} observations.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("---")

    st.markdown(
        '<div class="section-heading">Latest Prediction</div>',
        unsafe_allow_html=True,
    )

    if st.session_state.last_prediction is not None:

        st.metric(
            "Most Recent Predicted Demand",
            f"{st.session_state.last_prediction:.2f} units",
        )

        st.caption(
            "This value comes from your most recent successful prediction."
        )

    else:

        st.info(
            "No prediction has been generated in this session yet. "
            "Open Demand Prediction to get started."
        )

    st.markdown(
        '<div class="footer">'
        'EconoCausal | Dynamic Pricing via Double Machine Learning'
        '</div>',
        unsafe_allow_html=True,
    )
# =========================================================
# 10. DEMAND PREDICTION PAGE
# =========================================================

elif page == "Demand Prediction":

    st.markdown(
        '<div class="page-heading">Demand Prediction</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="page-description">'
        'Enter product and market details to estimate demand.'
        '</div>',
        unsafe_allow_html=True,
    )

    with st.form("prediction_form"):

        st.markdown("#### Product and Market Details")

        col1, col2, col3 = st.columns(3)

        with col1:

            competitor_pricing = st.number_input(
                "Competitor Pricing",
                min_value=0.0,
                value=100.0,
                step=5.0,
            )

            promotion = st.selectbox(
                "Promotion",
                [0, 1],
                format_func=lambda x: "Yes" if x == 1 else "No",
            )

        with col2:

            inventory_level = st.number_input(
                "Inventory Level",
                min_value=0,
                value=100,
                step=10,
            )

            seasonality = st.selectbox(
                "Season",
                ["Autumn", "Spring", "Summer", "Winter"],
            )

        with col3:

            category = st.selectbox(
                "Product Category",
                ["Electronics", "Furniture", "Groceries", "Toys"],
            )

            region = st.selectbox(
                "Region",
                ["North", "South", "West"],
            )

        submitted = st.form_submit_button(
            "Generate Demand Prediction",
            use_container_width=True,
        )

    # Model input features

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

    if submitted:

        prediction = predict_demand_api(api_input)

        if prediction is not None:

            st.session_state.last_prediction = prediction
            st.session_state.prediction_inputs = input_data.copy()

            no_promo = input_data.copy()
            no_promo["Promotion"] = 0

            with_promo = input_data.copy()
            with_promo["Promotion"] = 1

            try:

                promo_predictions = predict_demand(
                    [no_promo, with_promo]
                )

                st.session_state.last_promotion_comparison = {
                    "without": float(promo_predictions[0]),
                    "with": float(promo_predictions[1]),
                }

            except Exception as exc:

                st.session_state.last_promotion_comparison = None
                st.warning(f"Promotion comparison unavailable: {exc}")

    # Display stored prediction

    if st.session_state.last_prediction is not None:

        st.markdown("---")

        st.markdown("#### Prediction Results")

        result1, result2, result3 = st.columns(3)

        result1.metric(
            "Predicted Demand",
            f"{st.session_state.last_prediction:.2f} units",
        )

        result2.metric(
            "Promotion",
            "Yes" if promotion == 1 else "No",
        )

        result3.metric(
            "Competitor Pricing",
            f"{competitor_pricing:.2f}",
        )

        st.caption(
            "This prediction is generated by the deployed demand prediction API."
        )

        # Visualize the actual prediction returned by the deployed API.
        st.markdown("#### Estimated Demand Visualization")

        estimated_demand = float(st.session_state.last_prediction)
        chart_padding = max(abs(estimated_demand) * 0.12, 1.0)

        fig, ax = plt.subplots(figsize=(9, 2.6))

        ax.barh(
            ["Predicted demand"],
            [estimated_demand],
            color="#2878A8",
            height=0.42,
        )

        ax.axvline(0, color="#647789", linewidth=0.9, alpha=0.7)
        ax.set_xlim(
            min(0, estimated_demand - chart_padding),
            max(0, estimated_demand + chart_padding),
        )
        ax.set_xlabel("Estimated units")
        ax.set_ylabel("")
        ax.set_title("Demand predicted for the selected product and market")

        label_offset = chart_padding * 0.06
        ax.text(
            estimated_demand + (label_offset if estimated_demand >= 0 else -label_offset),
            0,
            f"{estimated_demand:,.2f} units",
            va="center",
            ha="left" if estimated_demand >= 0 else "right",
            fontweight="bold",
            color="#102A43",
        )

        ax.grid(axis="x", alpha=0.2)
        ax.set_axisbelow(True)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_visible(False)
        fig.tight_layout()

        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

        st.caption(
            "The bar shows the actual demand estimate returned by the API for "
            "the inputs above. It is a prediction, not a causal price-effect estimate."
        )

        comparison = st.session_state.last_promotion_comparison

        if comparison is not None:

            st.markdown("#### Promotion Comparison")

            without_promo = comparison["without"]
            with_promo = comparison["with"]

            difference = with_promo - without_promo

            pc1, pc2, pc3 = st.columns(3)

            pc1.metric(
                "Without Promotion",
                f"{without_promo:.2f} units",
            )

            pc2.metric(
                "With Promotion",
                f"{with_promo:.2f} units",
            )

            pc3.metric(
                "Predicted Difference",
                f"{difference:+.2f} units",
            )

            promo_df = pd.DataFrame({
                "Scenario": [
                    "Without Promotion",
                    "With Promotion",
                ],
                "Predicted Demand": [
                    without_promo,
                    with_promo,
                ],
            })

            st.bar_chart(
                promo_df.set_index("Scenario"),
                color="#2878A8",
                use_container_width=True,
            )

            st.caption(
                "This chart compares two model predictions while keeping "
                "the other selected inputs unchanged. It is not a separate "
                "causal estimate."
            )

    else:

        st.info(
            "Enter the details above and generate a prediction to see your results."
        )

    st.markdown(
        '<div class="footer">'
        'EconoCausal | Demand Prediction'
        '</div>',
        unsafe_allow_html=True,
    )
# =========================================================
# 11. SCENARIO ANALYSIS PAGE
# =========================================================

elif page == "Scenario Analysis":

    st.markdown(
        '<div class="page-heading">Pricing Scenario Analysis</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="page-description">'
        'Compare predicted demand at different competitor-pricing levels.'
        '</div>',
        unsafe_allow_html=True,
    )

    if st.session_state.prediction_inputs is None:

        st.info(
            "First generate a prediction in the Demand Prediction section. "
            "The selected product and market inputs will be used here."
        )

    else:

        st.markdown("#### Configure Pricing Scenarios")

        col1, col2 = st.columns(2)

        with col1:

            price_range = st.slider(
                "Competitor Pricing Range",
                min_value=10,
                max_value=250,
                value=(50, 200),
                step=10,
            )

        with col2:

            scenario_count = st.slider(
                "Number of Scenarios",
                min_value=3,
                max_value=10,
                value=6,
            )

        if st.button(
            "Run Scenario Analysis",
            use_container_width=True,
        ):

            try:

                prices = np.linspace(
                    price_range[0],
                    price_range[1],
                    scenario_count,
                ).round(2)

                scenario_inputs = []

                for price in prices:

                    scenario = st.session_state.prediction_inputs.copy()

                    scenario["Competitor Pricing"] = float(price)

                    scenario_inputs.append(scenario)

                predictions = predict_demand(scenario_inputs)

                scenario_df = pd.DataFrame({
                    "Competitor Pricing": prices,
                    "Predicted Demand": np.round(predictions, 2),
                })

                scenario_df[
                    "Demand Difference from First Scenario"
                ] = (
                    scenario_df["Predicted Demand"]
                    - scenario_df["Predicted Demand"].iloc[0]
                ).round(2)

                st.session_state.scenario_results = scenario_df

            except Exception as exc:

                st.error(f"Scenario analysis failed: {exc}")

        if st.session_state.scenario_results is not None:

            scenario_df = st.session_state.scenario_results

            st.markdown("---")

            st.markdown("#### Demand Across Pricing Levels")

            st.line_chart(
                scenario_df.set_index("Competitor Pricing")[
                    "Predicted Demand"
                ],
                color="#2878A8",
                use_container_width=True,
            )

            best = scenario_df.loc[
                scenario_df["Predicted Demand"].idxmax()
            ]

            worst = scenario_df.loc[
                scenario_df["Predicted Demand"].idxmin()
            ]

            best_col, worst_col = st.columns(2)

            best_col.metric(
                "Highest Predicted Demand",
                f'{best["Predicted Demand"]:.2f} units',
            )

            best_col.caption(
                f'Competitor pricing: {best["Competitor Pricing"]:.2f}'
            )

            worst_col.metric(
                "Lowest Predicted Demand",
                f'{worst["Predicted Demand"]:.2f} units',
            )

            worst_col.caption(
                f'Competitor pricing: {worst["Competitor Pricing"]:.2f}'
            )

            st.markdown("#### Scenario Comparison Table")

            st.dataframe(
                scenario_df,
                use_container_width=True,
                hide_index=True,
            )

            st.caption(
                "These are model-based scenario predictions. Only competitor "
                "pricing changes; other selected inputs remain fixed. "
                "This graph does not represent the DML causal price effect."
            )

    st.markdown(
        '<div class="footer">'
        'EconoCausal | Scenario Analysis'
        '</div>',
        unsafe_allow_html=True,
    )
# =========================================================
# 12. CAUSAL INSIGHTS PAGE
# =========================================================

elif page == "Causal Insights":

    st.markdown(
        '<div class="page-heading">Causal Insights</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="page-description">'
        'Understand the estimated price effect using Double Machine Learning.'
        '</div>',
        unsafe_allow_html=True,
    )

    # Main result cards

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Estimated Price Effect",
        f"{effect:.4f}",
    )

    c2.metric(
        "Robust Standard Error",
        f"{standard_error:.4f}",
    )

    c3.metric(
        "Observations",
        f"{observations:,}",
    )

    # Format p-value for display
    p_value_text = f"{p_value:.2e}" if p_value > 0 else "< 1e-300"

    c4.metric(
        "P-value",
        p_value_text,
    )

    st.markdown("---")

    st.markdown("#### Estimated Price Effect")

    fig, ax = plt.subplots(figsize=(10, 3.5))

    ax.errorbar(
        effect,
        0,
        xerr=[
            [effect - ci_lower],
            [ci_upper - effect],
        ],
        fmt="o",
        markersize=12,
        capsize=10,
        linewidth=4,
        color="#2878A8",
    )

    ax.axvline(
        0,
        linestyle="--",
        color="#d9534f",
        linewidth=1.5,
        label="Zero effect",
    )

    ax.set_yticks([0])
    ax.set_yticklabels(["DML Price Effect"])

    ax.set_xlabel("Estimated Effect")
    ax.set_title("95% Confidence Interval")

    ax.grid(axis="x", alpha=0.2)
    ax.legend()

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)

    fig.tight_layout()

    st.pyplot(fig, use_container_width=True)

    plt.close(fig)

    lower_col, upper_col = st.columns(2)

    lower_col.metric(
        "95% CI Lower Bound",
        f"{ci_lower:.4f}",
    )

    upper_col.metric(
        "95% CI Upper Bound",
        f"{ci_upper:.4f}",
    )

    st.markdown("---")

    st.markdown("#### Understanding the Results")

    significance = (
        "Statistically significant at the 5% level"
        if p_value < 0.05
        else "Not statistically significant at the 5% level"
    )

    st.markdown(
        f"""
        <div class="insight-card">
            <div class="insight-title">
                1. Estimated Price Effect
            </div>
            <div class="insight-text">
                The estimated DML price effect is {effect:.4f}.
                This represents the estimated treatment effect of Price
                on Demand under the assumptions of the analysis.
            </div>
        </div>

        <div class="insight-card">
            <div class="insight-title">
                2. Confidence Interval
            </div>
            <div class="insight-text">
                The 95% confidence interval ranges from {ci_lower:.4f}
                to {ci_upper:.4f}. It represents the uncertainty
                around the estimated effect.
            </div>
        </div>

        <div class="insight-card">
            <div class="insight-title">
                3. Statistical Significance
            </div>
            <div class="insight-text">
                {significance}. P-value:
                {p_value_text}.
            </div>
        </div>

        <div class="insight-card">
            <div class="insight-title">
                4. Data Coverage
            </div>
            <div class="insight-text">
                The analysis is based on {observations:,}
                observations.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.caption(
        "Statistical significance does not by itself prove causality. "
        "The causal interpretation depends on the DML assumptions, "
        "including appropriate control of confounders."
    )

    st.markdown(
        '<div class="footer">'
        'EconoCausal | Double Machine Learning'
        '</div>',
        unsafe_allow_html=True,
    )

