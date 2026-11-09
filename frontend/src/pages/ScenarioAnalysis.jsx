
import { useEffect, useState } from "react";
import { predictDemand } from "../services/api";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";
import {
  Activity,
  TrendingDown,
  TrendingUp,
  BarChart3,
  RotateCcw,
  Play,
} from "lucide-react";

const STORAGE_KEY = "econocausal_last_prediction_inputs";

const styles = {
  page: {
    padding: "28px",
    color: "#1e293b",
    background: "#f8fafc",
    minHeight: "100%",
  },
  heading: {
    fontSize: "25px",
    fontWeight: 700,
    marginBottom: "8px",
  },
  subtitle: {
    color: "#64748b",
    marginBottom: "25px",
    fontSize: "14px",
  },
  card: {
    background: "#fff",
    border: "1px solid #e2e8f0",
    borderRadius: "14px",
    padding: "24px",
    marginBottom: "22px",
  },
  sectionTitle: {
    fontSize: "17px",
    fontWeight: 650,
    marginBottom: "8px",
  },
  description: {
    color: "#64748b",
    fontSize: "13px",
    marginBottom: "22px",
  },
  sliderGroup: {
    marginBottom: "25px",
  },
  sliderHeader: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    marginBottom: "12px",
    gap: "12px",
  },
  slider: {
    width: "100%",
    accentColor: "#635bdb",
    cursor: "pointer",
  },
  price: {
    fontSize: "17px",
    fontWeight: 700,
    color: "#5145cd",
  },
  rangeLabels: {
    display: "flex",
    justifyContent: "space-between",
    color: "#94a3b8",
    fontSize: "11px",
    marginTop: "5px",
  },
  button: {
    display: "inline-flex",
    alignItems: "center",
    gap: "8px",
    background: "#5145cd",
    color: "#fff",
    border: "none",
    borderRadius: "8px",
    padding: "12px 20px",
    fontSize: "14px",
    fontWeight: 600,
    cursor: "pointer",
  },
  secondaryButton: {
    display: "inline-flex",
    alignItems: "center",
    gap: "8px",
    background: "#fff",
    color: "#475569",
    border: "1px solid #cbd5e1",
    borderRadius: "8px",
    padding: "11px 17px",
    fontSize: "14px",
    cursor: "pointer",
  },
  summaryGrid: {
    display: "grid",
    gridTemplateColumns: "repeat(auto-fit, minmax(180px, 1fr))",
    gap: "16px",
    marginBottom: "22px",
  },
  summaryCard: {
    background: "#fff",
    border: "1px solid #e2e8f0",
    borderRadius: "12px",
    padding: "20px",
  },
  summaryLabel: {
    color: "#64748b",
    fontSize: "13px",
    marginTop: "10px",
  },
  summaryValue: {
    fontSize: "25px",
    fontWeight: 700,
    marginTop: "8px",
    color: "#1e293b",
  },
  error: {
    background: "#fff1f2",
    border: "1px solid #fecdd3",
    color: "#be123c",
    padding: "13px",
    borderRadius: "8px",
    marginBottom: "18px",
    fontSize: "13px",
  },
  notice: {
    background: "#eff6ff",
    border: "1px solid #bfdbfe",
    color: "#1d4ed8",
    padding: "14px",
    borderRadius: "8px",
    fontSize: "13px",
    lineHeight: 1.6,
  },
};

function ScenarioAnalysis() {
  const [minPrice, setMinPrice] = useState(50);
  const [maxPrice, setMaxPrice] = useState(200);
  const [previousInputs, setPreviousInputs] = useState(null);
  const [chartData, setChartData] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [hasRun, setHasRun] = useState(false);

  useEffect(() => {
    try {
      const savedInputs = localStorage.getItem(STORAGE_KEY);

      if (savedInputs) {
        setPreviousInputs(JSON.parse(savedInputs));
      }
    } catch {
      setPreviousInputs(null);
    }
  }, []);

  const runAnalysis = async () => {
    setError("");
    setChartData([]);
    setHasRun(false);

    if (!previousInputs) {
      setError(
        "Please complete Demand Prediction first. Scenario Analysis needs your latest product and market inputs."
      );
      return;
    }

    if (minPrice >= maxPrice) {
      setError("Maximum competitor pricing must be greater than minimum pricing.");
      return;
    }

    setLoading(true);

    try {
      const pricePoints = Array.from({ length: 11 }, (_, index) =>
        Number((minPrice + ((maxPrice - minPrice) * index) / 10).toFixed(2))
      );

      const predictions = await Promise.all(
        pricePoints.map(async (price) => {
          const response = await predictDemand({
            ...previousInputs,
            competitor_pricing: price,
          });

          const demand = Number(response.predicted_demand);

          if (!Number.isFinite(demand)) {
            throw new Error("The prediction service returned an invalid demand value.");
          }

          return {
            price,
            demand: Number(demand.toFixed(2)),
          };
        })
      );

      setChartData(predictions);
      setHasRun(true);
    } catch (err) {
      setError(
        err.message || "Unable to complete scenario analysis. Please try again."
      );
    } finally {
      setLoading(false);
    }
  };

  const resetAnalysis = () => {
    setMinPrice(50);
    setMaxPrice(200);
    setChartData([]);
    setError("");
    setHasRun(false);
  };

  const lowestDemand = chartData.length
    ? Math.min(...chartData.map((item) => item.demand))
    : 0;

  const highestDemand = chartData.length
    ? Math.max(...chartData.map((item) => item.demand))
    : 0;

  const averageDemand = chartData.length
    ? chartData.reduce((total, item) => total + item.demand, 0) /
      chartData.length
    : 0;

  return (
    <div style={styles.page}>
      <h1 style={styles.heading}>Scenario Analysis</h1>
      <p style={styles.subtitle}>
        Explore how competitor pricing changes predicted demand.
      </p>

      <div style={styles.card}>
        <h2 style={styles.sectionTitle}>Competitor Pricing Range</h2>
        <p style={styles.description}>
          Select a minimum and maximum competitor price. The model will
          evaluate 11 price points using your latest Demand Prediction inputs.
        </p>

        <div style={styles.sliderGroup}>
          <div style={styles.sliderHeader}>
            <label>Minimum Competitor Pricing</label>
            <span style={styles.price}>₹{minPrice.toFixed(2)}</span>
          </div>

          <input
            type="range"
            min="0"
            max="300"
            step="5"
            value={minPrice}
            onChange={(e) => setMinPrice(Number(e.target.value))}
            style={styles.slider}
          />

          <div style={styles.rangeLabels}>
            <span>₹0</span>
            <span>₹300</span>
          </div>
        </div>

        <div style={styles.sliderGroup}>
          <div style={styles.sliderHeader}>
            <label>Maximum Competitor Pricing</label>
            <span style={styles.price}>₹{maxPrice.toFixed(2)}</span>
          </div>

          <input
            type="range"
            min="0"
            max="300"
            step="5"
            value={maxPrice}
            onChange={(e) => setMaxPrice(Number(e.target.value))}
            style={styles.slider}
          />

          <div style={styles.rangeLabels}>
            <span>₹0</span>
            <span>₹300</span>
          </div>
        </div>

        <div style={{ display: "flex", gap: "12px", flexWrap: "wrap" }}>
          <button
            onClick={runAnalysis}
            disabled={loading}
            style={{
              ...styles.button,
              opacity: loading ? 0.65 : 1,
              cursor: loading ? "not-allowed" : "pointer",
            }}
          >
            <Play size={16} />
            {loading ? "Analyzing..." : "Run Scenario Analysis"}
          </button>

          <button onClick={resetAnalysis} style={styles.secondaryButton}>
            <RotateCcw size={16} />
            Reset
          </button>
        </div>
      </div>

      {error && <div style={styles.error}>{error}</div>}

      {!previousInputs && (
        <div style={styles.notice}>
          Complete a prediction on the Demand Prediction page first. Your
          latest product and market conditions will be reused here.
        </div>
      )}

      {hasRun && (
        <>
          <div style={styles.summaryGrid}>
            <div style={styles.summaryCard}>
              <TrendingDown size={21} color="#e87979" />
              <div style={styles.summaryLabel}>Lowest Predicted Demand</div>
              <div style={styles.summaryValue}>
                {lowestDemand.toFixed(2)}
              </div>
              <div style={styles.summaryLabel}>Units</div>
            </div>

            <div style={styles.summaryCard}>
              <Activity size={21} color="#635bdb" />
              <div style={styles.summaryLabel}>Average Predicted Demand</div>
              <div style={styles.summaryValue}>
                {averageDemand.toFixed(2)}
              </div>
              <div style={styles.summaryLabel}>Units</div>
            </div>

            <div style={styles.summaryCard}>
              <TrendingUp size={21} color="#16a085" />
              <div style={styles.summaryLabel}>Highest Predicted Demand</div>
              <div style={styles.summaryValue}>
                {highestDemand.toFixed(2)}
              </div>
              <div style={styles.summaryLabel}>Units</div>
            </div>
          </div>

          <div style={styles.card}>
            <h2 style={styles.sectionTitle}>
              Competitor Pricing vs Predicted Demand
            </h2>
            <p style={styles.description}>
              Model predictions across your selected pricing range.
            </p>

            <div style={{ width: "100%", height: 350 }}>
              <ResponsiveContainer width="100%" height="100%">
                <LineChart
                  data={chartData}
                  margin={{ top: 10, right: 20, left: 5, bottom: 15 }}
                >
                  <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
                  <XAxis
                    dataKey="price"
                    type="number"
                    domain={[minPrice, maxPrice]}
                    tickFormatter={(value) => `₹${value}`}
                    label={{
                      value: "Competitor Pricing (₹)",
                      position: "insideBottom",
                      offset: -8,
                    }}
                  />
                  <YAxis
                    label={{
                      value: "Predicted Demand (units)",
                      angle: -90,
                      position: "insideLeft",
                    }}
                  />
                  <Tooltip
                    formatter={(value) => [
                      `${Number(value).toFixed(2)} units`,
                      "Predicted Demand",
                    ]}
                    labelFormatter={(value) => `Competitor Price: ₹${value}`}
                  />
                  <Line
                    type="monotone"
                    dataKey="demand"
                    name="Predicted Demand"
                    stroke="#635bdb"
                    strokeWidth={3}
                    dot={{ r: 5, fill: "#635bdb" }}
                    activeDot={{ r: 7 }}
                  />
                </LineChart>
              </ResponsiveContainer>
            </div>

            <p style={{ color: "#64748b", fontSize: "12px", lineHeight: 1.6 }}>
              Each point represents a separate prediction from your trained
              model. Only competitor pricing changes; the product category,
              region, seasonality, inventory and promotion values are kept
              constant using your latest Demand Prediction inputs. This is a
              model-based scenario comparison, not a causal estimate or a
              guarantee of actual sales.
            </p>
          </div>
        </>
      )}
    </div>
  );
}

export default ScenarioAnalysis;
