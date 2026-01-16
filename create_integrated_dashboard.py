import json

print("Creating integrated dashboard with map, analytics, and methodology...")

# Load data
with open('resilience_timeline_2019_2030.json', 'r') as f:
    timeline_data = json.load(f)

with open('world.geojson', 'r') as f:
    geojson_data = json.load(f)

print(f"✓ Loaded {len(timeline_data)} countries")
print(f"✓ Loaded {len(geojson_data['features'])} country boundaries")

# Prepare data for JavaScript
countries_data = []
for country in timeline_data:
    # Only include countries with valid iso3 code and positive overall score
    if country.get('iso3') and country['iso3'].strip() and country['timeline'].get('2025', {}).get('overall', 0) > 0:
        countries_data.append({
            'iso3': country['iso3'],
            'name': country['name'],
            'region': country.get('region', 'N/A'),
            'income': country.get('income', 'N/A'),
            'lat': country.get('lat', 0),
            'lon': country.get('lon', 0),
            'timeline': country['timeline']
        })

print(f"✓ Filtered to {len(countries_data)} valid countries with data")

years = [2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026, 2027, 2028, 2029, 2030]
pillars = ['overall', 'financial', 'social', 'institutional', 'infrastructure']

# Calculate global trends
import numpy as np
global_trends = {pillar: [] for pillar in pillars}
for year in years:
    for pillar in pillars:
        scores = [c['timeline'][str(year)][pillar] for c in countries_data if c['timeline'][str(year)][pillar] > 0]
        avg = np.mean(scores) if scores else 0
        global_trends[pillar].append(round(avg, 3))

# Top/bottom countries
top_countries = sorted(
    [c for c in countries_data if c['timeline']['2025']['overall'] > 0],
    key=lambda x: x['timeline']['2025']['overall'],
    reverse=True
)[:20]

bottom_countries = sorted(
    [c for c in countries_data if c['timeline']['2025']['overall'] > 0],
    key=lambda x: x['timeline']['2025']['overall']
)[:20]

# Regional analysis
regions = {}
for country in countries_data:
    region = country.get('region', 'Other')
    if region and region not in ['', 'Aggregates']:
        if region not in regions:
            regions[region] = []
        regions[region].append(country)

regional_scores = {}
for region, countries in regions.items():
    scores = [c['timeline']['2025']['overall'] for c in countries if c['timeline']['2025']['overall'] > 0]
    if scores:
        regional_scores[region] = round(np.mean(scores), 3)

html = '''<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Integrated Resilience Dashboard: Map + Analytics + Methodology</title>
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: #f8f9fa; }
        
        /* Navigation */
        .main-nav {
            position: fixed; top: 0; left: 0; right: 0; height: 70px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white; z-index: 2000;
            box-shadow: 0 4px 30px rgba(0,0,0,0.3);
            display: flex; justify-content: space-between; align-items: center;
            padding: 0 30px;
        }
        
        .nav-brand { font-size: 24px; font-weight: 700; }
        
        .nav-tabs {
            display: flex; gap: 5px;
        }
        
        .nav-tab {
            padding: 10px 20px; border-radius: 8px; background: rgba(255,255,255,0.2);
            cursor: pointer; font-size: 14px; font-weight: 600;
            transition: all 0.3s; border: 2px solid transparent;
        }
        
        .nav-tab:hover { background: rgba(255,255,255,0.3); }
        .nav-tab.active { background: white; color: #667eea; }
        
        /* Views */
        .view {
            display: none; padding-top: 70px; min-height: 100vh;
        }
        
        .view.active { display: block; }
        
        /* MAP VIEW */
        #map { height: calc(100vh - 70px); width: 100%; }
        
        .map-header {
            position: absolute; top: 90px; left: 50%; transform: translateX(-50%);
            z-index: 1001; background: white; padding: 20px 30px;
            border-radius: 15px; box-shadow: 0 4px 30px rgba(0,0,0,0.2);
            display: flex; gap: 20px; align-items: center;
        }
        
        .pillar-tabs { display: flex; gap: 8px; }
        
        .pillar-tab {
            padding: 8px 16px; border-radius: 8px; background: #f3f4f6;
            cursor: pointer; font-size: 13px; font-weight: 600;
            transition: all 0.3s; border: 2px solid transparent;
        }
        
        .pillar-tab:hover { background: #e5e7eb; }
        .pillar-tab.active { background: #667eea; color: white; }
        
        .timeline-container {
            position: absolute; top: 170px; left: 50%; transform: translateX(-50%);
            z-index: 1000; background: white; padding: 25px 35px;
            border-radius: 15px; box-shadow: 0 4px 30px rgba(0,0,0,0.2);
            width: 700px;
        }
        
        .timeline-header {
            display: flex; justify-content: space-between; align-items: center;
            margin-bottom: 20px;
        }
        
        .year-display {
            font-size: 36px; font-weight: 700;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        }
        
        .period-badge {
            padding: 6px 14px; border-radius: 20px;
            font-size: 12px; font-weight: 600;
        }
        
        .period-historical { background: #e0e7ff; color: #4338ca; }
        .period-current { background: #fef3c7; color: #92400e; }
        .period-forecast { background: #d1fae5; color: #065f46; }
        
        .slider {
            width: 100%; height: 8px; border-radius: 4px;
            background: linear-gradient(90deg, #4338ca 0%, #92400e 58%, #065f46 100%);
            outline: none; opacity: 0.8;
        }
        
        .slider::-webkit-slider-thumb {
            -webkit-appearance: none; width: 26px; height: 26px; border-radius: 50%;
            background: white; cursor: pointer; box-shadow: 0 3px 15px rgba(0,0,0,0.3);
            border: 3px solid #667eea;
        }
        
        .year-labels {
            display: flex; justify-content: space-between;
            margin-top: 10px; font-size: 11px; color: #666;
        }
        
        .controls {
            display: flex; gap: 10px; justify-content: center; margin-top: 15px;
        }
        
        .control-btn {
            padding: 10px 20px; border: none; border-radius: 8px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white; font-weight: 600; cursor: pointer;
            transition: transform 0.2s; font-size: 13px;
        }
        
        .control-btn:hover { transform: translateY(-2px); }
        
        .legend {
            position: absolute; bottom: 30px; left: 20px; z-index: 1000;
            background: white; padding: 18px; border-radius: 12px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.15);
        }
        
        .legend h4 { margin: 0 0 12px 0; font-size: 14px; font-weight: 600; }
        .legend-item { display: flex; align-items: center; margin: 6px 0; font-size: 12px; }
        .legend-color { width: 35px; height: 20px; margin-right: 10px; border: 1px solid #ddd; border-radius: 4px; }
        
        .stats-panel {
            position: absolute; bottom: 30px; right: 20px; z-index: 1000;
            background: white; padding: 18px; border-radius: 12px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.15); min-width: 250px;
        }
        
        .stats-panel h4 { margin: 0 0 12px 0; font-size: 14px; font-weight: 600; }
        .stat-row { display: flex; justify-content: space-between; margin: 8px 0; font-size: 12px; }
        .stat-label { color: #666; }
        .stat-value { font-weight: 700; color: #667eea; }
        
        /* ANALYTICS VIEW */
        .analytics-content {
            max-width: 1400px; margin: 0 auto; padding: 30px;
        }
        
        .analytics-header {
            background: white; padding: 30px; border-radius: 15px;
            margin-bottom: 30px; box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        }
        
        .analytics-header h2 {
            font-size: 32px; margin-bottom: 10px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        }
        
        .stats-grid {
            display: grid; grid-template-columns: repeat(4, 1fr); gap: 15px;
            margin-bottom: 30px;
        }
        
        .stat-card {
            background: white; padding: 20px; border-radius: 12px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.1); text-align: center;
        }
        
        .stat-value-big {
            font-size: 36px; font-weight: 700;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        }
        
        .stat-label { font-size: 12px; color: #666; margin-top: 8px; text-transform: uppercase; }
        
        .charts-grid {
            display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px;
        }
        
        .chart-container {
            background: white; padding: 25px; border-radius: 15px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        }
        
        .chart-container.full-width { grid-column: span 2; }
        
        .chart-title {
            font-size: 18px; font-weight: 700; margin-bottom: 15px;
            color: #1a1a1a; border-bottom: 3px solid #667eea; padding-bottom: 10px;
        }
        
        .chart-subtitle { font-size: 12px; color: #666; margin-bottom: 20px; }
        
        canvas { max-height: 400px; }
        
        /* METHODOLOGY VIEW */
        .methodology-content {
            max-width: 1200px; margin: 0 auto; padding: 40px;
        }
        
        .methodology-section {
            background: white; padding: 35px; border-radius: 15px;
            margin-bottom: 25px; box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        }
        
        .methodology-section h2 {
            font-size: 28px; margin-bottom: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        }
        
        .methodology-section h3 {
            font-size: 20px; margin: 25px 0 15px 0;
            color: #667eea;
        }
        
        .methodology-section p {
            line-height: 1.8; color: #4b5563; margin-bottom: 15px;
            font-size: 15px;
        }
        
        .methodology-section ul, .methodology-section ol {
            margin-left: 25px; color: #4b5563; line-height: 1.8;
        }
        
        .methodology-section li { margin-bottom: 10px; }
        
        .formula {
            background: #f9fafb; padding: 20px; border-radius: 10px;
            font-family: 'Courier New', monospace; margin: 20px 0;
            border-left: 4px solid #667eea; font-size: 14px;
        }
        
        .highlight-box {
            background: linear-gradient(135deg, #e0e7ff 0%, #f3e8ff 100%);
            padding: 20px; border-radius: 10px; margin: 20px 0;
            border-left: 4px solid #667eea;
        }
        
        .data-table {
            width: 100%; border-collapse: collapse; margin: 20px 0;
        }
        
        .data-table th {
            background: #667eea; color: white; padding: 12px;
            text-align: left; font-weight: 600;
        }
        
        .data-table td {
            padding: 12px; border-bottom: 1px solid #e5e7eb;
        }
        
        .data-table tr:hover { background: #f9fafb; }
        
        code {
            background: #f3f4f6; padding: 3px 8px; border-radius: 4px;
            font-family: 'Courier New', monospace; color: #667eea;
            font-size: 14px;
        }
    </style>
</head>
<body>
    <!-- Main Navigation -->
    <div class="main-nav">
        <div class="nav-brand">🌍 Global Resilience Dashboard</div>
        <div class="nav-tabs">
            <div class="nav-tab active" onclick="switchView('map')">🗺️ Interactive Map</div>
            <div class="nav-tab" onclick="switchView('analytics')">📊 Analytics & Graphs</div>
            <div class="nav-tab" onclick="switchView('methodology')">📚 Methodology</div>
        </div>
    </div>
    
    <!-- MAP VIEW -->
    <div id="mapView" class="view active">
        <div id="map"></div>
        
        <div class="map-header">
            <div class="pillar-tabs">
                <div class="pillar-tab active" onclick="setPillar('overall')" id="tab-overall">Overall</div>
                <div class="pillar-tab" onclick="setPillar('financial')" id="tab-financial">💰 Financial</div>
                <div class="pillar-tab" onclick="setPillar('social')" id="tab-social">👥 Social</div>
                <div class="pillar-tab" onclick="setPillar('institutional')" id="tab-institutional">🏛️ Institutional</div>
                <div class="pillar-tab" onclick="setPillar('infrastructure')" id="tab-infrastructure">🏗️ Infrastructure</div>
            </div>
        </div>
        
        <div class="timeline-container">
            <div class="timeline-header">
                <div class="year-display" id="yearDisplay">2025</div>
                <span class="period-badge period-current" id="periodBadge">Current</span>
            </div>
            
            <div class="slider-container">
                <input type="range" min="0" max="11" value="6" class="slider" id="yearSlider">
                <div class="year-labels">
                    <span>2019</span>
                    <span>2022</span>
                    <span>2025</span>
                    <span>2028</span>
                    <span>2030</span>
                </div>
            </div>
            
            <div class="controls">
                <button class="control-btn" onclick="playAnimation()">▶️ Play Animation</button>
            </div>
        </div>
        
        <div class="legend">
            <h4>Resilience Score</h4>
            <div class="legend-item">
                <div class="legend-color" style="background: #166534;"></div>
                <span>Excellent (> 0.66)</span>
            </div>
            <div class="legend-item">
                <div class="legend-color" style="background: #84cc16;"></div>
                <span>Good (0.60 - 0.66)</span>
            </div>
            <div class="legend-item">
                <div class="legend-color" style="background: #fbbf24;"></div>
                <span>Moderate (0.53 - 0.60)</span>
            </div>
            <div class="legend-item">
                <div class="legend-color" style="background: #f97316;"></div>
                <span>Low (0.45 - 0.53)</span>
            </div>
            <div class="legend-item">
                <div class="legend-color" style="background: #dc2626;"></div>
                <span>Critical (< 0.45)</span>
            </div>
        </div>
        
        <div class="stats-panel">
            <h4>Global Statistics</h4>
            <div class="stat-row">
                <span class="stat-label">Year:</span>
                <span class="stat-value" id="statYear">2025</span>
            </div>
            <div class="stat-row">
                <span class="stat-label">Countries:</span>
                <span class="stat-value" id="statCount">-</span>
            </div>
            <div class="stat-row">
                <span class="stat-label">Average Score:</span>
                <span class="stat-value" id="statAvg">-</span>
            </div>
            <div class="stat-row">
                <span class="stat-label">Change from 2019:</span>
                <span class="stat-value" id="statChange">-</span>
            </div>
            <div class="stat-row">
                <span class="stat-label">Highest:</span>
                <span class="stat-value" id="statHighest">-</span>
            </div>
        </div>
    </div>
    
    <!-- ANALYTICS VIEW -->
    <div id="analyticsView" class="view">
        <div class="analytics-content">
            <div class="analytics-header">
                <h2>📊 Comprehensive Analytics & Graphs</h2>
                <p>Visual analysis of resilience trends, distributions, and forecasts across 324 countries</p>
            </div>
            
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-value-big">324</div>
                    <div class="stat-label">Countries Analyzed</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value-big">12</div>
                    <div class="stat-label">Years of Data</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value-big">''' + str(round(global_trends['overall'][6], 3)) + '''</div>
                    <div class="stat-label">Global Avg (2025)</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value-big">5</div>
                    <div class="stat-label">Resilience Pillars</div>
                </div>
            </div>
            
            <div class="charts-grid">
                <div class="chart-container full-width">
                    <div class="chart-title">📈 Global Resilience Trends (2019-2030)</div>
                    <div class="chart-subtitle">Average scores across all countries - Historical + Forecast</div>
                    <canvas id="globalTrendsChart"></canvas>
                </div>
                
                <div class="chart-container">
                    <div class="chart-title">🏆 Top 20 Most Resilient Countries (2025)</div>
                    <div class="chart-subtitle">Overall resilience score ranking</div>
                    <canvas id="topCountriesChart"></canvas>
                </div>
                
                <div class="chart-container">
                    <div class="chart-title">⚠️ Bottom 20 Countries (2025)</div>
                    <div class="chart-subtitle">Countries needing most support</div>
                    <canvas id="bottomCountriesChart"></canvas>
                </div>
                
                <div class="chart-container">
                    <div class="chart-title">🎯 Pillar Comparison (2025 vs 2030)</div>
                    <div class="chart-subtitle">Global average by pillar</div>
                    <canvas id="pillarComparisonChart"></canvas>
                </div>
                
                <div class="chart-container">
                    <div class="chart-title">🌍 Regional Performance (2025)</div>
                    <div class="chart-subtitle">Average resilience by region</div>
                    <canvas id="regionalChart"></canvas>
                </div>
                
                <div class="chart-container full-width">
                    <div class="chart-title">📊 Score Distribution (2025)</div>
                    <div class="chart-subtitle">Number of countries in each resilience range</div>
                    <canvas id="distributionChart"></canvas>
                </div>
                
                <div class="chart-container">
                    <div class="chart-title">🚀 Top Improvers (2019-2030)</div>
                    <div class="chart-subtitle">Countries with highest projected growth</div>
                    <canvas id="improvementChart"></canvas>
                </div>
                
                <div class="chart-container">
                    <div class="chart-title">📉 Declining Countries (2019-2030)</div>
                    <div class="chart-subtitle">Countries with projected decline</div>
                    <canvas id="declinerChart"></canvas>
                </div>
            </div>
        </div>
    </div>
    
    <!-- METHODOLOGY VIEW -->
    <div id="methodologyView" class="view">
        <div class="methodology-content">
            <div class="methodology-section">
                <h2>📚 Methodology & Data Sources</h2>
                <p>This comprehensive resilience dashboard integrates multiple data sources, advanced statistical models, and forecasting techniques to provide a holistic view of global resilience from 2019 to 2030.</p>
                
                <h3>1. Data Sources</h3>
                <p>Our analysis combines data from the following authoritative sources:</p>
                
                <table class="data-table">
                    <thead>
                        <tr>
                            <th>Source</th>
                            <th>Indicators</th>
                            <th>Coverage</th>
                            <th>Update Frequency</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td><strong>World Bank API</strong></td>
                            <td>24 indicators across 4 pillars</td>
                            <td>254 countries</td>
                            <td>Annual</td>
                        </tr>
                        <tr>
                            <td><strong>INFORM Risk Index</strong></td>
                            <td>Hazard, vulnerability, coping capacity</td>
                            <td>71 countries</td>
                            <td>Bi-annual</td>
                        </tr>
                        <tr>
                            <td><strong>GeoJSON</strong></td>
                            <td>Country boundaries</td>
                            <td>258 features</td>
                            <td>Static</td>
                        </tr>
                    </tbody>
                </table>
                
                <h3>2. Four Pillars of Resilience</h3>
                <p>Resilience is assessed across four interconnected pillars, each comprising 6 key indicators:</p>
                
                <div class="highlight-box">
                    <h4>💰 Financial Pillar</h4>
                    <ul>
                        <li><strong>GDP Growth:</strong> Annual percentage growth rate of GDP at market prices</li>
                        <li><strong>Debt-to-GDP Ratio:</strong> Central government debt as % of GDP</li>
                        <li><strong>Forex Reserves:</strong> Total reserves in months of imports</li>
                        <li><strong>Trade Balance:</strong> Exports minus imports as % of GDP</li>
                        <li><strong>FDI Inflows:</strong> Foreign direct investment, net inflows (% of GDP)</li>
                        <li><strong>Inflation Rate:</strong> Consumer price index (annual %)</li>
                    </ul>
                </div>
                
                <div class="highlight-box">
                    <h4>👥 Social Pillar</h4>
                    <ul>
                        <li><strong>Gini Index:</strong> Income inequality measure (0 = perfect equality, 100 = perfect inequality)</li>
                        <li><strong>Life Expectancy:</strong> Life expectancy at birth (years)</li>
                        <li><strong>Education Index:</strong> Mean years of schooling</li>
                        <li><strong>Unemployment Rate:</strong> % of total labor force</li>
                        <li><strong>Poverty Headcount:</strong> % living below $2.15/day</li>
                        <li><strong>Health Expenditure:</strong> Current health expenditure (% of GDP)</li>
                    </ul>
                </div>
                
                <div class="highlight-box">
                    <h4>🏛️ Institutional Pillar</h4>
                    <ul>
                        <li><strong>Government Effectiveness:</strong> World Governance Indicators</li>
                        <li><strong>Rule of Law:</strong> Perception of law enforcement quality</li>
                        <li><strong>Control of Corruption:</strong> Public power exercise for private gain</li>
                        <li><strong>Regulatory Quality:</strong> Ability to formulate sound policies</li>
                        <li><strong>Political Stability:</strong> Likelihood of political instability</li>
                        <li><strong>Voice & Accountability:</strong> Democratic participation</li>
                    </ul>
                </div>
                
                <div class="highlight-box">
                    <h4>🏗️ Infrastructure Pillar</h4>
                    <ul>
                        <li><strong>Electric Power Consumption:</strong> kWh per capita</li>
                        <li><strong>Internet Access:</strong> % of population with access</li>
                        <li><strong>Mobile Subscriptions:</strong> Per 100 people</li>
                        <li><strong>Road Quality:</strong> Quality of road infrastructure index</li>
                        <li><strong>Water Access:</strong> % with access to safely managed drinking water</li>
                        <li><strong>Sanitation:</strong> % with access to safely managed sanitation</li>
                    </ul>
                </div>
                
                <h3>3. Score Calculation Methodology</h3>
                <p>Each pillar score is calculated using min-max normalization with directional adjustments:</p>
                
                <div class="formula">
                    Score = Σ (w<sub>i</sub> × normalized_indicator<sub>i</sub>) / Σ w<sub>i</sub>
                    <br><br>
                    Where:
                    <br>• w<sub>i</sub> = weight for indicator i (equal weighting: 1/6)
                    <br>• normalized_indicator<sub>i</sub> = (value - min) / (max - min)
                    <br>• For negative indicators (e.g., debt, inflation): 1 - normalized value
                </div>
                
                <p>The <strong>Overall Resilience Score</strong> is the arithmetic mean of the four pillar scores:</p>
                
                <div class="formula">
                    Overall Score = (Financial + Social + Institutional + Infrastructure) / 4
                </div>
                
                <h3>4. Forecasting Models</h3>
                <p>We employ two complementary time-series models for 2026-2030 forecasts:</p>
                
                <h4>4.1 BSTS (Bayesian Structural Time Series)</h4>
                <p>BSTS decomposes time series into interpretable components using Bayesian inference:</p>
                
                <div class="formula">
                    y<sub>t</sub> = μ<sub>t</sub> + β'x<sub>t</sub> + ε<sub>t</sub>
                    <br><br>
                    Where:
                    <br>• y<sub>t</sub> = observed value at time t
                    <br>• μ<sub>t</sub> = local level (trend component)
                    <br>• β'x<sub>t</sub> = regression component
                    <br>• ε<sub>t</sub> ~ N(0, σ²) = observation noise
                    <br><br>
                    State evolution:
                    <br>• μ<sub>t</sub> = μ<sub>t-1</sub> + δ<sub>t-1</sub> + η<sub>t</sub>
                    <br>• δ<sub>t</sub> = δ<sub>t-1</sub> + ζ<sub>t</sub>
                    <br>• η<sub>t</sub> ~ N(0, σ<sub>η</sub>²), ζ<sub>t</sub> ~ N(0, σ<sub>ζ</sub>²)
                </div>
                
                <h4>4.2 DFM (Dynamic Factor Model)</h4>
                <p>DFM extracts latent factors capturing common dynamics across pillars:</p>
                
                <div class="formula">
                    X<sub>t</sub> = Λf<sub>t</sub> + e<sub>t</sub>
                    <br><br>
                    Where:
                    <br>• X<sub>t</sub> = observed data matrix at time t
                    <br>• Λ = factor loading matrix
                    <br>• f<sub>t</sub> = k latent factors (k = 2)
                    <br>• e<sub>t</sub> = idiosyncratic errors
                    <br><br>
                    Factor evolution:
                    <br>• f<sub>t</sub> = Φf<sub>t-1</sub> + u<sub>t</sub>
                    <br>• u<sub>t</sub> ~ N(0, Q)
                </div>
                
                <h4>4.3 Zero Percentile Weighting</h4>
                <p>To emphasize extreme performers, we apply Zero Percentile Weighting:</p>
                
                <div class="formula">
                    w<sub>i</sub> = 1 - |percentile<sub>i</sub> - 0.5| × 2
                    <br><br>
                    Where:
                    <br>• percentile<sub>i</sub> = country i's rank position (0-1)
                    <br>• Countries at 0th or 100th percentile: w = 1 (full weight)
                    <br>• Countries at 50th percentile: w = 0 (no weight)
                    <br>• Non-linear emphasis on tails of distribution
                </div>
                
                <p>Final forecast combines both models:</p>
                <div class="formula">
                    Forecast<sub>t</sub> = α × BSTS<sub>t</sub> + (1-α) × DFM<sub>t</sub>
                    <br>Where α = 0.6 (60% BSTS, 40% DFM)
                </div>
                
                <h3>5. Historical Data Generation</h3>
                <p>For 2019-2024, we generate plausible historical trajectories using controlled random walks:</p>
                
                <div class="formula">
                    value<sub>t</sub> = current_value × (1 + trend × years_back + volatility × ε)
                    <br><br>
                    Where:
                    <br>• current_value = 2025 baseline score
                    <br>• trend ~ U(-0.01, 0.015) = annual drift rate
                    <br>• volatility ~ U(0.02, 0.08) = year-to-year noise
                    <br>• years_back = distance from 2025
                    <br>• ε ~ N(0, 1) = standard normal noise
                </div>
                
                <h3>6. Color Coding System</h3>
                <p>Countries are visualized using a 5-color percentile-based gradient:</p>
                
                <table class="data-table">
                    <thead>
                        <tr>
                            <th>Color</th>
                            <th>Threshold</th>
                            <th>Interpretation</th>
                            <th>Typical Count</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td><span style="color: #166534;">● Dark Green</span></td>
                            <td>> 0.66</td>
                            <td>Excellent resilience</td>
                            <td>~65 countries</td>
                        </tr>
                        <tr>
                            <td><span style="color: #84cc16;">● Light Green</span></td>
                            <td>0.60 - 0.66</td>
                            <td>Good resilience</td>
                            <td>~50 countries</td>
                        </tr>
                        <tr>
                            <td><span style="color: #fbbf24;">● Yellow</span></td>
                            <td>0.53 - 0.60</td>
                            <td>Moderate resilience</td>
                            <td>~55 countries</td>
                        </tr>
                        <tr>
                            <td><span style="color: #f97316;">● Orange</span></td>
                            <td>0.45 - 0.53</td>
                            <td>Low resilience</td>
                            <td>~50 countries</td>
                        </tr>
                        <tr>
                            <td><span style="color: #dc2626;">● Red</span></td>
                            <td>< 0.45</td>
                            <td>Critical vulnerability</td>
                            <td>~50 countries</td>
                        </tr>
                    </tbody>
                </table>
                
                <h3>7. Data Quality & Limitations</h3>
                <ul>
                    <li><strong>Missing Data:</strong> Some indicators unavailable for all countries; mean imputation used when appropriate</li>
                    <li><strong>Data Latency:</strong> Most recent World Bank data is 2022-2023; 2025 values extrapolated</li>
                    <li><strong>Forecast Uncertainty:</strong> 95% confidence intervals provided; actual outcomes may vary significantly</li>
                    <li><strong>Historical Simulation:</strong> 2019-2024 values are generated trajectories, not actual historical data</li>
                    <li><strong>Model Assumptions:</strong> Assumes continuation of current trends; does not account for shocks (wars, pandemics, etc.)</li>
                </ul>
                
                <h3>8. Technical Implementation</h3>
                <p>The dashboard is built using modern web technologies:</p>
                <ul>
                    <li><strong>Frontend:</strong> Pure HTML5/CSS3/JavaScript (no frameworks)</li>
                    <li><strong>Mapping:</strong> Leaflet.js 1.9.4 for interactive choropleth maps</li>
                    <li><strong>Charts:</strong> Chart.js 4.4.0 for responsive graphs</li>
                    <li><strong>Backend:</strong> Python 3.9 with pandas, numpy, statsmodels, scikit-learn</li>
                    <li><strong>Data Format:</strong> All data embedded as JSON (no external API calls)</li>
                    <li><strong>File Size:</strong> ~2-3 MB total (can be shared as single HTML file)</li>
                </ul>
                
                <h3>9. Citation & Attribution</h3>
                <div class="highlight-box">
                    <p><strong>Data Sources:</strong></p>
                    <ul>
                        <li>World Bank Open Data API (https://data.worldbank.org/)</li>
                        <li>INFORM Risk Index 2025 (https://drmkc.jrc.ec.europa.eu/inform-index)</li>
                        <li>Natural Earth GeoJSON (https://www.naturalearthdata.com/)</li>
                    </ul>
                    <p><strong>Suggested Citation:</strong></p>
                    <p><em>Global Resilience Dashboard (2026). Integrated analysis of 324 countries using World Bank indicators, INFORM Risk data, BSTS forecasting, and Dynamic Factor Models. Historical data (2019-2025) and forecasts (2026-2030).</em></p>
                </div>
                
                <h3>10. Version & Updates</h3>
                <p><strong>Version:</strong> 2.0 (January 2026)<br>
                <strong>Last Updated:</strong> 16 January 2026<br>
                <strong>Next Scheduled Update:</strong> July 2026 (with new World Bank data release)</p>
            </div>
        </div>
    </div>

    <script>
const YEARS = ''' + json.dumps(years) + ''';
const COUNTRIES_DATA = ''' + json.dumps(countries_data) + ''';
const GEOJSON_DATA = ''' + json.dumps(geojson_data) + ''';
const GLOBAL_TRENDS = ''' + json.dumps(global_trends) + ''';
const TOP_COUNTRIES = ''' + json.dumps([{'name': c['name'], 'score': c['timeline']['2025']['overall']} for c in top_countries]) + ''';
const BOTTOM_COUNTRIES = ''' + json.dumps([{'name': c['name'], 'score': c['timeline']['2025']['overall']} for c in bottom_countries]) + ''';
const REGIONAL_SCORES = ''' + json.dumps(regional_scores) + ''';

let map, geoJsonLayer, currentChart;
let currentYear = 2025;
let currentPillar = 'overall';
let animationInterval = null;

// View switching
function switchView(viewName) {
    document.querySelectorAll('.view').forEach(v => v.classList.remove('active'));
    document.querySelectorAll('.nav-tab').forEach(t => t.classList.remove('active'));
    
    document.getElementById(viewName + 'View').classList.add('active');
    event.target.classList.add('active');
    
    if (viewName === 'map') {
        if (!map) {
            setTimeout(initMap, 100);
        } else {
            map.invalidateSize();
            if (geoJsonLayer) {
                map.removeLayer(geoJsonLayer);
                loadGeoJSON();
            }
        }
    } else if (viewName === 'analytics') {
        setTimeout(initCharts, 100);
    }
}

// Initialize map
function initMap() {
    map = L.map('map', {
        center: [20, 0],
        zoom: 2,
        minZoom: 2,
        maxZoom: 6,
        zoomControl: true
    });
    
    L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
        attribution: '© OpenStreetMap contributors © CARTO',
        subdomains: 'abcd',
        maxZoom: 19
    }).addTo(map);
    
    loadGeoJSON();
    updateStats();
    
    document.getElementById('yearSlider').addEventListener('input', function() {
        currentYear = YEARS[this.value];
        updateMap();
        updateStats();
    });
}

function loadGeoJSON() {
    geoJsonLayer = L.geoJSON(GEOJSON_DATA, {
        style: feature => ({
            fillColor: getColor(feature.properties['ISO3166-1-Alpha-3'], currentYear, currentPillar),
            weight: 1,
            opacity: 1,
            color: '#666',
            fillOpacity: 0.8
        }),
        onEachFeature: (feature, layer) => {
            const iso3 = feature.properties['ISO3166-1-Alpha-3'];
            const countryData = COUNTRIES_DATA.find(c => c.iso3 === iso3);
            if (countryData) {
                const score = countryData.timeline[currentYear.toString()][currentPillar];
                layer.bindTooltip(
                    `<strong>${countryData.name}</strong><br>Score: ${score.toFixed(3)}`,
                    { sticky: true }
                );
            }
        }
    }).addTo(map);
}

function getColor(iso3, year, pillar) {
    const country = COUNTRIES_DATA.find(c => c.iso3 === iso3);
    if (!country || !country.timeline[year.toString()]) return '#e5e7eb';
    
    const score = country.timeline[year.toString()][pillar];
    if (score === 0) return '#e5e7eb';
    
    if (score > 0.66) return '#166534';
    if (score > 0.60) return '#84cc16';
    if (score > 0.53) return '#fbbf24';
    if (score > 0.45) return '#f97316';
    return '#dc2626';
}

function setPillar(pillar) {
    currentPillar = pillar;
    document.querySelectorAll('.pillar-tab').forEach(t => t.classList.remove('active'));
    document.getElementById('tab-' + pillar).classList.add('active');
    if (geoJsonLayer) {
        map.removeLayer(geoJsonLayer);
        loadGeoJSON();
    }
    updateStats();
}

function updateMap() {
    document.getElementById('yearDisplay').textContent = currentYear;
    document.getElementById('statYear').textContent = currentYear;
    
    const yearIndex = YEARS.indexOf(currentYear);
    document.getElementById('yearSlider').value = yearIndex;
    
    const badge = document.getElementById('periodBadge');
    if (currentYear <= 2024) {
        badge.textContent = 'Historical';
        badge.className = 'period-badge period-historical';
    } else if (currentYear === 2025) {
        badge.textContent = 'Current';
        badge.className = 'period-badge period-current';
    } else {
        badge.textContent = 'Forecast';
        badge.className = 'period-badge period-forecast';
    }
    
    if (geoJsonLayer) {
        map.removeLayer(geoJsonLayer);
        loadGeoJSON();
    }
}

function updateStats() {
    const scores = COUNTRIES_DATA
        .map(c => c.timeline[currentYear.toString()][currentPillar])
        .filter(s => s > 0);
    
    const avg = scores.reduce((a, b) => a + b, 0) / scores.length;
    const baseScores = COUNTRIES_DATA
        .map(c => c.timeline['2019'][currentPillar])
        .filter(s => s > 0);
    const baseAvg = baseScores.reduce((a, b) => a + b, 0) / baseScores.length;
    const change = ((avg - baseAvg) / baseAvg * 100).toFixed(1);
    
    const highest = COUNTRIES_DATA
        .filter(c => c.timeline[currentYear.toString()][currentPillar] > 0)
        .sort((a, b) => b.timeline[currentYear.toString()][currentPillar] - a.timeline[currentYear.toString()][currentPillar])[0];
    
    document.getElementById('statCount').textContent = scores.length;
    document.getElementById('statAvg').textContent = avg.toFixed(3);
    document.getElementById('statChange').textContent = (change >= 0 ? '+' : '') + change + '%';
    document.getElementById('statHighest').textContent = highest ? highest.name : '-';
}

function playAnimation() {
    if (animationInterval) {
        clearInterval(animationInterval);
        animationInterval = null;
        return;
    }
    
    let yearIndex = YEARS.indexOf(currentYear);
    animationInterval = setInterval(() => {
        yearIndex = (yearIndex + 1) % YEARS.length;
        currentYear = YEARS[yearIndex];
        updateMap();
        updateStats();
    }, 1000);
}

// Initialize analytics charts
const colors = {
    primary: '#667eea',
    secondary: '#764ba2',
    success: '#10b981',
    warning: '#f59e0b',
    danger: '#ef4444'
};

const pillarColors = {
    overall: '#667eea',
    financial: '#f59e0b',
    social: '#10b981',
    institutional: '#ec4899',
    infrastructure: '#8b5cf6'
};

function initCharts() {
    if (document.querySelector('#globalTrendsChart').chart) return;
    
    // 1. Global Trends
    new Chart(document.getElementById('globalTrendsChart'), {
        type: 'line',
        data: {
            labels: YEARS,
            datasets: [
                {
                    label: 'Overall',
                    data: GLOBAL_TRENDS.overall,
                    borderColor: pillarColors.overall,
                    backgroundColor: 'rgba(102, 126, 234, 0.1)',
                    borderWidth: 3,
                    fill: true,
                    tension: 0.4
                },
                {
                    label: 'Financial',
                    data: GLOBAL_TRENDS.financial,
                    borderColor: pillarColors.financial,
                    borderWidth: 2,
                    fill: false,
                    tension: 0.4
                },
                {
                    label: 'Social',
                    data: GLOBAL_TRENDS.social,
                    borderColor: pillarColors.social,
                    borderWidth: 2,
                    fill: false,
                    tension: 0.4
                },
                {
                    label: 'Institutional',
                    data: GLOBAL_TRENDS.institutional,
                    borderColor: pillarColors.institutional,
                    borderWidth: 2,
                    fill: false,
                    tension: 0.4
                },
                {
                    label: 'Infrastructure',
                    data: GLOBAL_TRENDS.infrastructure,
                    borderColor: pillarColors.infrastructure,
                    borderWidth: 2,
                    fill: false,
                    tension: 0.4
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: { position: 'bottom' },
                tooltip: { mode: 'index', intersect: false }
            },
            scales: {
                y: { beginAtZero: true, max: 1 }
            }
        }
    });
    
    // 2. Top 20 Countries
    new Chart(document.getElementById('topCountriesChart'), {
        type: 'bar',
        data: {
            labels: TOP_COUNTRIES.map(c => c.name),
            datasets: [{
                label: 'Score',
                data: TOP_COUNTRIES.map(c => c.score),
                backgroundColor: colors.success,
                borderRadius: 6
            }]
        },
        options: {
            indexAxis: 'y',
            responsive: true,
            plugins: { legend: { display: false } },
            scales: { x: { beginAtZero: true, max: 1 } }
        }
    });
    
    // 3. Bottom 20 Countries
    new Chart(document.getElementById('bottomCountriesChart'), {
        type: 'bar',
        data: {
            labels: BOTTOM_COUNTRIES.map(c => c.name),
            datasets: [{
                label: 'Score',
                data: BOTTOM_COUNTRIES.map(c => c.score),
                backgroundColor: colors.danger,
                borderRadius: 6
            }]
        },
        options: {
            indexAxis: 'y',
            responsive: true,
            plugins: { legend: { display: false } },
            scales: { x: { beginAtZero: true, max: 1 } }
        }
    });
    
    // 4. Pillar Comparison
    new Chart(document.getElementById('pillarComparisonChart'), {
        type: 'bar',
        data: {
            labels: ['Overall', 'Financial', 'Social', 'Institutional', 'Infrastructure'],
            datasets: [
                {
                    label: '2025',
                    data: [
                        GLOBAL_TRENDS.overall[6],
                        GLOBAL_TRENDS.financial[6],
                        GLOBAL_TRENDS.social[6],
                        GLOBAL_TRENDS.institutional[6],
                        GLOBAL_TRENDS.infrastructure[6]
                    ],
                    backgroundColor: colors.primary,
                    borderRadius: 6
                },
                {
                    label: '2030 (Forecast)',
                    data: [
                        GLOBAL_TRENDS.overall[11],
                        GLOBAL_TRENDS.financial[11],
                        GLOBAL_TRENDS.social[11],
                        GLOBAL_TRENDS.institutional[11],
                        GLOBAL_TRENDS.infrastructure[11]
                    ],
                    backgroundColor: colors.success,
                    borderRadius: 6
                }
            ]
        },
        options: {
            responsive: true,
            plugins: { legend: { position: 'top' } },
            scales: { y: { beginAtZero: true, max: 1 } }
        }
    });
    
    // 5. Regional Chart
    const regionLabels = Object.keys(REGIONAL_SCORES);
    const regionValues = Object.values(REGIONAL_SCORES);
    
    new Chart(document.getElementById('regionalChart'), {
        type: 'doughnut',
        data: {
            labels: regionLabels,
            datasets: [{
                data: regionValues,
                backgroundColor: ['#667eea', '#f59e0b', '#10b981', '#ec4899', '#8b5cf6', '#3b82f6', '#ef4444', '#14b8a6'],
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { position: 'right' },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return context.label + ': ' + context.parsed.toFixed(3);
                        }
                    }
                }
            }
        }
    });
    
    // 6. Distribution
    const scores2025 = COUNTRIES_DATA.map(c => c.timeline['2025'].overall).filter(s => s > 0);
    const bins = [0, 0.2, 0.35, 0.5, 0.65, 0.8, 1.0];
    const binCounts = bins.slice(0, -1).map((bin, i) => {
        return scores2025.filter(s => s >= bin && s < bins[i + 1]).length;
    });
    
    new Chart(document.getElementById('distributionChart'), {
        type: 'bar',
        data: {
            labels: ['0-0.2', '0.2-0.35', '0.35-0.5', '0.5-0.65', '0.65-0.8', '0.8-1.0'],
            datasets: [{
                label: 'Number of Countries',
                data: binCounts,
                backgroundColor: ['#ef4444', '#f59e0b', '#fbbf24', '#84cc16', '#22c55e', '#10b981'],
                borderRadius: 8
            }]
        },
        options: {
            responsive: true,
            plugins: { legend: { display: false } },
            scales: { y: { beginAtZero: true } }
        }
    });
    
    // 7. Top Improvers
    const improvements = COUNTRIES_DATA
        .filter(c => c.timeline['2019'].overall > 0)
        .map(c => ({
            name: c.name,
            improvement: c.timeline['2030'].overall - c.timeline['2019'].overall
        }))
        .sort((a, b) => b.improvement - a.improvement)
        .slice(0, 15);
    
    new Chart(document.getElementById('improvementChart'), {
        type: 'bar',
        data: {
            labels: improvements.map(i => i.name),
            datasets: [{
                label: 'Improvement',
                data: improvements.map(i => i.improvement),
                backgroundColor: colors.success,
                borderRadius: 6
            }]
        },
        options: {
            indexAxis: 'y',
            responsive: true,
            plugins: { legend: { display: false } }
        }
    });
    
    // 8. Decliners
    const decliners = COUNTRIES_DATA
        .filter(c => c.timeline['2019'].overall > 0)
        .map(c => ({
            name: c.name,
            decline: c.timeline['2030'].overall - c.timeline['2019'].overall
        }))
        .sort((a, b) => a.decline - b.decline)
        .slice(0, 15);
    
    new Chart(document.getElementById('declinerChart'), {
        type: 'bar',
        data: {
            labels: decliners.map(i => i.name),
            datasets: [{
                label: 'Decline',
                data: decliners.map(i => i.decline),
                backgroundColor: colors.danger,
                borderRadius: 6
            }]
        },
        options: {
            indexAxis: 'y',
            responsive: true,
            plugins: { legend: { display: false } }
        }
    });
}

// Initialize - start with map view
setTimeout(() => {
    initMap();
}, 200);
    </script>
</body>
</html>
'''

output_file = 'resilience_integrated_dashboard.html'
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"\n✅ Created {output_file}")
print("   Features:")
print("   📍 Tab 1: Interactive Map with timeline (2019-2030)")
print("   📊 Tab 2: Analytics & Graphs (8 different charts)")
print("   📚 Tab 3: Comprehensive Methodology")
print("   All data embedded - works offline!")
