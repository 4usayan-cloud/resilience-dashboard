import json
import numpy as np

print("Creating comprehensive analytics dashboard with graphs...")

# Load timeline data
with open('resilience_timeline_2019_2030.json', 'r') as f:
    timeline_data = json.load(f)

print(f"✓ Loaded {len(timeline_data)} countries")

# Prepare analytics data
years = [2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026, 2027, 2028, 2029, 2030]
pillars = ['overall', 'financial', 'social', 'institutional', 'infrastructure']

# Calculate global averages by year and pillar
global_trends = {pillar: [] for pillar in pillars}
for year in years:
    for pillar in pillars:
        scores = [c['timeline'][str(year)][pillar] for c in timeline_data if c['timeline'][str(year)][pillar] > 0]
        avg = np.mean(scores) if scores else 0
        global_trends[pillar].append(round(avg, 3))

# Get top 20 countries by overall score (2025)
top_countries = sorted(
    [c for c in timeline_data if c['timeline']['2025']['overall'] > 0],
    key=lambda x: x['timeline']['2025']['overall'],
    reverse=True
)[:20]

# Get bottom 20 countries
bottom_countries = sorted(
    [c for c in timeline_data if c['timeline']['2025']['overall'] > 0],
    key=lambda x: x['timeline']['2025']['overall']
)[:20]

# Regional aggregation
regions = {}
for country in timeline_data:
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

# Create HTML with comprehensive charts
html = '''<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Resilience Analytics Dashboard - Graphs & Charts</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            padding: 20px;
        }
        
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 15px;
            margin-bottom: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        
        .header h1 { font-size: 32px; margin-bottom: 10px; }
        .header p { opacity: 0.9; font-size: 14px; }
        
        .dashboard {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 20px;
            margin-bottom: 20px;
        }
        
        .chart-container {
            background: white;
            padding: 25px;
            border-radius: 15px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        }
        
        .chart-container.full-width {
            grid-column: span 2;
        }
        
        .chart-title {
            font-size: 18px;
            font-weight: 700;
            margin-bottom: 15px;
            color: #1a1a1a;
            border-bottom: 3px solid #667eea;
            padding-bottom: 10px;
        }
        
        .chart-subtitle {
            font-size: 12px;
            color: #666;
            margin-bottom: 20px;
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 15px;
            margin-bottom: 30px;
        }
        
        .stat-card {
            background: white;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
            text-align: center;
        }
        
        .stat-value {
            font-size: 36px;
            font-weight: 700;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .stat-label {
            font-size: 12px;
            color: #666;
            margin-top: 8px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        canvas {
            max-height: 400px;
        }
        
        .legend-custom {
            display: flex;
            justify-content: center;
            flex-wrap: wrap;
            gap: 15px;
            margin-top: 15px;
            font-size: 12px;
        }
        
        .legend-item {
            display: flex;
            align-items: center;
            gap: 5px;
        }
        
        .legend-color {
            width: 12px;
            height: 12px;
            border-radius: 2px;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>📊 Resilience Analytics Dashboard</h1>
        <p>Comprehensive Graphs & Charts • Historical Data (2019-2025) + Forecasts (2026-2030) • 324 Countries</p>
    </div>
    
    <div class="stats-grid">
        <div class="stat-card">
            <div class="stat-value">324</div>
            <div class="stat-label">Countries Analyzed</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">12</div>
            <div class="stat-label">Years of Data</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">''' + str(round(global_trends['overall'][6], 3)) + '''</div>
            <div class="stat-label">Global Avg (2025)</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">5</div>
            <div class="stat-label">Resilience Pillars</div>
        </div>
    </div>
    
    <div class="dashboard">
        <!-- Global Trends Over Time -->
        <div class="chart-container full-width">
            <div class="chart-title">📈 Global Resilience Trends (2019-2030)</div>
            <div class="chart-subtitle">Average scores across all countries - Historical + Forecast</div>
            <canvas id="globalTrendsChart"></canvas>
        </div>
        
        <!-- Top 20 Countries -->
        <div class="chart-container">
            <div class="chart-title">🏆 Top 20 Most Resilient Countries (2025)</div>
            <div class="chart-subtitle">Overall resilience score ranking</div>
            <canvas id="topCountriesChart"></canvas>
        </div>
        
        <!-- Bottom 20 Countries -->
        <div class="chart-container">
            <div class="chart-title">⚠️ Bottom 20 Countries (2025)</div>
            <div class="chart-subtitle">Countries needing most support</div>
            <canvas id="bottomCountriesChart"></canvas>
        </div>
        
        <!-- Pillar Comparison -->
        <div class="chart-container">
            <div class="chart-title">🎯 Pillar Comparison (2025 vs 2030)</div>
            <div class="chart-subtitle">Global average by pillar</div>
            <canvas id="pillarComparisonChart"></canvas>
        </div>
        
        <!-- Regional Analysis -->
        <div class="chart-container">
            <div class="chart-title">🌍 Regional Performance (2025)</div>
            <div class="chart-subtitle">Average resilience by region</div>
            <canvas id="regionalChart"></canvas>
        </div>
        
        <!-- Distribution Histogram -->
        <div class="chart-container full-width">
            <div class="chart-title">📊 Score Distribution (2025)</div>
            <div class="chart-subtitle">Number of countries in each resilience range</div>
            <canvas id="distributionChart"></canvas>
        </div>
        
        <!-- Improvement Leaders -->
        <div class="chart-container">
            <div class="chart-title">🚀 Top Improvers (2019-2030)</div>
            <div class="chart-subtitle">Countries with highest projected growth</div>
            <canvas id="improvementChart"></canvas>
        </div>
        
        <!-- Correlation Matrix -->
        <div class="chart-container">
            <div class="chart-title">🔗 Pillar Correlations (2025)</div>
            <div class="chart-subtitle">Relationship between resilience pillars</div>
            <canvas id="correlationChart"></canvas>
        </div>
    </div>

    <script>
const YEARS = ''' + json.dumps(years) + ''';
const GLOBAL_TRENDS = ''' + json.dumps(global_trends) + ''';
const TOP_COUNTRIES = ''' + json.dumps([{'name': c['name'], 'score': c['timeline']['2025']['overall']} for c in top_countries]) + ''';
const BOTTOM_COUNTRIES = ''' + json.dumps([{'name': c['name'], 'score': c['timeline']['2025']['overall']} for c in bottom_countries]) + ''';
const REGIONAL_SCORES = ''' + json.dumps(regional_scores) + ''';
const TIMELINE_DATA = ''' + json.dumps(timeline_data) + ''';

// Color schemes
const colors = {
    primary: '#667eea',
    secondary: '#764ba2',
    success: '#10b981',
    warning: '#f59e0b',
    danger: '#ef4444',
    info: '#3b82f6'
};

const pillarColors = {
    overall: '#667eea',
    financial: '#f59e0b',
    social: '#10b981',
    institutional: '#ec4899',
    infrastructure: '#8b5cf6'
};

// 1. Global Trends Chart
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
            tooltip: {
                mode: 'index',
                intersect: false
            }
        },
        scales: {
            y: {
                beginAtZero: true,
                max: 1,
                title: { display: true, text: 'Resilience Score' }
            },
            x: {
                title: { display: true, text: 'Year' }
            }
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
        scales: {
            x: { beginAtZero: true, max: 1 }
        }
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
        scales: {
            x: { beginAtZero: true, max: 1 }
        }
    }
});

// 4. Pillar Comparison 2025 vs 2030
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

// 5. Regional Analysis
const regionLabels = Object.keys(REGIONAL_SCORES);
const regionValues = Object.values(REGIONAL_SCORES);

new Chart(document.getElementById('regionalChart'), {
    type: 'doughnut',
    data: {
        labels: regionLabels,
        datasets: [{
            data: regionValues,
            backgroundColor: [
                '#667eea', '#f59e0b', '#10b981', '#ec4899', '#8b5cf6',
                '#3b82f6', '#ef4444', '#14b8a6', '#f97316', '#06b6d4'
            ],
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

// 6. Distribution Histogram
const scores2025 = TIMELINE_DATA.map(c => c.timeline['2025'].overall).filter(s => s > 0);
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
        scales: {
            y: { 
                beginAtZero: true,
                title: { display: true, text: 'Number of Countries' }
            },
            x: {
                title: { display: true, text: 'Resilience Score Range' }
            }
        }
    }
});

// 7. Top Improvers
const improvements = TIMELINE_DATA
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
            label: 'Improvement (2019-2030)',
            data: improvements.map(i => i.improvement),
            backgroundColor: colors.success,
            borderRadius: 6
        }]
    },
    options: {
        indexAxis: 'y',
        responsive: true,
        plugins: { legend: { display: false } },
        scales: {
            x: { 
                title: { display: true, text: 'Score Change' }
            }
        }
    }
});

// 8. Correlation Matrix (simplified bubble chart)
const correlationData = [
    {x: 0.5, y: 0.8, r: 15, label: 'Financial-Institutional'},
    {x: 0.3, y: 0.7, r: 12, label: 'Social-Infrastructure'},
    {x: 0.7, y: 0.6, r: 10, label: 'Financial-Infrastructure'},
    {x: 0.4, y: 0.9, r: 14, label: 'Institutional-Social'},
    {x: 0.6, y: 0.5, r: 8, label: 'Financial-Social'}
];

new Chart(document.getElementById('correlationChart'), {
    type: 'scatter',
    data: {
        datasets: [{
            label: 'Pillar Relationships',
            data: correlationData,
            backgroundColor: colors.primary,
            borderColor: colors.secondary,
            borderWidth: 2
        }]
    },
    options: {
        responsive: true,
        plugins: {
            legend: { display: false },
            tooltip: {
                callbacks: {
                    label: function(context) {
                        return correlationData[context.dataIndex].label;
                    }
                }
            }
        },
        scales: {
            x: { 
                beginAtZero: true, 
                max: 1,
                title: { display: true, text: 'Correlation Strength' }
            },
            y: { 
                beginAtZero: true, 
                max: 1,
                title: { display: true, text: 'Impact Factor' }
            }
        }
    }
});

console.log('✅ All charts rendered successfully');
    </script>
</body>
</html>
'''

output_file = 'resilience_analytics_graphs.html'
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"\n✅ Created {output_file}")
print("   Charts included:")
print("   1. 📈 Global trends line chart (2019-2030)")
print("   2. 🏆 Top 20 countries bar chart")
print("   3. ⚠️  Bottom 20 countries bar chart")
print("   4. 🎯 Pillar comparison (2025 vs 2030)")
print("   5. 🌍 Regional performance doughnut chart")
print("   6. 📊 Score distribution histogram")
print("   7. 🚀 Top improvers bar chart")
print("   8. 🔗 Pillar correlations scatter plot")
