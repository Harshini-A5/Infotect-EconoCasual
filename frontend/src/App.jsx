
import { useState } from "react";
import {
  LayoutDashboard,
  TrendingUp,
  SlidersHorizontal,
  BrainCircuit,
  Bell,
  Search,
  ChevronDown,
  Package,
  Activity,
  Target,
  BarChart3,
  Menu,
} from "lucide-react";

import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

import DemandPrediction from "./pages/DemandPrediction";
import ScenarioAnalysis from "./pages/ScenarioAnalysis";
import CausalInsights from "./pages/CausalInsights";
import "./App.css";

const navigation = [
  { label: "Overview", icon: LayoutDashboard },
  { label: "Demand Prediction", icon: TrendingUp },
  { label: "Scenario Analysis", icon: SlidersHorizontal },
  { label: "Causal Insights", icon: BrainCircuit },
];

const categoryData = [
  { category: "Groceries", demand: 120.98 },
  { category: "Clothing", demand: 112.62 },
  { category: "Electronics", demand: 97.48 },
  { category: "Toys", demand: 92.61 },
  { category: "Furniture", demand: 73.58 },
];

function Overview() {
  return (
    <>
      <div className="page-heading">
        <div>
          <span className="eyebrow">ANALYTICS / OVERVIEW</span>
          <h1>Business Overview</h1>
          <p>Monitor demand patterns and understand pricing impact.</p>
        </div>
        <div className="date-chip">Retail demand dataset</div>
      </div>

      <div className="welcome-panel">
        <div>
          <span className="welcome-tag">ECONOCAUSAL INTELLIGENCE</span>
          <h2>
            Understand demand.
            <br />
            Make smarter pricing decisions.
          </h2>
          <p>
            Explore demand predictions and causal price-effect insights
            from your retail analytics model.
          </p>
        </div>

        <div className="welcome-graphic">
          <div className="graphic-circle circle-one" />
          <div className="graphic-circle circle-two" />
          <BarChart3 size={76} strokeWidth={1.2} />
        </div>
      </div>

      <div className="section-heading">
        <div>
          <h2>Key performance indicators</h2>
          <p>Summary of the current analysis</p>
        </div>
        <span className="live-indicator">
          <span /> Model analysis
        </span>
      </div>

      <div className="kpi-grid">
        <div className="kpi-card">
          <div className="kpi-top">
            <span className="kpi-icon purple">
              <Package size={19} />
            </span>
            <span className="kpi-caption">DATA VOLUME</span>
          </div>
          <h3>76,000</h3>
          <p>Retail observations</p>
          <div className="kpi-footer">Processed dataset</div>
        </div>

        <div className="kpi-card">
          <div className="kpi-top">
            <span className="kpi-icon blue">
              <Target size={19} />
            </span>
            <span className="kpi-caption">CAUSAL ESTIMATE</span>
          </div>
          <h3>0.9215</h3>
          <p>Estimated price effect</p>
          <div className="kpi-footer">Double Machine Learning</div>
        </div>

        <div className="kpi-card">
          <div className="kpi-top">
            <span className="kpi-icon green">
              <Activity size={19} />
            </span>
            <span className="kpi-caption">MODEL STATUS</span>
          </div>
          <h3 className="status-text">Ready</h3>
          <p>Prediction model</p>
          <div className="kpi-footer">Backend model available</div>
        </div>

        <div className="kpi-card">
          <div className="kpi-top">
            <span className="kpi-icon orange">
              <TrendingUp size={19} />
            </span>
            <span className="kpi-caption">CONFIDENCE INTERVAL</span>
          </div>
          <h3>0.8931–0.9499</h3>
          <p>95% confidence interval</p>
          <div className="kpi-footer">Robust DML inference</div>
        </div>
      </div>

      <div className="analytics-grid">
        <div className="panel category-panel">
          <div className="panel-heading">
            <div>
              <h2>Average demand by category</h2>
              <p>Mean demand across retail product categories</p>
            </div>
            <span className="panel-menu">•••</span>
          </div>

          <div className="chart-area">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart
                data={categoryData}
                margin={{ top: 15, right: 12, left: -18, bottom: 5 }}
              >
                <CartesianGrid
                  strokeDasharray="3 3"
                  vertical={false}
                  stroke="#edf0f5"
                />
                <XAxis
                  dataKey="category"
                  axisLine={false}
                  tickLine={false}
                  tick={{ fill: "#7c8496", fontSize: 11 }}
                />
                <YAxis
                  axisLine={false}
                  tickLine={false}
                  tick={{ fill: "#7c8496", fontSize: 11 }}
                />
                <Tooltip
                  cursor={{ fill: "#f4f2ff" }}
                  contentStyle={{
                    borderRadius: "10px",
                    border: "1px solid #e8eaf0",
                    boxShadow: "0 5px 20px rgba(20,30,60,0.08)",
                  }}
                />
                <Bar
                  dataKey="demand"
                  name="Average demand"
                  fill="#7065d9"
                  radius={[6, 6, 0, 0]}
                  maxBarSize={48}
                />
              </BarChart>
            </ResponsiveContainer>
          </div>

          <div className="chart-note">
            <span className="note-dot" />
            <span>
              Demand is highest in Groceries and lowest in Furniture.
            </span>
          </div>
        </div>

        <div className="panel insight-panel">
          <div className="panel-heading">
            <div>
              <h2>Analysis highlights</h2>
              <p>Insights from the dataset</p>
            </div>
            <BrainCircuit size={20} className="heading-icon" />
          </div>

          <div className="insight-item">
            <div className="insight-icon purple">
              <TrendingUp size={18} />
            </div>
            <div>
              <h3>Promotion impact</h3>
              <p>
                Average demand was 123.27 units with promotion,
                compared with 95.03 without promotion.
              </p>
            </div>
          </div>

          <div className="insight-item">
            <div className="insight-icon blue">
              <Target size={18} />
            </div>
            <div>
              <h3>Price-effect estimate</h3>
              <p>
                The estimated DML coefficient is 0.9215, with a
                robust confidence interval of 0.8931 to 0.9499.
              </p>
            </div>
          </div>

          <div className="insight-item">
            <div className="insight-icon green">
              <Package size={18} />
            </div>
            <div>
              <h3>Category performance</h3>
              <p>
                Groceries records the highest average demand
                among the five product categories.
              </p>
            </div>
          </div>

          <div className="method-note">
            <span>i</span>
            <p>
              Insights are based on the analyzed retail dataset.
              Predictions and causal estimates have different interpretations.
            </p>
          </div>
        </div>
      </div>

      <div className="footer-note">
        <span>EconoCausal Analytics</span>
        <span>Retail intelligence workspace · Version 1.0</span>
      </div>
    </>
  );
}

function App() {
  const [activePage, setActivePage] = useState("Overview");

  const pageContent = {
    Overview: <Overview />,
    "Demand Prediction": <DemandPrediction />,
    "Scenario Analysis": <ScenarioAnalysis />,
    "Causal Insights": <CausalInsights />,
  };

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-mark">
            <BarChart3 size={23} />
          </div>
          <div>
            <h2>EconoCausal</h2>
            <span>RETAIL INTELLIGENCE</span>
          </div>
        </div>

        <div className="workspace-label">WORKSPACE</div>

        <nav className="navigation">
          {navigation.map(({ label, icon: Icon }) => (
            <button
              key={label}
              className={`nav-item ${
                activePage === label ? "active" : ""
              }`}
              onClick={() => setActivePage(label)}
            >
              <Icon size={19} />
              <span>{label}</span>
              {activePage === label && (
                <span className="active-indicator" />
              )}
            </button>
          ))}
        </nav>

        <div className="sidebar-bottom">
          <div className="sidebar-status">
            <span className="status-dot" />
            <div>
              <strong>Analytics workspace</strong>
              <small>Frontend preview</small>
            </div>
          </div>

          <div className="user-profile">
            <div className="avatar">EC</div>
            <div>
              <strong>Project Workspace</strong>
              <small>Retail Analytics</small>
            </div>
            <ChevronDown size={16} />
          </div>
        </div>
      </aside>

      <main className="main-area">
        <header className="topbar">
          <div className="breadcrumb">
            <Menu size={18} className="mobile-menu-icon" />
            <span>Workspace</span>
            <span className="breadcrumb-divider">/</span>
            <strong>{activePage}</strong>
          </div>

          <div className="topbar-actions">
            <div className="system-status">
              <span /> System workspace
            </div>
            <button className="icon-button" aria-label="Search">
              <Search size={19} />
            </button>
            <button className="icon-button" aria-label="Notifications">
              <Bell size={19} />
            </button>
            <div className="top-avatar">EC</div>
          </div>
        </header>

        <div className="content-area">
          {pageContent[activePage]}
        </div>
      </main>
    </div>
  );
}

export default App;
