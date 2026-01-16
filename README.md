# Global Resilience Dashboard - Live Online Version 🌍

## 🚀 Live Dashboard

**Access Now:** [Deploy URL will appear here after GitHub Pages setup]

## 📋 Overview
Comprehensive resilience analysis dashboard with **real-time data** from 11+ APIs, historical data (2019-2025) and BSTS+DFM forecasts (2026-2030) for 253 World Bank recognized economies across 4 pillars of resilience.

**Version:** 3.0 (Online & Dynamic)
**Last Updated:** 16 January 2026  
**Technologies:** Leaflet.js, Chart.js, Live APIs, Real-time Data Feeds

---

## ✨ New Features (v3.0)

### 🕐 **8 Timezone Display with DST**
- UTC, New York, London, Paris, Tokyo, Sydney, Dubai, Singapore
- Updates every second
- Automatic DST detection and indicators

### 📡 **11 Live API Integrations**
1. **Reddit API** - Real-time discussions from worldnews, geopolitics, economics, climate
2. **GDELT 2.0** - Global news events with geo-tagging
3. **YouTube Data API** - Trending topics and discussions
4. **Alpha Vantage + Stooq** - Financial market data (stocks, gold, oil, forex)
5. **World Bank API** - Live GDP growth and economic indicators
6. **UNCTADstat API** - International trade statistics
7. **OECD API** - Employment, inflation, GDP statistics
8. **IMF Data API** - Global economic forecasts
9. **FRED API** - US Federal Reserve economic data
10. **Google Trends** - Search interest trends
11. **GDACS + NASA EONET** - Real-time disaster and natural event alerts

### 📊 **Interactive Data Layer Controls**
Toggle different data overlays on the map:
- 🚨 Disasters (GDACS)
- 📰 Global News (GDELT)
- 🌋 Natural Events (NASA)
- 💬 Reddit Discussions
- 📹 YouTube Topics
- 📈 Google Trends
- 💱 Financial Markets

### 🔄 **Auto-Refresh**
- Timezones: Every second
- API data: Every 5 minutes
- Automatic synchronization

---

## 🎯 Main Dashboard Files

### **Primary Dashboard (Use This!)**
- **`resilience_integrated_dashboard_v2.html`** ⭐ **MAIN FILE - LIVE & DYNAMIC**
  - All-in-one dashboard with 3 tabs + Live Data Panel
    - 🗺️ Interactive Map (2019-2030 timeline, 5 pillars, data layer controls)
    - 📊 Analytics & Graphs (8 different charts)
    - 📚 Comprehensive Methodology
  - 📡 Live Data Panel with 11 API integrations
  - 🕐 8 Timezone display with DST detection
  - 📊 Minimizable data feed panel
  - 🔄 Auto-refreshing every 5 minutes
  - Fully functional online with real-time data
  - **This is the latest, production-ready online dashboard**

### Alternative/Legacy Dashboards
- `resilience_integrated_dashboard.html` - Previous version (offline focus)
- `resilience_complete_timeline.html` - Map-only timeline version
- `resilience_forecast_dashboard.html` - Forecast animation focus
- `resilience_analytics_graphs.html` - Charts-only version
- `resilience_choropleth_map.html` - Basic choropleth map

---

## 📊 Data Files

### Core Data (Required)
1. **`resilience_timeline_2019_2030.json`** (Main dataset)
   - 324 countries with 12 years of data (2019-2030)
   - Structure: `{iso3, name, region, income, lat, lon, timeline: {year: {overall, financial, social, institutional, infrastructure}}}`
   - Size: ~1.5 MB

2. **`world.geojson`** (Country boundaries)
   - 258 country polygons for choropleth maps
   - Properties: `name`, `ISO3166-1-Alpha-3`, `ISO3166-1-Alpha-2`
   - Size: ~900 KB

3. **`resilience_data_complete.json`** (2025 baseline)
   - Merged World Bank + INFORM Risk data
   - 324 countries with current scores
   - Used as baseline for forecasts

### Forecast Data
4. **`resilience_forecasts_2025_2030.json`**
   - BSTS+DFM model predictions (2026-2030)
   - Includes confidence intervals (lower, upper bounds)
   - Zero Percentile Weighting applied

### Legacy/Intermediate Data
- `resilience_data_live.json` - Raw World Bank API data (254 countries)
- `resilience_data_cleaned.json` - INFORM Risk merged data (293 countries)
- `resilience_pillars.json` - Original corrupted file (kept for reference)

---

## 🐍 Python Scripts

### Data Collection
1. **`fetch_live_data.py`** - World Bank API data fetcher
   - Fetches 24 indicators across 4 pillars
   - No API key required
   - Output: `resilience_data_live.json`

2. **`integrate_inform_data.py`** - INFORM Risk integration
   - Reads: `INFORM_Risk_Mid_2025_v071.xlsx`
   - Merges with World Bank data
   - Output: `resilience_data_complete.json`

### Forecasting
3. **`forecast_resilience.py`** - BSTS+DFM forecasting model
   - Bayesian Structural Time Series (BSTS)
   - Dynamic Factor Model (DFM) with 2 latent factors
   - Zero Percentile Weighting algorithm
   - Output: `resilience_forecasts_2025_2030.json`

4. **`create_historical_forecast_data.py`** - Historical simulation
   - Generates 2019-2024 historical trajectories
   - Smooth random walk with controlled volatility
   - Output: `resilience_timeline_2019_2030.json`

### Dashboard Generation
5. **`create_integrated_dashboard.py`** ⭐ - Main dashboard creator
   - Generates `resilience_integrated_dashboard.html`
   - Embeds all data (no external files needed)
   - Run this to regenerate the main dashboard

6. **`create_complete_timeline_dashboard.py`** - Timeline map creator
7. **`create_forecast_dashboard.py`** - Forecast animation creator
8. **`create_analytics_dashboard.py`** - Graphs-only creator

### Data Processing (Legacy)
- `reconstruct_data.py` - Extracted 262 countries from corrupted JSON
- `merge_inform_data.py` - Initial INFORM data merge
- `clean_data.py`, `parse_data.py`, `extract_json.py` - Various data fixes

### Utilities
- `api.py` - Flask backend (unused in final version)
- `analyze_scores.py` - Score distribution analysis
- `inspect_excel.py` - INFORM Excel file inspector

---

## 🏛️ Four Pillars of Resilience

### 💰 Financial Pillar (6 indicators)
- GDP Growth, Debt-to-GDP Ratio, Forex Reserves, Trade Balance, FDI Inflows, Inflation Rate

### 👥 Social Pillar (6 indicators)
- Gini Index, Life Expectancy, Education Index, Unemployment Rate, Poverty Headcount, Health Expenditure

### 🏛️ Institutional Pillar (6 indicators)
- Government Effectiveness, Rule of Law, Control of Corruption, Regulatory Quality, Political Stability, Voice & Accountability

### 🏗️ Infrastructure Pillar (6 indicators)
- Electric Power Consumption, Internet Access, Mobile Subscriptions, Road Quality, Water Access, Sanitation

**Overall Score = Average of 4 Pillars**

---

## 🎨 Color Coding System

Percentile-based 5-color gradient:
- 🟢 **Dark Green** (>0.66): Excellent resilience - Top 20%
- 🟢 **Light Green** (0.60-0.66): Good resilience
- 🟡 **Yellow** (0.53-0.60): Moderate resilience
- 🟠 **Orange** (0.45-0.53): Low resilience
- 🔴 **Red** (<0.45): Critical vulnerability - Bottom 20%

---

## 🔧 Setup & Installation

### Prerequisites
```bash
Python 3.9+
pip (Python package manager)
```

### Install Dependencies
```bash
cd /Users/sayansen/Desktop/resilience_map_source

# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
source .venv/bin/activate  # macOS/Linux
# OR
.venv\Scripts\activate     # Windows

# Install required packages
pip install pandas numpy matplotlib seaborn openpyxl requests statsmodels scikit-learn scipy flask flask-cors
```

### Package Versions
- pandas: 2.3.3
- numpy: 2.0.2
- statsmodels: 0.14.6
- scikit-learn: 1.6.1
- scipy: 1.13.1
- requests: 2.32.5

---

## 🚀 Usage

### Quick Start (No Setup Required)
Simply open **`resilience_integrated_dashboard.html`** in any modern web browser. Everything is embedded!

### Regenerate Main Dashboard
```bash
source .venv/bin/activate
python create_integrated_dashboard.py
open resilience_integrated_dashboard.html
```

### Update Data from World Bank
```bash
source .venv/bin/activate
python fetch_live_data.py                    # Fetch latest World Bank data
python integrate_inform_data.py              # Merge with INFORM Risk
python forecast_resilience.py                # Generate new forecasts
python create_historical_forecast_data.py    # Create timeline
python create_integrated_dashboard.py        # Regenerate dashboard
```

### Full Pipeline (Complete Rebuild)
```bash
source .venv/bin/activate

# Step 1: Get fresh data
python fetch_live_data.py

# Step 2: Integrate INFORM Risk data
# (Requires INFORM_Risk_Mid_2025_v071.xlsx in parent directory)
python integrate_inform_data.py

# Step 3: Generate forecasts
python forecast_resilience.py

# Step 4: Create historical timeline
python create_historical_forecast_data.py

# Step 5: Generate dashboard
python create_integrated_dashboard.py

# Open result
open resilience_integrated_dashboard.html
```

---

## 📐 Methodology

### Score Calculation
```
normalized_value = (value - min) / (max - min)
pillar_score = Σ(weight_i × normalized_indicator_i) / Σ(weight_i)
overall_score = (financial + social + institutional + infrastructure) / 4
```

### BSTS Model
```
y_t = μ_t + β'x_t + ε_t
μ_t = μ_(t-1) + δ_(t-1) + η_t
δ_t = δ_(t-1) + ζ_t
```

### DFM Model
```
X_t = Λf_t + e_t
f_t = Φf_(t-1) + u_t
```

### Zero Percentile Weighting
```
weight_i = 1 - |percentile_i - 0.5| × 2
```
Emphasizes extreme performers (top and bottom 20%)

### Historical Generation
```
value_t = current_value × (1 + trend × years_back + volatility × ε)
trend ~ U(-0.01, 0.015)
volatility ~ U(0.02, 0.08)
```

---

## 📁 File Structure

```
resilience_map_source/
├── README.md                                    # This file
│
├── 🎯 MAIN DELIVERABLE
│   └── resilience_integrated_dashboard.html    # ⭐ Use this!
│
├── 📊 CORE DATA FILES
│   ├── resilience_timeline_2019_2030.json      # Main dataset (2019-2030)
│   ├── world.geojson                           # Country boundaries
│   ├── resilience_data_complete.json           # 2025 baseline
│   └── resilience_forecasts_2025_2030.json     # Forecast results
│
├── 🐍 PYTHON SCRIPTS
│   ├── create_integrated_dashboard.py          # Main dashboard generator
│   ├── fetch_live_data.py                      # World Bank API
│   ├── integrate_inform_data.py                # INFORM integration
│   ├── forecast_resilience.py                  # BSTS+DFM model
│   └── create_historical_forecast_data.py      # Timeline generator
│
├── 📈 ALTERNATIVE DASHBOARDS
│   ├── resilience_complete_timeline.html       # Timeline-only
│   ├── resilience_forecast_dashboard.html      # Forecast animation
│   └── resilience_analytics_graphs.html        # Charts-only
│
├── 🗂️ LEGACY/INTERMEDIATE FILES
│   ├── resilience_data_live.json
│   ├── resilience_data_cleaned.json
│   └── [various processing scripts]
│
└── .venv/                                       # Python virtual environment
```

---

## 🌐 Data Sources

### World Bank Open Data API
- URL: https://data.worldbank.org/
- Coverage: 254 countries
- Indicators: 24 across 4 pillars
- Update frequency: Annual
- License: CC BY-4.0

### INFORM Risk Index 2025
- URL: https://drmkc.jrc.ec.europa.eu/inform-index
- Coverage: 71 countries (matched to our dataset)
- Components: Hazard, Vulnerability, Coping Capacity
- Version: Mid-2025 v0.7.1
- File: `INFORM_Risk_Mid_2025_v071.xlsx` (parent directory)

### Natural Earth GeoJSON
- URL: https://www.naturalearthdata.com/
- Features: 258 country boundaries
- License: Public Domain

---

## 🔄 Version History

### Version 2.0 (16 January 2026) - Current
- ✅ Integrated dashboard with 3 tabs (Map + Analytics + Methodology)
- ✅ Fixed color coding with correct GeoJSON property names
- ✅ 253 countries with valid ISO3 codes
- ✅ All data embedded (fully offline capable)
- ✅ Complete 2019-2030 timeline
- ✅ BSTS+DFM forecasting with Zero Percentile Weights

### Version 1.5 (15 January 2026)
- Historical + Forecast timeline integration
- Separate analytics dashboard
- Multi-pillar choropleth maps

### Version 1.0 (14 January 2026)
- Initial BSTS+DFM forecasting
- Basic timeline functionality
- World Bank API integration

---

## 🎓 Citation

**Suggested Citation:**
```
Global Resilience Dashboard (2026). Integrated analysis of 253 countries 
using World Bank indicators, INFORM Risk data, BSTS forecasting, and 
Dynamic Factor Models. Historical data (2019-2025) and forecasts (2026-2030).
Created: 16 January 2026.
```

---

## 🐛 Known Limitations

1. **Historical Data Simulation**: 2019-2024 values are generated using smooth random walks, not actual historical data
2. **Data Latency**: Most recent World Bank data is 2022-2023; 2025 values extrapolated
3. **Missing Data**: Some indicators unavailable for all countries; mean imputation used
4. **Forecast Uncertainty**: 95% confidence intervals provided; actual outcomes may vary significantly
5. **Model Assumptions**: Assumes continuation of current trends; does not account for shocks (wars, pandemics, etc.)
6. **Coverage**: 253 countries have complete data; 71 missing or aggregates

---

## 📧 Support & Updates

**Next Scheduled Update:** July 2026 (with new World Bank data release)

To update:
1. Run `fetch_live_data.py` to get latest World Bank data
2. Follow full pipeline steps above
3. Regenerate dashboard

---

## 📜 License

**Data Sources:**
- World Bank Data: CC BY-4.0
- INFORM Risk: Open Access
- Natural Earth: Public Domain

**Dashboard Code:**
- HTML/CSS/JavaScript: Free to use and modify
- Python Scripts: Free to use and modify

---

## ✅ Quick Checklist

**What you have:**
- [x] Main dashboard (resilience_integrated_dashboard.html)
- [x] All required data files (JSON + GeoJSON)
- [x] Python scripts for data collection & forecasting
- [x] Virtual environment with dependencies
- [x] Complete methodology documentation

**To share/backup:**
1. Copy entire `resilience_map_source` folder
2. Main dashboard works standalone (just the HTML file)
3. To regenerate: Need Python 3.9+ and install dependencies

**To use offline:**
- Just open `resilience_integrated_dashboard.html` in any browser
- No internet connection required
- All data embedded in HTML file

---

## 🎉 You're All Set!

Everything is ready to use. The dashboard is fully functional and can be:
- ✅ Opened directly in any browser
- ✅ Shared as a single HTML file
- ✅ Regenerated with updated data anytime
- ✅ Customized via Python scripts

**Start here:** Open `resilience_integrated_dashboard.html`

---

*Last updated: 16 January 2026*
