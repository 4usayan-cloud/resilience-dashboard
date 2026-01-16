import json

print("Loading data...")

# Load resilience data (try live data first, fall back to cleaned)
try:
    with open('resilience_data_live.json', 'r') as f:
        resilience_data = json.load(f)
    print("✓ Using LIVE data from World Bank APIs")
except:
    with open('resilience_data_cleaned.json', 'r') as f:
        resilience_data = json.load(f)
    print("✓ Using static data")

# Load world GeoJSON
with open('world.geojson', 'r') as f:
    world_geojson = json.load(f)

# Create lookup dictionary
resilience_lookup = {country['iso3']: country for country in resilience_data}

print(f"✓ {len(resilience_lookup)} countries in resilience data")
print(f"✓ {len(world_geojson['features'])} features in GeoJSON")

# Create HTML with choropleth map
html_template = '''<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Global Resilience Choropleth Map</title>
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; }
        
        #map { position: absolute; top: 0; bottom: 0; width: 100%; }
        
        .controls {
            position: absolute;
            top: 20px;
            right: 20px;
            z-index: 1000;
            background: white;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.2);
            max-width: 300px;
        }
        
        .controls h2 {
            font-size: 18px;
            margin-bottom: 15px;
            color: #1a1a1a;
        }
        
        .toggle-buttons {
            display: flex;
            flex-direction: column;
            gap: 8px;
        }
        
        .toggle-buttons button {
            padding: 12px;
            border: 2px solid #e5e7eb;
            background: white;
            border-radius: 8px;
            cursor: pointer;
            font-size: 14px;
            font-weight: 600;
            transition: all 0.2s;
        }
        
        .toggle-buttons button:hover {
            background: #f3f4f6;
            border-color: #0ea5a4;
        }
        
        .toggle-buttons button.active {
            background: #0ea5a4;
            color: white;
            border-color: #0ea5a4;
        }
        
        .legend {
            position: absolute;
            bottom: 30px;
            left: 20px;
            z-index: 1000;
            background: white;
            padding: 15px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.15);
        }
        
        .legend h4 {
            margin: 0 0 10px 0;
            font-size: 14px;
        }
        
        .legend-item {
            display: flex;
            align-items: center;
            margin: 5px 0;
            font-size: 12px;
        }
        
        .legend-color {
            width: 30px;
            height: 20px;
            margin-right: 8px;
            border: 1px solid #ddd;
            border-radius: 3px;
        }
        
        .country-info {
            position: absolute;
            top: 20px;
            left: 20px;
            z-index: 1000;
            background: white;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.2);
            max-width: 400px;
            max-height: 70vh;
            overflow-y: auto;
            display: none;
        }
        
        .country-info.show {
            display: block;
        }
        
        .country-info h3 {
            margin: 0 0 15px 0;
            color: #0ea5a4;
            font-size: 20px;
        }
        
        .country-info .close-btn {
            position: absolute;
            top: 15px;
            right: 15px;
            background: none;
            border: none;
            font-size: 24px;
            cursor: pointer;
            color: #666;
        }
        
        .score-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px;
            margin: 15px 0;
        }
        
        .score-card {
            background: #f8f9fa;
            padding: 12px;
            border-radius: 8px;
            text-align: center;
        }
        
        .score-card .label {
            font-size: 11px;
            color: #666;
            text-transform: uppercase;
            margin-bottom: 5px;
        }
        
        .score-card .value {
            font-size: 24px;
            font-weight: bold;
            color: #0ea5a4;
        }
        
        #countryChart {
            margin-top: 20px;
            max-height: 200px;
        }
    </style>
</head>
<body>
    <div id="map"></div>
    
    <div class="controls">
        <h2>📊 View</h2>
        <div class="toggle-buttons">
            <button onclick="setView('overall')" class="active" id="btn-overall">Overall Score</button>
            <button onclick="setView('financial')" id="btn-financial">💰 Financial</button>
            <button onclick="setView('social')" id="btn-social">👥 Social</button>
            <button onclick="setView('institutional')" id="btn-institutional">🏛️ Institutional</button>
            <button onclick="setView('infrastructure')" id="btn-infrastructure">🏗️ Infrastructure</button>
        </div>
    </div>
    
    <div class="legend">
        <h4>Resilience Score</h4>
        <div class="legend-item">
            <div class="legend-color" style="background: #d32f2f;"></div>
            <span>Low (&lt; 0.45) - Bottom 20%</span>
        </div>
        <div class="legend-item">
            <div class="legend-color" style="background: #ff9800;"></div>
            <span>Below Average (0.45 - 0.53)</span>
        </div>
        <div class="legend-item">
            <div class="legend-color" style="background: #ffeb3b;"></div>
            <span>Average (0.53 - 0.60)</span>
        </div>
        <div class="legend-item">
            <div class="legend-color" style="background: #9ccc65;"></div>
            <span>Above Average (0.60 - 0.66)</span>
        </div>
        <div class="legend-item">
            <div class="legend-color" style="background: #2e7d32;"></div>
            <span>High (&gt; 0.66) - Top 20%</span>
        </div>
        <div class="legend-item">
            <div class="legend-color" style="background: #e0e0e0;"></div>
            <span>No Data</span>
        </div>
    </div>
    
    <div class="country-info" id="countryInfo">
        <button class="close-btn" onclick="closeInfo()">×</button>
        <h3 id="countryName"></h3>
        <div class="score-grid">
            <div class="score-card">
                <div class="label">Overall</div>
                <div class="value" id="scoreOverall">-</div>
            </div>
            <div class="score-card">
                <div class="label">Financial</div>
                <div class="value" id="scoreFinancial">-</div>
            </div>
            <div class="score-card">
                <div class="label">Social</div>
                <div class="value" id="scoreSocial">-</div>
            </div>
            <div class="score-card">
                <div class="label">Institutional</div>
                <div class="value" id="scoreInstitutional">-</div>
            </div>
            <div class="score-card">
                <div class="label">Infrastructure</div>
                <div class="value" id="scoreInfrastructure">-</div>
            </div>
        </div>
        <canvas id="countryChart"></canvas>
    </div>

    <script>
// Embedded data
const RESILIENCE_DATA = ''' + json.dumps(resilience_lookup) + ''';
const WORLD_GEOJSON = ''' + json.dumps(world_geojson) + ''';

let map;
let geoJsonLayer;
let currentView = 'overall';
let currentChart = null;

// Initialize map
map = L.map('map', {
    center: [20, 0],
    zoom: 2.5,
    minZoom: 2,
    maxBounds: [[-90, -180], [90, 180]]
});

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors',
    noWrap: true
}).addTo(map);

// Color scale function
function getColor(score) {
    if (!score || score === 0) return '#e0e0e0';
    // Percentile-based thresholds for better distribution
    if (score < 0.45) return '#d32f2f';      // Bottom 20% - Red
    if (score < 0.53) return '#ff9800';      // 20-40% - Orange
    if (score < 0.60) return '#ffeb3b';      // 40-60% - Yellow
    if (score < 0.66) return '#9ccc65';      // 60-80% - Light Green
    return '#2e7d32';                         // Top 20% - Dark Green
}

// Style function for GeoJSON
function style(feature) {
    const iso3 = feature.properties['ISO3166-1-Alpha-3'];
    const countryData = RESILIENCE_DATA[iso3];
    const score = countryData ? countryData[currentView === 'overall' ? 'score' : currentView] : 0;
    
    return {
        fillColor: getColor(score),
        weight: 1,
        opacity: 1,
        color: 'white',
        fillOpacity: 0.8
    };
}

// Highlight feature on hover
function highlightFeature(e) {
    const layer = e.target;
    layer.setStyle({
        weight: 3,
        color: '#0ea5a4',
        fillOpacity: 1
    });
    layer.bringToFront();
}

// Reset highlight
function resetHighlight(e) {
    geoJsonLayer.resetStyle(e.target);
}

// Show country info on click
function showCountryInfo(e) {
    const feature = e.target.feature;
    const iso3 = feature.properties['ISO3166-1-Alpha-3'];
    const countryData = RESILIENCE_DATA[iso3];
    
    if (!countryData) {
        return;
    }
    
    document.getElementById('countryName').textContent = feature.properties.name;
    document.getElementById('scoreOverall').textContent = (countryData.score || 0).toFixed(3);
    document.getElementById('scoreFinancial').textContent = (countryData.financial || 0).toFixed(3);
    document.getElementById('scoreSocial').textContent = (countryData.social || 0).toFixed(3);
    document.getElementById('scoreInstitutional').textContent = (countryData.institutional || 0).toFixed(3);
    document.getElementById('scoreInfrastructure').textContent = (countryData.infrastructure || 0).toFixed(3);
    
    document.getElementById('countryInfo').classList.add('show');
    
    // Update chart
    updateChart(countryData);
}

// Update chart
function updateChart(countryData) {
    const ctx = document.getElementById('countryChart');
    
    if (currentChart) {
        currentChart.destroy();
    }
    
    currentChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Overall', 'Financial', 'Social', 'Institutional', 'Infrastructure'],
            datasets: [{
                label: 'Resilience Score',
                data: [
                    countryData.score || 0,
                    countryData.financial || 0,
                    countryData.social || 0,
                    countryData.institutional || 0,
                    countryData.infrastructure || 0
                ],
                backgroundColor: ['#0ea5a4', '#3b82f6', '#8b5cf6', '#ec4899', '#f59e0b'],
                borderRadius: 6
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            scales: {
                y: {
                    beginAtZero: true,
                    max: 1,
                    ticks: {
                        font: { size: 10 }
                    }
                },
                x: {
                    ticks: {
                        font: { size: 10 }
                    }
                }
            },
            plugins: {
                legend: {
                    display: false
                }
            }
        }
    });
}

// Close info panel
function closeInfo() {
    document.getElementById('countryInfo').classList.remove('show');
}

// On each feature
function onEachFeature(feature, layer) {
    layer.on({
        mouseover: highlightFeature,
        mouseout: resetHighlight,
        click: showCountryInfo
    });
}

// Load GeoJSON layer
function loadGeoJSON() {
    if (geoJsonLayer) {
        map.removeLayer(geoJsonLayer);
    }
    
    geoJsonLayer = L.geoJSON(WORLD_GEOJSON, {
        style: style,
        onEachFeature: onEachFeature
    }).addTo(map);
}

// Set view
function setView(view) {
    currentView = view;
    
    // Update button states
    document.querySelectorAll('.toggle-buttons button').forEach(btn => {
        btn.classList.remove('active');
    });
    document.getElementById('btn-' + view).classList.add('active');
    
    // Reload GeoJSON with new colors
    loadGeoJSON();
}

// Initialize
loadGeoJSON();
console.log('Map loaded with', Object.keys(RESILIENCE_DATA).length, 'countries');
    </script>
</body>
</html>
'''

# Write the HTML file
with open('resilience_choropleth_map.html', 'w', encoding='utf-8') as f:
    f.write(html_template)

print("\n✅ Created resilience_choropleth_map.html")
print("   - Full country shapes colored by resilience")
print("   - 5-color gradient system")
print("   - Interactive charts for each country")
print("   - Toggle between Overall and 4 pillars")
