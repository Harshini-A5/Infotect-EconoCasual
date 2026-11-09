
import { useState } from "react";
import { predictDemand } from "../services/api";
import {
  Activity,
  ArrowRight,
  BarChart3,
  Boxes,
  CheckCircle2,
  LoaderCircle,
  RotateCcw,
  TrendingUp,
} from "lucide-react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Cell,
} from "recharts";

export default function DemandPrediction() {
  const initialForm = {
    competitor_pricing: 100,
    promotion: 1,
    inventory_level: 100,
    seasonality: "Autumn",
    category: "Electronics",
    region: "North",
  };

  const [form, setForm] = useState(initialForm);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  function updateField(event) {
    const { name, value } = event.target;

    setForm((previous) => ({
      ...previous,
      [name]: [
        "competitor_pricing",
        "inventory_level",
        "promotion",
      ].includes(name)
        ? Number(value)
        : value,
    }));
  }

  
async function handleSubmit(event) {
  event.preventDefault();
  setLoading(true);
  setError("");
  setResult(null);

  // Preserve the exact inputs used for this prediction.
  const submittedInputs = { ...form };

  try {
    const response = await predictDemand(submittedInputs);

    // Save the successful prediction inputs for Scenario Analysis.
    try {
      localStorage.setItem(
        "econocausal_last_prediction_inputs",
        JSON.stringify(submittedInputs)
      );
    } catch (storageError) {
      console.warn("Unable to save prediction inputs:", storageError);
    }

    setResult(response);
  } catch (err) {
    setError(err.message || "Unable to generate prediction.");
  } finally {
    setLoading(false);
  }
}

  function resetForm() {
    setForm(initialForm);
    setResult(null);
    setError("");
  }

  const predictedDemand = result
    ? Number(result.predicted_demand)
    : 0;

  const chartData = result
    ? [
        {
          name: "Predicted Demand",
          value: predictedDemand,
        },
        {
          name: "Available Inventory",
          value: Number(form.inventory_level),
        },
      ]
    : [];

  const inventoryDifference = result
    ? Number(form.inventory_level) - predictedDemand
    : 0;

  return (
    <div className="dp-page">
      <style>{`
        .dp-page {
          display: flex;
          flex-direction: column;
          gap: 22px;
          color: #20243a;
          width: 100%;
        }

        .dp-heading {
          display: flex;
          justify-content: space-between;
          align-items: center;
          gap: 16px;
        }

        .dp-eyebrow {
          color: #6257d9;
          font-size: 11px;
          font-weight: 800;
          letter-spacing: 1.5px;
        }

        .dp-heading h1 {
          font-size: 27px;
          margin: 7px 0 5px;
          font-weight: 750;
          letter-spacing: -0.7px;
        }

        .dp-heading p {
          color: #85899b;
          font-size: 13px;
          margin: 0;
        }

        .dp-heading-icon {
          width: 48px;
          height: 48px;
          display: grid;
          place-items: center;
          border-radius: 14px;
          background: #eeecff;
          color: #6558d9;
          flex-shrink: 0;
        }

        .dp-status {
          display: inline-flex;
          align-items: center;
          gap: 7px;
          margin-top: 12px;
          font-size: 11px;
          color: #16845b;
          font-weight: 700;
        }

        .dp-status-dot {
          width: 7px;
          height: 7px;
          border-radius: 50%;
          background: #20b77b;
        }

        .dp-main-grid {
          display: grid;
          grid-template-columns: minmax(0, 1.35fr) minmax(280px, 0.85fr);
          gap: 20px;
          align-items: start;
        }

        .dp-card {
          background: #ffffff;
          border: 1px solid #e9eaf1;
          border-radius: 16px;
          padding: 23px;
          box-shadow: 0 3px 12px rgba(30, 35, 70, 0.035);
          min-width: 0;
        }

        .dp-card-heading {
          display: flex;
          justify-content: space-between;
          align-items: center;
          gap: 12px;
          margin-bottom: 20px;
        }

        .dp-card-heading h2 {
          font-size: 16px;
          font-weight: 750;
          margin: 0;
          color: #252940;
        }

        .dp-card-heading p {
          font-size: 12px;
          color: #9094a5;
          margin: 5px 0 0;
        }

        .dp-card-icon {
          color: #7468df;
          background: #f1efff;
          border-radius: 10px;
          padding: 9px;
          box-sizing: content-box;
        }

        .dp-section-title {
          display: flex;
          align-items: center;
          gap: 9px;
          margin: 23px 0 15px;
          padding-bottom: 11px;
          border-bottom: 1px solid #eff0f5;
          color: #5d55c9;
          font-size: 12px;
          font-weight: 800;
          letter-spacing: 0.5px;
        }

        .dp-section-title:first-of-type {
          margin-top: 0;
        }

        .dp-form-grid {
          display: grid;
          grid-template-columns: repeat(2, minmax(0, 1fr));
          gap: 17px 16px;
        }

        .dp-field {
          display: flex;
          flex-direction: column;
          gap: 8px;
          min-width: 0;
          color: #505469;
          font-size: 12px;
          font-weight: 650;
        }

        .dp-field input,
        .dp-field select {
          width: 100%;
          height: 43px;
          box-sizing: border-box;
          border: 1px solid #e4e6ee;
          border-radius: 9px;
          padding: 0 12px;
          outline: none;
          background: #fbfbfd;
          color: #30344b;
          font-size: 13px;
          font-family: inherit;
          transition: border-color 0.2s, box-shadow 0.2s;
        }

        .dp-field input:focus,
        .dp-field select:focus {
          border-color: #8175e8;
          box-shadow: 0 0 0 3px rgba(113, 99, 218, 0.10);
          background: #fff;
        }

        .dp-input-prefix {
          position: relative;
        }

        .dp-input-prefix span {
          position: absolute;
          left: 13px;
          top: 50%;
          transform: translateY(-50%);
          color: #888ba0;
          font-size: 13px;
          font-weight: 700;
        }

        .dp-input-prefix input {
          padding-left: 30px;
        }

        .dp-form-actions {
          display: flex;
          justify-content: flex-end;
          gap: 10px;
          margin-top: 25px;
          padding-top: 19px;
          border-top: 1px solid #eff0f5;
        }

        .dp-button {
          min-height: 42px;
          border-radius: 9px;
          padding: 0 16px;
          display: inline-flex;
          align-items: center;
          justify-content: center;
          gap: 8px;
          font-family: inherit;
          font-size: 12px;
          font-weight: 700;
          cursor: pointer;
          transition: 0.2s;
        }

        .dp-reset {
          border: 1px solid #e4e5ed;
          background: white;
          color: #656a7e;
        }

        .dp-reset:hover {
          background: #f5f5fa;
        }

        .dp-submit {
          border: none;
          color: white;
          background: #6257d9;
          box-shadow: 0 4px 10px rgba(98, 87, 217, 0.18);
        }

        .dp-submit:hover:not(:disabled) {
          background: #5045c4;
          transform: translateY(-1px);
        }

        .dp-submit:disabled {
          opacity: 0.65;
          cursor: not-allowed;
        }

        .dp-result-card {
          min-height: 335px;
        }

        .dp-result-empty {
          min-height: 240px;
          display: flex;
          flex-direction: column;
          align-items: center;
          justify-content: center;
          text-align: center;
          padding: 20px;
        }

        .dp-empty-icon {
          width: 65px;
          height: 65px;
          border-radius: 18px;
          display: grid;
          place-items: center;
          color: #7165dc;
          background: #f0efff;
          margin-bottom: 17px;
        }

        .dp-result-empty h3 {
          margin: 0 0 8px;
          font-size: 15px;
          color: #34384d;
        }

        .dp-result-empty p {
          color: #9296a6;
          font-size: 12px;
          line-height: 1.7;
          max-width: 230px;
          margin: 0;
        }

        .dp-result-success {
          padding: 8px 2px 0;
        }

        .dp-result-label {
          font-size: 10px;
          letter-spacing: 1.2px;
          color: #888ca0;
          font-weight: 800;
        }

        .dp-result-value {
          font-size: 39px;
          font-weight: 800;
          letter-spacing: -1.5px;
          color: #282c43;
          margin: 9px 0 1px;
          line-height: 1.2;
        }

        .dp-result-unit {
          font-size: 12px;
          color: #9296a6;
        }

        .dp-success-tag {
          display: inline-flex;
          align-items: center;
          gap: 6px;
          background: #eaf8f1;
          color: #16845b;
          border-radius: 20px;
          padding: 7px 10px;
          margin-top: 16px;
          font-size: 10px;
          font-weight: 750;
        }

        .dp-result-details {
          border-top: 1px solid #eff0f5;
          margin-top: 20px;
          padding-top: 13px;
          display: flex;
          flex-direction: column;
          gap: 12px;
        }

        .dp-detail-row {
          display: flex;
          justify-content: space-between;
          gap: 10px;
          font-size: 12px;
        }

        .dp-detail-row span {
          color: #85899b;
        }

        .dp-detail-row strong {
          color: #3c4055;
          font-weight: 700;
          text-align: right;
        }

        .dp-error {
          padding: 18px;
          background: #fff1f1;
          border: 1px solid #ffdada;
          border-radius: 10px;
          color: #b93838;
          font-size: 12px;
          line-height: 1.6;
        }

        .dp-error h3 {
          margin: 0 0 6px;
          font-size: 14px;
        }

        .dp-error p {
          margin: 0;
        }

        .dp-chart-card {
          margin-top: 0;
        }

        .dp-chart-heading {
          display: flex;
          justify-content: space-between;
          align-items: flex-start;
          gap: 12px;
          margin-bottom: 15px;
        }

        .dp-chart-heading h2 {
          margin: 0;
          font-size: 16px;
          color: #292d43;
        }

        .dp-chart-heading p {
          margin: 5px 0 0;
          font-size: 12px;
          color: #9296a6;
        }

        .dp-chart-legend {
          display: flex;
          flex-wrap: wrap;
          gap: 13px;
          margin-top: 12px;
          font-size: 11px;
          color: #777c90;
        }

        .dp-legend-item {
          display: flex;
          align-items: center;
          gap: 6px;
        }

        .dp-legend-dot {
          width: 8px;
          height: 8px;
          border-radius: 3px;
        }

        .dp-chart-note {
          margin-top: 12px;
          padding: 11px 13px;
          border-radius: 9px;
          background: #f7f7fc;
          color: #73788d;
          font-size: 11px;
          line-height: 1.6;
        }

        .dp-disclaimer {
          display: flex;
          align-items: flex-start;
          gap: 10px;
          padding: 14px 16px;
          background: #f0efff;
          border: 1px solid #e5e2ff;
          border-radius: 11px;
          color: #6159b8;
          font-size: 11px;
          line-height: 1.6;
        }

        .dp-disclaimer p {
          margin: 0;
        }

        .dp-spin {
          animation: dp-spin 1s linear infinite;
        }

        @keyframes dp-spin {
          to { transform: rotate(360deg); }
        }

        @media (max-width: 950px) {
          .dp-main-grid {
            grid-template-columns: 1fr;
          }

          .dp-result-card {
            min-height: 0;
          }
        }

        @media (max-width: 560px) {
          .dp-card {
            padding: 17px;
          }

          .dp-form-grid {
            grid-template-columns: 1fr;
          }

          .dp-heading h1 {
            font-size: 23px;
          }

          .dp-form-actions {
            flex-direction: column-reverse;
          }

          .dp-button {
            width: 100%;
          }
        }
      `}</style>

      {/* PAGE HEADER */}
      <div className="dp-heading">
        <div>
          <span className="dp-eyebrow">PREDICTIVE ANALYTICS</span>
          <h1>Demand Prediction</h1>
          <p>
            Analyze market conditions and estimate product demand
            using the trained machine learning model.
          </p>
          <div className="dp-status">
            <span className="dp-status-dot" />
            Prediction service
          </div>
        </div>

        <div className="dp-heading-icon">
          <Activity size={24} />
        </div>
      </div>

      {/* INPUT AND RESULT */}
      <div className="dp-main-grid">
        <section className="dp-card">
          <div className="dp-card-heading">
            <div>
              <h2>Prediction Parameters</h2>
              <p>Configure the product and market conditions.</p>
            </div>
            <BarChart3 size={22} className="dp-card-icon" />
          </div>

          <form onSubmit={handleSubmit}>
            {/* PRODUCT AND MARKET */}
            <div className="dp-section-title">
              <Boxes size={16} />
              01 — PRODUCT & MARKET DETAILS
            </div>

            <div className="dp-form-grid">
              <label className="dp-field">
                Product Category
                <select
                  name="category"
                  value={form.category}
                  onChange={updateField}
                >
                  <option>Electronics</option>
                  <option>Furniture</option>
                  <option>Groceries</option>
                  <option>Toys</option>
                </select>
              </label>

              <label className="dp-field">
                Region
                <select
                  name="region"
                  value={form.region}
                  onChange={updateField}
                >
                  <option>North</option>
                  <option>South</option>
                  <option>West</option>
                </select>
              </label>

              <label className="dp-field">
                Seasonality
                <select
                  name="seasonality"
                  value={form.seasonality}
                  onChange={updateField}
                >
                  <option>Autumn</option>
                  <option>Spring</option>
                  <option>Summer</option>
                  <option>Winter</option>
                </select>
              </label>

              <label className="dp-field">
                Inventory Level (units)
                <input
                  type="number"
                  name="inventory_level"
                  min="0"
                  value={form.inventory_level}
                  onChange={updateField}
                  required
                />
              </label>
            </div>

            {/* PRICING AND PROMOTION */}
            <div className="dp-section-title">
              <TrendingUp size={16} />
              02 — PRICING & PROMOTION
            </div>

            <div className="dp-form-grid">
              <label className="dp-field">
                Competitor Pricing
                <div className="dp-input-prefix">
                  <span>₹</span>
                  <input
                    type="number"
                    name="competitor_pricing"
                    min="0"
                    step="0.01"
                    value={form.competitor_pricing}
                    onChange={updateField}
                    required
                  />
                </div>
              </label>

              <label className="dp-field">
                Promotion Status
                <select
                  name="promotion"
                  value={form.promotion}
                  onChange={updateField}
                >
                  <option value={0}>No Promotion</option>
                  <option value={1}>Promotion Active</option>
                </select>
              </label>
            </div>

            <div className="dp-form-actions">
              <button
                type="button"
                className="dp-button dp-reset"
                onClick={resetForm}
              >
                <RotateCcw size={15} />
                Reset
              </button>

              <button
                type="submit"
                className="dp-button dp-submit"
                disabled={loading}
              >
                {loading ? (
                  <>
                    <LoaderCircle size={16} className="dp-spin" />
                    Predicting...
                  </>
                ) : (
                  <>
                    Generate Prediction
                    <ArrowRight size={16} />
                  </>
                )}
              </button>
            </div>
          </form>
        </section>

        {/* PREDICTION RESULT */}
        <section className="dp-card dp-result-card">
          <div className="dp-card-heading">
            <div>
              <h2>Prediction Result</h2>
              <p>Estimated demand from the trained model.</p>
            </div>
            <TrendingUp size={22} className="dp-card-icon" />
          </div>

          {loading ? (
            <div className="dp-result-empty">
              <LoaderCircle
                size={34}
                className="dp-spin"
                color="#7165dc"
              />
              <h3>Analyzing market parameters</h3>
              <p>
                Please wait while the model generates your prediction.
              </p>
            </div>
          ) : error ? (
            <div className="dp-error">
              <h3>Prediction unsuccessful</h3>
              <p>{error}</p>
            </div>
          ) : result ? (
            <div className="dp-result-success">
              <span className="dp-result-label">
                ESTIMATED PRODUCT DEMAND
              </span>

              <div className="dp-result-value">
                {predictedDemand.toFixed(2)}
              </div>

              <span className="dp-result-unit">
                {result.unit || "units"}
              </span>

              <div className="dp-success-tag">
                <CheckCircle2 size={14} />
                Prediction generated successfully
              </div>

              <div className="dp-result-details">
                <div className="dp-detail-row">
                  <span>Product category</span>
                  <strong>{form.category}</strong>
                </div>

                <div className="dp-detail-row">
                  <span>Region</span>
                  <strong>{form.region}</strong>
                </div>

                <div className="dp-detail-row">
                  <span>Season</span>
                  <strong>{form.seasonality}</strong>
                </div>

                <div className="dp-detail-row">
                  <span>Promotion</span>
                  <strong>
                    {form.promotion ? "Active" : "Inactive"}
                  </strong>
                </div>
              </div>

              {result.note && (
                <div className="dp-chart-note">
                  {result.note}
                </div>
              )}
            </div>
          ) : (
            <div className="dp-result-empty">
              <div className="dp-empty-icon">
                <BarChart3 size={30} />
              </div>
              <h3>Ready to predict</h3>
              <p>
                Enter your market parameters and generate a
                prediction to view the results and demand chart.
              </p>
            </div>
          )}
        </section>
      </div>

      {/* ACTUAL RESULT GRAPH */}
      {result && !loading && (
        <section className="dp-card dp-chart-card">
          <div className="dp-chart-heading">
            <div>
              <h2>Demand vs Available Inventory</h2>
              <p>
                Comparison based on the latest prediction and
                the inventory value entered above.
              </p>
            </div>
            <BarChart3 size={22} color="#7165dc" />
          </div>

          <div style={{ width: "100%", height: 280 }}>
            <ResponsiveContainer width="100%" height="100%">
              <BarChart
                data={chartData}
                margin={{
                  top: 15,
                  right: 15,
                  left: 0,
                  bottom: 5,
                }}
                barSize={65}
              >
                <CartesianGrid
                  strokeDasharray="3 3"
                  vertical={false}
                  stroke="#eceef4"
                />

                <XAxis
                  dataKey="name"
                  axisLine={false}
                  tickLine={false}
                  tick={{ fill: "#777c90", fontSize: 11 }}
                />

                <YAxis
                  axisLine={false}
                  tickLine={false}
                  tick={{ fill: "#9296a6", fontSize: 11 }}
                  allowDecimals={false}
                />

                <Tooltip
                  formatter={(value) => [
                    `${Number(value).toFixed(2)} units`,
                    "Quantity",
                  ]}
                  contentStyle={{
                    borderRadius: 10,
                    border: "1px solid #e8e9f0",
                    fontSize: 12,
                  }}
                />

                <Bar
                  dataKey="value"
                  name="Units"
                  radius={[7, 7, 0, 0]}
                >
                  {chartData.map((entry, index) => (
                    <Cell
                      key={entry.name}
                      fill={index === 0 ? "#7165dc" : "#36b58a"}
                    />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>

          <div className="dp-chart-legend">
            <div className="dp-legend-item">
              <span
                className="dp-legend-dot"
                style={{ background: "#7165dc" }}
              />
              Predicted demand
            </div>

            <div className="dp-legend-item">
              <span
                className="dp-legend-dot"
                style={{ background: "#36b58a" }}
              />
              Available inventory
            </div>
          </div>

          <div className="dp-chart-note">
            {inventoryDifference >= 0
              ? `The entered inventory is ${inventoryDifference.toFixed(2)} units higher than the predicted demand.`
              : `The predicted demand is ${Math.abs(inventoryDifference).toFixed(2)} units higher than the entered inventory.`}
            {" "}This is a comparison of the model estimate and
            entered inventory, not a separate stock optimization prediction.
          </div>
        </section>
      )}

      {/* DISCLAIMER */}
      <div className="dp-disclaimer">
        <Activity size={17} style={{ flexShrink: 0, marginTop: 1 }} />
        <p>
          Predictions are estimates generated by the trained
          machine learning model. Actual demand may vary depending
          on changing market conditions.
        </p>
      </div>
    </div>
  );
}
