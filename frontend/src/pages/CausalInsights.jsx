
import { useEffect, useState } from "react";
import {
  Activity,
  BrainCircuit,
  Database,
  Info,
  RefreshCw,
  ShieldCheck,
  TrendingDown,
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
  ReferenceLine,
} from "recharts";

const REPORT_URL = `${import.meta.env.BASE_URL}data/robust_dml_inference.csv`;

const styles = {
  page: { display: "flex", flexDirection: "column", gap: "22px", color: "#20243a", width: "100%" },
  header: { display: "flex", justifyContent: "space-between", alignItems: "center", gap: "15px" },
  eyebrow: { color: "#6257d9", fontSize: "11px", fontWeight: 800, letterSpacing: "1.5px" },
  title: { fontSize: "27px", fontWeight: 750, margin: "7px 0 5px" },
  subtitle: { color: "#85899b", fontSize: "13px", margin: 0, lineHeight: 1.6 },
  headerIcon: { width: "48px", height: "48px", display: "grid", placeItems: "center", borderRadius: "14px", background: "#eeecff", color: "#6558d9", flexShrink: 0 },
  hero: { background: "linear-gradient(120deg, #29245f, #5145a8)", color: "#fff", padding: "25px", borderRadius: "16px", display: "flex", justifyContent: "space-between", alignItems: "center", gap: "20px", flexWrap: "wrap" },
  heroLabel: { color: "#d4d0ff", fontSize: "11px", fontWeight: 750, letterSpacing: "1.2px" },
  heroTitle: { fontSize: "21px", fontWeight: 750, margin: "10px 0 7px" },
  heroText: { color: "#e1dfff", fontSize: "12px", lineHeight: 1.7, maxWidth: "620px", margin: 0 },
  heroIcon: { opacity: 0.85 },
  grid: { display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(180px, 1fr))", gap: "16px" },
  card: { background: "#fff", border: "1px solid #e9eaf1", borderRadius: "14px", padding: "21px", boxShadow: "0 3px 12px rgba(30, 35, 70, 0.035)", minWidth: 0 },
  metricLabel: { fontSize: "12px", color: "#85899b", marginTop: "12px" },
  metricValue: { fontSize: "25px", fontWeight: 750, color: "#292d43", marginTop: "7px", overflowWrap: "anywhere" },
  metricDescription: { fontSize: "11px", color: "#a0a3b0", marginTop: "5px" },
  sectionHeading: { fontSize: "16px", fontWeight: 750, color: "#292d43", margin: "0 0 7px" },
  sectionDescription: { fontSize: "12px", color: "#9296a6", margin: "0 0 20px", lineHeight: 1.6 },
  infoBox: { background: "#f5f4ff", border: "1px solid #e5e2ff", borderRadius: "10px", padding: "14px", display: "flex", gap: "10px", color: "#6259b8", fontSize: "12px", lineHeight: 1.7 },
  errorBox: { background: "#fff7ed", border: "1px solid #fed7aa", borderRadius: "10px", padding: "15px", color: "#9a3412", fontSize: "12px", lineHeight: 1.7 },
  methodGrid: { display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(200px, 1fr))", gap: "14px" },
  methodItem: { background: "#fafaff", border: "1px solid #eeeeF7", borderRadius: "10px", padding: "17px" },
  methodTitle: { fontSize: "13px", fontWeight: 750, color: "#393d55", margin: "10px 0 6px" },
  methodText: { color: "#85899b", fontSize: "11px", lineHeight: 1.7, margin: 0 },
  status: { display: "inline-flex", alignItems: "center", gap: "7px", padding: "7px 11px", borderRadius: "20px", background: "#eaf8f1", color: "#16845b", fontSize: "11px", fontWeight: 750 },
  button: { display: "inline-flex", alignItems: "center", gap: "8px", background: "#6257d9", color: "#fff", border: "none", borderRadius: "8px", padding: "10px 15px", fontSize: "12px", fontWeight: 700, cursor: "pointer" },
};

function parseCSV(text) {
  const rows = [];
  let row = [];
  let value = "";
  let quoted = false;

  for (let i = 0; i < text.length; i++) {
    const char = text[i];

    if (char === '"') {
      if (quoted && text[i + 1] === '"') {
        value += '"';
        i++;
      } else {
        quoted = !quoted;
      }
    } else if (char === "," && !quoted) {
      row.push(value.trim());
      value = "";
    } else if ((char === "\n" || char === "\r") && !quoted) {
      if (char === "\r" && text[i + 1] === "\n") i++;
      row.push(value.trim());
      if (row.some((cell) => cell !== "")) rows.push(row);
      row = [];
      value = "";
    } else {
      value += char;
    }
  }

  row.push(value.trim());
  if (row.some((cell) => cell !== "")) rows.push(row);

  if (rows.length < 2) {
    throw new Error("The DML report is empty or has no data rows.");
  }

  const headers = rows[0].map((header) =>
    header.replace(/^\uFEFF/, "").toLowerCase().replace(/[^a-z0-9]/g, "")
  );

  return rows.slice(1).map((cells) => {
    const record = {};
    headers.forEach((header, index) => {
      record[header] = cells[index] ?? "";
    });
    return record;
  });
}

function getNumber(record, aliases) {
  for (const alias of aliases) {
    const value = record[alias];
    if (value !== undefined && value !== "") {
      const number = Number(value);
      if (Number.isFinite(number)) return number;
    }
  }
  return null;
}

function formatNumber(value, digits = 4) {
  if (value === null || value === undefined) return "Not available";
  return Number(value).toLocaleString("en-IN", {
    maximumFractionDigits: digits,
  });
}

function CausalInsights() {
  const [report, setReport] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  async function loadReport() {
    setLoading(true);
    setError("");

    try {
      const response = await fetch(REPORT_URL);

      if (!response.ok) {
        throw new Error(
          "DML report not found. Add robust_dml_inference.csv to frontend/public/data/."
        );
      }

      const csvText = await response.text();
      const records = parseCSV(csvText);
      const record = records[0];

      const estimate = getNumber(record, [
        "estimatedpriceeffect",
        "estimate",
        "coefficient",
        "coef",
        "effect",
        "ate",
        "theta",
        "treatmenteffect",
      ]);

      const standardError = getNumber(record, [
        "robuststandarderrorhc1",
        "robustse",
        "stderr",
        "standarderror",
        "se",
        "robuststderr",
      ]);

      const confidenceLower = getNumber(record, [
        "ci95lower",
        "cilower",
        "lowerci",
        "lower95",
        "ci025",
        "lowerbound",
      ]);

      const confidenceUpper = getNumber(record, [
        "ci95upper",
        "ciupper",
        "upperci",
        "upper95",
        "ci975",
        "upperbound",
      ]);

      const pValue = getNumber(record, [
        "pvalue",
        "pval",
        "p",
        "pvalueestimate",
      ]);

      const observations = getNumber(record, [
        "observations",
        "nobs",
        "nobservations",
        "samplecount",
      ]);

      if (estimate === null) {
        throw new Error("The report was loaded, but the estimated price effect is not a valid number.");
      }

      setReport({
        estimate,
        standardError,
        confidenceLower,
        confidenceUpper,
        pValue,
        observations,
      });
    } catch (err) {
      setError(err.message || "Unable to load the DML inference report.");
      setReport(null);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadReport();
  }, []);

  const chartData =
    report &&
    report.confidenceLower !== null &&
    report.confidenceUpper !== null
      ? [{ name: "Estimated Price Effect", effect: report.estimate }]
      : [];

  const statisticallySignificant =
    report?.pValue !== null &&
    report?.pValue !== undefined &&
    report.pValue < 0.05;

  return (
    <div style={styles.page}>
      <div style={styles.header}>
        <div>
          <span style={styles.eyebrow}>CAUSAL MACHINE LEARNING</span>
          <h1 style={styles.title}>Causal Insights</h1>
          <p style={styles.subtitle}>
            Understand the estimated relationship between product pricing and demand using Double Machine Learning.
          </p>
        </div>
        <div style={styles.headerIcon}><BrainCircuit size={25} /></div>
      </div>

      <section style={styles.hero}>
        <div>
          <span style={styles.heroLabel}>ECONOCAUSAL ANALYTICS</span>
          <h2 style={styles.heroTitle}>Beyond prediction — understanding price effects</h2>
          <p style={styles.heroText}>
            This analysis uses Double Machine Learning to estimate the effect of product price on demand while accounting for observed market conditions and potential confounding factors.
          </p>
        </div>
        <BrainCircuit size={65} style={styles.heroIcon} />
      </section>

      {loading && (
        <section style={styles.card}>
          <p style={styles.subtitle}>Loading DML inference results...</p>
        </section>
      )}

      {!loading && error && (
        <section style={styles.errorBox}>
          <strong>Inference report unavailable</strong>
          <p>{error}</p>
          <p>Expected file: <code>frontend/public/data/robust_dml_inference.csv</code></p>
          <button style={styles.button} onClick={loadReport}>
            <RefreshCw size={14} /> Retry
          </button>
        </section>
      )}

      {!loading && report && (
        <>
          <div style={styles.grid}>
            <div style={styles.card}>
              <Activity size={21} color="#6257d9" />
              <div style={styles.metricLabel}>Estimated Price Effect</div>
              <div style={styles.metricValue}>{formatNumber(report.estimate)}</div>
              <div style={styles.metricDescription}>DML treatment-effect estimate</div>
            </div>

            <div style={styles.card}>
              <TrendingUp size={21} color="#16a085" />
              <div style={styles.metricLabel}>Robust Standard Error</div>
              <div style={styles.metricValue}>{formatNumber(report.standardError)}</div>
              <div style={styles.metricDescription}>Estimation uncertainty</div>
            </div>

            <div style={styles.card}>
              <ShieldCheck size={21} color="#6257d9" />
              <div style={styles.metricLabel}>P-value</div>
              <div style={styles.metricValue}>{formatNumber(report.pValue, 6)}</div>
              <div style={styles.metricDescription}>Statistical evidence</div>
            </div>

            <div style={styles.card}>
              <Database size={21} color="#16a085" />
              <div style={styles.metricLabel}>Observations</div>
              <div style={styles.metricValue}>{formatNumber(report.observations, 0)}</div>
              <div style={styles.metricDescription}>Records used in estimation</div>
            </div>
          </div>

          <section style={styles.card}>
            <h2 style={styles.sectionHeading}>Statistical Significance</h2>
            <p style={styles.sectionDescription}>Interpretation based on the 5% significance threshold.</p>

            {report.pValue === null ? (
              <div style={styles.infoBox}>
                <Info size={18} />
                The report does not contain an identifiable p-value. Statistical significance cannot be determined.
              </div>
            ) : (
              <div style={{
                ...styles.status,
                background: statisticallySignificant ? "#eaf8f1" : "#fff7ed",
                color: statisticallySignificant ? "#16845b" : "#b45309",
              }}>
                {statisticallySignificant
                  ? "Statistically significant at 5%"
                  : "Not statistically significant at 5%"}
              </div>
            )}

            <p style={{ ...styles.sectionDescription, marginTop: "14px" }}>
              {report.pValue === null
                ? "Add the p-value to the inference report to evaluate statistical significance."
                : statisticallySignificant
                  ? "The estimated effect is statistically distinguishable from zero at the 5% significance level. This does not by itself establish that the estimate is free from bias."
                  : "The available result does not provide sufficient statistical evidence to reject a zero effect at the 5% significance level."}
            </p>
          </section>

          <section style={styles.card}>
            <h2 style={styles.sectionHeading}>Price Effect & Confidence Interval</h2>
            <p style={styles.sectionDescription}>The estimated effect and its reported 95% confidence interval.</p>

            {chartData.length > 0 ? (
              <>
                <div style={{ width: "100%", height: 220 }}>
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart
                      data={chartData}
                      layout="vertical"
                      margin={{ top: 10, right: 25, left: 25, bottom: 10 }}
                    >
                      <CartesianGrid strokeDasharray="3 3" stroke="#eceef4" />
                      <XAxis type="number" tick={{ fontSize: 11, fill: "#85899b" }} />
                      <YAxis type="category" dataKey="name" width={155} tick={{ fontSize: 11, fill: "#555a70" }} />
                      <Tooltip formatter={(value) => formatNumber(value)} />
                      <ReferenceLine x={0} stroke="#dc7373" />
                      <Bar dataKey="effect" name="Estimated effect" fill="#7165dc" barSize={30} radius={[5, 5, 5, 5]} />
                    </BarChart>
                  </ResponsiveContainer>
                </div>

                <div style={styles.infoBox}>
                  <Info size={18} />
                  Estimate: {formatNumber(report.estimate)}. Reported confidence interval: {formatNumber(report.confidenceLower)} to {formatNumber(report.confidenceUpper)}.
                </div>
              </>
            ) : (
              <div style={styles.infoBox}>
                <Info size={18} />
                The report does not contain identifiable lower and upper confidence interval columns.
              </div>
            )}
          </section>
        </>
      )}

      <section style={styles.card}>
        <h2 style={styles.sectionHeading}>Methodology</h2>
        <p style={styles.sectionDescription}>How EconoCausal estimates the effect of price on product demand.</p>

        <div style={styles.methodGrid}>
          <div style={styles.methodItem}>
            <Database size={21} color="#6257d9" />
            <h3 style={styles.methodTitle}>Data Preparation</h3>
            <p style={styles.methodText}>Historical product and market data are prepared and processed for causal analysis.</p>
          </div>
          <div style={styles.methodItem}>
            <BrainCircuit size={21} color="#6257d9" />
            <h3 style={styles.methodTitle}>Double Machine Learning</h3>
            <p style={styles.methodText}>Machine learning models estimate nuisance relationships to help isolate the treatment effect.</p>
          </div>
          <div style={styles.methodItem}>
            <ShieldCheck size={21} color="#6257d9" />
            <h3 style={styles.methodTitle}>Robust Inference</h3>
            <p style={styles.methodText}>Robust standard errors and confidence intervals help quantify estimation uncertainty.</p>
          </div>
          <div style={styles.methodItem}>
            <TrendingDown size={21} color="#6257d9" />
            <h3 style={styles.methodTitle}>Price & Demand</h3>
            <p style={styles.methodText}>The analysis estimates how product pricing relates to demand after adjusting for observed confounders.</p>
          </div>
        </div>
      </section>

      <div style={styles.infoBox}>
        <Info size={18} style={{ flexShrink: 0 }} />
        <span>
          Causal estimates depend on the quality of the data, model assumptions and confounders included in the analysis. They should not be interpreted as guaranteed changes in actual sales.
        </span>
      </div>
    </div>
  );
}

export default CausalInsights;
