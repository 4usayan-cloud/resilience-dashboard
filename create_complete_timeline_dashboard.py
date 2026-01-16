import json

print("Creating comprehensive multi-pillar timeline dashboard...")

# Load timeline data
with open('resilience_timeline_2019_2030.json', 'r') as f:
    timeline_data = json.load(f)

# Load GeoJSON
with open('world.geojson', 'r') as f:
    world_geojson = json.load(f)

timeline_lookup = {c['iso3']: c for c in timeline_data}

print(f"✓ Loaded timeline data for {len(timeline_lookup)} countries")

# Create comprehensive HTML dashboard
html = '''<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Resilience Timeline: Historical + Forecast (2019-2030)</title>
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; overflow: hidden; background: #f8f9fa; }
        
        #map { position: absolute; top: 0; bottom: 0; width: 100%; }
        
        .header {
            position: absolute; top: 0; left: 0; right: 0; height: 90px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white; padding: 20px 30px; z-index: 1001;
            box-shadow: 0 4px 30px rgba(0,0,0,0.3);
            display: flex; justify-content: space-between; align-items: center;
        }
        
        .header h1 { font-size: 28px; font-weight: 700; margin-bottom: 5px; }
        .header-subtitle { font-size: 13px; opacity: 0.95; }
        
        .pillar-tabs {
            display: flex; gap: 10px;
        }
        
        .pillar-tab {
            padding: 8px 16px; border-radius: 8px; background: rgba(255,255,255,0.2);
            cursor: pointer; font-size: 13px; font-weight: 600;
            transition: all 0.3s; border: 2px solid transparent;
        }
        
        .pillar-tab:hover { background: rgba(255,255,255,0.3); }
        .pillar-tab.active { background: white; color: #667eea; border-color: white; }
        
        .timeline-container {
            position: absolute; top: 110px; left: 50%; transform: translateX(-50%);
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
        
        .slider-container { position: relative; padding: 10px 0; }
        
        .slider {
            width: 100%; height: 8px; border-radius: 4px;
            background: linear-gradient(90deg, #4338ca 0%, #92400e 58%, #065f46 100%);
            outline: none; opacity: 0.8; transition: opacity 0.2s;
        }
        
        .slider:hover { opacity: 1; }
        
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
        
        .control-btn:hover { transform: translateY(-2px); box-shadow: 0 4px 15px rgba(102,126,234,0.4); }
        
        .legend {
            position: absolute; bottom: 30px; left: 20px; z-index: 1000;
            background: white; padding: 18px; border-radius: 12px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.15);
        }
        
        .legend h4 { margin: 0 0 12px 0; font-size: 14px; font-weight: 600; color: #1a1a1a; }
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
        
        .country-detail {
            position: absolute; top: 250px; right: 20px; z-index: 1000;
            background: white; padding: 25px; border-radius: 15px;
            box-shadow: 0 4px 30px rgba(0,0,0,0.2); width: 450px;
            max-height: calc(100vh - 270px); overflow-y: auto; display: none;
        }
        
        .country-detail.show { display: block; }
        
        .country-detail h3 {
            margin: 0 0 20px 0; color: #667eea; font-size: 22px;
            padding-bottom: 12px; border-bottom: 2px solid #e5e7eb;
        }
        
        .close-btn {
            position: absolute; top: 20px; right: 20px; background: none;
            border: none; font-size: 28px; cursor: pointer; color: #999;
        }
        
        .close-btn:hover { color: #667eea; }
        
        .metric-grid {
            display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px; margin: 20px 0;
        }
        
        .metric-card {
            background: linear-gradient(135deg, #f9fafb 0%, #ffffff 100%);
            padding: 15px; border-radius: 10px; border: 2px solid #e5e7eb; text-align: center;
        }
        
        .metric-card .label {
            font-size: 11px; color: #666; text-transform: uppercase;
            margin-bottom: 8px; font-weight: 600;
        }
        
        .metric-card .value {
            font-size: 26px; font-weight: 700;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        }
        
        .metric-card.highlight {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-color: #667eea;
        }
        
        .metric-card.highlight .label { color: rgba(255,255,255,0.9); }
        .metric-card.highlight .value { color: white; -webkit-text-fill-color: white; }
        
        .trend-badge {
            display: inline-block; padding: 4px 10px; border-radius: 15px;
            font-size: 11px; font-weight: 600; margin: 5px 0;
        }
        
        .trend-up { background: #d1fae5; color: #065f46; }
        .trend-down { background: #fee2e2; color: #991b1b; }
        .trend-stable { background: #e0e7ff; color: #3730a3; }
        
        #timelineChart { margin-top: 20px; max-height: 220px; }
    </style>
</head>
<body>
    <div class="header">
        <div>
            <h1>🌍 Global Resilience Timeline Dashboard</h1>
            <div class="header-subtitle">Historical Data (2019-2025) + BSTS+DFM Forecasts (2026-2030) • 324 Countries</div>
        </div>
        <div class="pillar-tabs">
            <div class="pillar-tab active" onclick="setPillar('overall')" id="tab-overall">Overall</div>
            <div class="pillar-tab" onclick="setPillar('financial')" id="tab-financial">💰 Financial</div>
            <div class="pillar-tab" onclick="setPillar('social')" id="tab-social">👥 Social</div>
            <div class="pillar-tab" onclick="setPillar('institutional')" id="tab-institutional">🏛️ Institutional</div>
            <div class="pillar-tab" onclick="setPillar('infrastructure')" id="tab-infrastructure">🏗️ Infrastructure</div>
        </div>
    </div>
    
    <div id="map"></div>
    
    <div class="timeline-container">
        <div class="timeline-header">
            <div class="year-display" id="yearDisplay">2025</div>
            <div class="period-badge period-current" id="periodBadge">Current</div>
        </div>
        <div class="slider-container">
            <input type="range" min="0" max="11" value="6" class="slider" id="yearSlider">
            <div class="year-labels">
                <span>2019</span><span>2021</span><span>2023</span><span style="font-weight:700;color:#92400e">2025</span>
                <span>2027</span><span>2029</span>
            </div>
        </div>
        <div class="controls">
            <button class="control-btn" onclick="playAnimation()">▶ Play Timeline</button>
            <button class="control-btn" onclick="resetYear()">⟲ Reset to 2025</button>
            <button class="control-btn" onclick="compareHistorical()">📊 Show Trends</button>
        </div>
    </div>
    
    <div class="legend">
        <h4 id="legendTitle">Overall Resilience</h4>
        <div class="legend-item"><div class="legend-color" style="background: #d32f2f;"></div><span>Low (&lt; 0.45)</span></div>
        <div class="legend-item"><div class="legend-color" style="background: #ff9800;"></div><span>Below Avg (0.45-0.53)</span></div>
        <div class="legend-item"><div class="legend-color" style="background: #ffeb3b;"></div><span>Average (0.53-0.60)</span></div>
        <div class="legend-item"><div class="legend-color" style="background: #9ccc65;"></div><span>Above Avg (0.60-0.66)</span></div>
        <div class="legend-item"><div class="legend-color" style="background: #2e7d32;"></div><span>High (&gt; 0.66)</span></div>
    </div>
    
    <div class="stats-panel">
        <h4>📊 Global Statistics</h4>
        <div class="stat-row">
            <span class="stat-label">Year:</span>
            <span class="stat-value" id="statYear">2025</span>
        </div>
        <div class="stat-row">
            <span class="stat-label">Countries:</span>
            <span class="stat-value" id="statCount">0</span>
        </div>
        <div class="stat-row">
            <span class="stat-label">Global Average:</span>
            <span class="stat-value" id="statAvg">0.000</span>
        </div>
        <div class="stat-row">
            <span class="stat-label">Change from 2019:</span>
            <span class="stat-value" id="statChange">-</span>
        </div>
        <div class="stat-row">
            <span class="stat-label">Highest:</span>
            <span class="stat-value" id="statMax">-</span>
        </div>
    </div>
    
    <div class="country-detail" id="countryDetail">
        <button class="close-btn" onclick="closeDetail()">×</button>
        <h3 id="countryName"></h3>
        
        <div class="metric-grid">
            <div class="metric-card highlight">
                <div class="label" id="currentMetricLabel">Overall</div>
                <div class="value" id="currentMetricValue">-</div>
            </div>
            <div class="metric-card">
                <div class="label">Financial</div>
                <div class="value" id="metricFinancial">-</div>
            </div>
            <div class="metric-card">
                <div class="label">Social</div>
                <div class="value" id="metricSocial">-</div>
            </div>
            <div class="metric-card">
                <div class="label">Institutional</div>
                <div class="value" id="metricInstitutional">-</div>
            </div>
            <div class="metric-card">
                <div class="label">Infrastructure</div>
                <div class="value" id="metricInfrastructure">-</div>
            </div>
        </div>
        
        <div id="trendBadge"></div>
        
        <canvas id="timelineChart"></canvas>
    </div>

    <script>
const TIMELINE_DATA = ''' + json.dumps(timeline_lookup) + ''';
const WORLD_GEOJSON = ''' + json.dumps(world_geojson) + ''';
const YEARS = [2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026, 2027, 2028, 2029, 2030];

let map, geoJsonLayer, currentYear = 2025, currentPillar = 'overall';
let animationInterval = null, currentChart = null, currentCountry = null;

map = L.map('map', {
    center: [20, 0], zoom: 2.5, minZoom: 2,
    maxBounds: [[-90, -180], [90, 180]]
}).setView([20, 0], 2.5);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap', noWrap: true
}).addTo(map);

function getColor(score) {
    if (!score || score === 0) return '#e0e0e0';
    if (score < 0.45) return '#d32f2f';
    if (score < 0.53) return '#ff9800';
    if (score < 0.60) return '#ffeb3b';
    if (score < 0.66) return '#9ccc65';
    return '#2e7d32';
}

function style(feature) {
    const iso3 = feature.properties['ISO3166-1-Alpha-3'];
    const countryData = TIMELINE_DATA[iso3];
    const yearData = countryData?.timeline?.[currentYear.toString()];
    const score = yearData?.[currentPillar] || 0;
    
    return {
        fillColor: getColor(score),
        weight: 1, opacity: 1, color: 'white', fillOpacity: 0.8
    };
}

function highlightFeature(e) {
    e.target.setStyle({ weight: 3, color: '#667eea', fillOpacity: 1 });
    e.target.bringToFront();
}

function resetHighlight(e) {
    geoJsonLayer.resetStyle(e.target);
}

function showCountryInfo(e) {
    const feature = e.target.feature;
    const iso3 = feature.properties['ISO3166-1-Alpha-3'];
    const countryData = TIMELINE_DATA[iso3];
    
    if (!countryData) return;
    
    currentCountry = countryData;
    const yearData = countryData.timeline[currentYear.toString()];
    
    document.getElementById('countryName').textContent = feature.properties.name;
    document.getElementById('currentMetricLabel').textContent = currentPillar.charAt(0).toUpperCase() + currentPillar.slice(1);
    document.getElementById('currentMetricValue').textContent = (yearData[currentPillar] || 0).toFixed(3);
    document.getElementById('metricFinancial').textContent = (yearData.financial || 0).toFixed(3);
    document.getElementById('metricSocial').textContent = (yearData.social || 0).toFixed(3);
    document.getElementById('metricInstitutional').textContent = (yearData.institutional || 0).toFixed(3);
    document.getElementById('metricInfrastructure').textContent = (yearData.infrastructure || 0).toFixed(3);
    
    // Calculate trend
    const year2019 = countryData.timeline['2019'][currentPillar];
    const currentVal = yearData[currentPillar];
    const change = currentVal - year2019;
    const pctChange = year2019 > 0 ? ((change / year2019) * 100) : 0;
    
    let trendHTML = '';
    if (Math.abs(pctChange) < 3) {
        trendHTML = '<span class="trend-badge trend-stable">→ Stable (since 2019)</span>';
    } else if (change > 0) {
        trendHTML = `<span class="trend-badge trend-up">↗ Improving +${pctChange.toFixed(1)}% since 2019</span>`;
    } else {
        trendHTML = `<span class="trend-badge trend-down">↘ Declining ${pctChange.toFixed(1)}% since 2019</span>`;
    }
    document.getElementById('trendBadge').innerHTML = trendHTML;
    
    document.getElementById('countryDetail').classList.add('show');
    updateChart(countryData);
}

function updateChart(countryData) {
    const ctx = document.getElementById('timelineChart');
    if (currentChart) currentChart.destroy();
    
    const values = YEARS.map(y => countryData.timeline[y.toString()][currentPillar] || 0);
    
    currentChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: YEARS,
            datasets: [{
                label: currentPillar.charAt(0).toUpperCase() + currentPillar.slice(1),
                data: values,
                borderColor: '#667eea',
                backgroundColor: 'rgba(102, 126, 234, 0.1)',
                borderWidth: 3,
                fill: true,
                tension: 0.4,
                pointRadius: 4,
                pointBackgroundColor: '#667eea'
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { display: false },
                title: { 
                    display: true, 
                    text: `${countryData.name} - ${currentPillar.charAt(0).toUpperCase() + currentPillar.slice(1)} (2019-2030)`,
                    font: { size: 13, weight: '600' }
                }
            },
            scales: {
                y: { beginAtZero: true, max: 1, ticks: { font: { size: 10 } } },
                x: { ticks: { font: { size: 9 } } }
            },
            interaction: {
                intersect: false,
                mode: 'index'
            }
        }
    });
}

function closeDetail() {
    document.getElementById('countryDetail').classList.remove('show');
}

function onEachFeature(feature, layer) {
    layer.on({
        mouseover: highlightFeature,
        mouseout: resetHighlight,
        click: showCountryInfo
    });
}

function loadGeoJSON() {
    if (geoJsonLayer) map.removeLayer(geoJsonLayer);
    
    geoJsonLayer = L.geoJSON(WORLD_GEOJSON, {
        style: style,
        onEachFeature: onEachFeature
    }).addTo(map);
    
    updateStats();
}

function updateStats() {
    const allCountries = Object.values(TIMELINE_DATA);
    const scores = allCountries
        .map(c => c.timeline[currentYear.toString()]?.[currentPillar])
        .filter(s => s > 0);
    
    document.getElementById('statYear').textContent = currentYear;
    document.getElementById('statCount').textContent = scores.length;
    document.getElementById('statAvg').textContent = (scores.reduce((a,b) => a+b, 0) / scores.length).toFixed(3);
    
    const scores2019 = allCountries
        .map(c => c.timeline['2019']?.[currentPillar])
        .filter(s => s > 0);
    const avg2019 = scores2019.reduce((a,b) => a+b, 0) / scores2019.length;
    const avgCurrent = scores.reduce((a,b) => a+b, 0) / scores.length;
    const change = avgCurrent - avg2019;
    document.getElementById('statChange').textContent = (change >= 0 ? '+' : '') + change.toFixed(3);
    
    const maxCountry = allCountries.reduce((max, c) => {
        const score = c.timeline[currentYear.toString()]?.[currentPillar] || 0;
        return score > max.score ? {name: c.name, score} : max;
    }, {name: '', score: 0});
    document.getElementById('statMax').textContent = `${maxCountry.name} (${maxCountry.score.toFixed(3)})`;
}

document.getElementById('yearSlider').addEventListener('input', function(e) {
    currentYear = YEARS[parseInt(e.target.value)];
    updateYearDisplay();
    loadGeoJSON();
});

function updateYearDisplay() {
    document.getElementById('yearDisplay').textContent = currentYear;
    
    const badge = document.getElementById('periodBadge');
    if (currentYear < 2025) {
        badge.textContent = 'Historical';
        badge.className = 'period-badge period-historical';
    } else if (currentYear === 2025) {
        badge.textContent = 'Current';
        badge.className = 'period-badge period-current';
    } else {
        badge.textContent = 'Forecast';
        badge.className = 'period-badge period-forecast';
    }
}

function setPillar(pillar) {
    currentPillar = pillar;
    
    document.querySelectorAll('.pillar-tab').forEach(tab => tab.classList.remove('active'));
    document.getElementById('tab-' + pillar).classList.add('active');
    
    const title = pillar.charAt(0).toUpperCase() + pillar.slice(1) + ' Resilience';
    document.getElementById('legendTitle').textContent = title;
    
    loadGeoJSON();
    
    if (currentCountry) {
        const yearData = currentCountry.timeline[currentYear.toString()];
        document.getElementById('currentMetricLabel').textContent = pillar.charAt(0).toUpperCase() + pillar.slice(1);
        document.getElementById('currentMetricValue').textContent = (yearData[pillar] || 0).toFixed(3);
        updateChart(currentCountry);
    }
}

function playAnimation() {
    if (animationInterval) {
        clearInterval(animationInterval);
        animationInterval = null;
        return;
    }
    
    let index = parseInt(document.getElementById('yearSlider').value);
    animationInterval = setInterval(() => {
        if (index >= YEARS.length) {
            clearInterval(animationInterval);
            animationInterval = null;
            return;
        }
        
        document.getElementById('yearSlider').value = index;
        currentYear = YEARS[index];
        updateYearDisplay();
        loadGeoJSON();
        index++;
    }, 1200);
}

function resetYear() {
    currentYear = 2025;
    document.getElementById('yearSlider').value = 6;
    updateYearDisplay();
    loadGeoJSON();
}

function compareHistorical() {
    alert('Historical comparison feature: Compare any country\\'s performance from 2019-2030 by clicking on it!');
}

loadGeoJSON();
console.log('✅ Timeline dashboard loaded - 2019-2030');
    </script>
</body>
</html>
'''

output_file = 'resilience_complete_timeline.html'
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"\n✅ Created {output_file}")
print("   Features:")
print("   - 📅 Historical data (2019-2025) + Forecasts (2026-2030)")
print("   - 🎯 5 pillars: Overall, Financial, Social, Institutional, Infrastructure")
print("   - 🎬 Timeline animation across 12 years")
print("   - 📊 Country-specific trends and charts")
print("   - 📈 Global statistics and comparisons")
print("   - 🔄 Real-time pillar switching")
print("   - 📱 Interactive maps for each metric")
