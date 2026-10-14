# EconoCausal: Dynamic Pricing via Double Machine Learning

## Overview

EconoCausal is a machine learning project that explores the relationship between product pricing and customer demand using Double Machine Learning (DML).

The project uses historical sales data and observed factors such as competitor pricing, promotions, inventory, seasonality, product category, and region to estimate the price effect on demand.

## Objectives

- Analyze historical sales and pricing data.
- Prepare and validate data for causal analysis.
- Build machine learning models for price and demand.
- Estimate the price–demand relationship using residual-based DML.
- Evaluate the stability of the estimate and export results.

## Technologies

- Python
- Pandas and NumPy
- Scikit-learn
- Matplotlib
- Git and GitHub

## Project Structure

```text
Infotect-EconoCasual/
├── data/
│   ├── raw/
│   └── processed/
├── reports/
│   ├── figures/
│   └── results/
├── src/
│   ├── preprocessing.py
│   ├── feature_engineering.py
│   ├── prepare_dml_data.py
│   ├── model_config.py
│   ├── treatment_model.py
│   ├── demand_model.py
│   ├── prepare_dml_residuals.py
│   ├── dml_estimator.py
│   ├── model_diagnostics.py
│   ├── export_results.py
│   └── effect_stability.py
├── requirements.txt
└── README.md
```

## Setup

1. Clone the repository.
2. Create and activate a Python virtual environment.
3. Install dependencies:

```bash
python -m pip install -r requirements.txt
```

4. Place the original dataset at `data/raw/sales_data.csv`.
5. Run the preprocessing and feature-engineering scripts in the appropriate order.
6. Run the DML input preparation and estimation scripts.

## Main Commands

```bash
python -m src.preprocessing
python -m src.feature_engineering
python -m src.prepare_dml_data
python -m src.validate_dml_inputs
python -m src.dml_estimator
python -m src.model_diagnostics
python -m src.export_results
python -m src.effect_stability
```

Run each command only after confirming that its input files exist and its prerequisites have been completed.

## Outputs

The project generates exploratory data visualizations and CSV files containing DML estimates, diagnostics, and stability-check results under `reports/`.

## Important Note

The estimated price effect is based on observational data. Its causal interpretation depends on assumptions, including adequate adjustment for confounding and correct model specification. The estimate should not be treated as proof of causality without further validation.

## Project Status

Initial data preparation, feature engineering, and DML model development are in progress.