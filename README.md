# EconoCausal – Dynamic Pricing via Double Machine Learning

An end-to-end data science project that combines Machine Learning and Double Machine Learning (DML) to study the relationship between product pricing and customer demand.

## Live Demo

- **React Dashboard:** https://econocausal-react.onrender.com
- **FastAPI Backend:** https://econocausal-api.onrender.com

## Project Overview

EconoCausal helps explore how product prices and market conditions relate to demand. It provides demand predictions, pricing scenario comparisons, and causal-effect insights through an interactive dashboard.

## Key Features

- Demand prediction using a trained Machine Learning model.
- Dynamic pricing scenario analysis across multiple price points.
- Double Machine Learning for estimating the effect of price on demand.
- Interactive dashboard built with React.
- REST API developed using FastAPI.
- Data exploration, preprocessing, and feature engineering.
- Visual presentation of model predictions and causal insights.

## Dataset

The project uses a retail dataset containing **76,000 records and 16 original columns**.

Important features include:
- Product and store information
- Price and competitor pricing
- Inventory level
- Discounts and promotions
- Weather and seasonality
- Units sold and demand

Additional features were created during preprocessing to support analysis and modelling.

## Technology Stack

| Area | Technologies |
|---|---|
| Programming | Python, JavaScript |
| Data Analysis | Pandas, NumPy |
| Machine Learning | Scikit-learn |
| Causal Inference | Double Machine Learning, Statsmodels |
| Backend | FastAPI |
| Frontend | React, Vite |
| Charts | Recharts |
| UI Icons | Lucide React |
| Deployment | Render |
| Version Control | Git, GitHub |

## Project Modules

1. **Data Preparation:** Cleaning, preprocessing, exploratory data analysis, and feature engineering.
2. **Demand Prediction:** Predicts demand using the trained ML model.
3. **Scenario Analysis:** Compares predicted demand across different pricing conditions.
4. **Causal Insights:** Presents DML-based estimates of the price effect on demand.
5. **API Integration:** Connects the React dashboard with the FastAPI prediction service.

## Project Structure

```text
EconoCausal/
├── backend/
│   └── main.py
├── frontend/
│   ├── public/
│   └── src/
├── data/
│   ├── raw/
│   └── processed/
├── models/
├── reports/
├── notebooks/
├── app.py
└── README.md
```

## Running Locally

### Backend

```bash
cd backend
pip install -r ../requirements.txt
uvicorn main:app --reload
```

### Frontend

Open another terminal:

```bash
cd frontend
npm install
npm run dev
```

Configure the frontend API URL using the environment variable `VITE_API_BASE_URL` when required.

## Project Status

**Deployed successfully.**

The React dashboard and FastAPI backend are hosted on Render.

## Author

**S. Harshini**

B.Tech – Artificial Intelligence and Machine Learning

GitHub: https://github.com/Harshini-A5

---

*This project was developed as a practical application of Machine Learning, causal inference, data analysis, and full-stack development.*