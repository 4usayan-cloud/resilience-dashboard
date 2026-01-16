import json

print("Creating enhanced user-friendly map...")

# Load complete data
with open('resilience_data_complete.json', 'r') as f:
    resilience_data = json.load(f)

# Load world GeoJSON
with open('world.geojson', 'r') as f:
    world_geojson = json.load(f)

# Create lookup dictionary
resilience_lookup = {country['iso3']: country for country in resilience_data}

print(f"✓ {len(resilience_lookup)} countries in complete dataset")
print(f"✓ {len(world_geojson['features'])} features in GeoJSON")

# Create enhanced HTML
html_template = '''<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Global Resilience Atlas - Interactive Dashboard</title>
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
            overflow: hidden;
        }
        
        #map { position: absolute; top: 0; bottom: 0; width: 100%; }
        
        /* Header */
        .header {
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 70px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px 30px;
            z-index: 1001;
            box-shadow: 0 2px 20px rgba(0,0,0,0.3);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .header h1 {
            font-size: 24px;
            font-weight: 700;
        }
        
        .header-subtitle {
            font-size: 12px;
            opacity: 0.9;
            margin-top: 3px;
        }
        
        /* Search Box */
        .search-container {
            position: absolute;
            top: 90px;
            left: 20px;
            z-index: 1000;
            background: white;
            padding: 15px;
            border-radius: 12px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.2);
            width: 350px;
        }
        
        .search-box {
            width: 100%;
            padding: 12px 15px;
            border: 2px solid #e5e7eb;
            border-radius: 8px;
            font-size: 14px;
            transition: border-color 0.2s;
        }
        
        .search-box:focus {
            outline: none;
            border-color: #667eea;
        }
        
        .search-results {
            max-height: 300px;
            overflow-y: auto;
            margin-top: 10px;
            display: none;
        }
        
        .search-results.show {
            display: block;
        }
        
        .search-item {
            padding: 10px;
            cursor: pointer;
            border-bottom: 1px solid #f3f4f6;
            transition: background 0.2s;
        }
        
        .search-item:hover {
            background: #f9fafb;
        }
        
        .search-item strong {
            color: #667eea;
        }
        
        /* Controls */
        .controls {
            position: absolute;
            top: 90px;
            right: 20px;
            z-index: 1000;
            background: white;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.2);
            max-width: 300px;
        }
        
        .controls h2 {
            font-size: 16px;
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
            font-size: 13px;
            font-weight: 600;
            transition: all 0.2s;
            text-align: left;
        }
        
        .toggle-buttons button:hover {
            background: #f3f4f6;
            border-color: #667eea;
        }
        
        .toggle-buttons button.active {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-color: #667eea;
        }
        
        /* Legend */
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
            font-weight: 600;
        }
        
        .legend-item {
            display: flex;
            align-items: center;
            margin: 5px 0;
            font-size: 11px;
        }
        
        .legend-color {
            width: 30px;
            height: 18px;
            margin-right: 8px;
            border: 1px solid #ddd;
            border-radius: 3px;
        }
        
        /* Country Info Panel */
        .country-info {
            position: absolute;
            top: 90px;
            left: 390px;
            z-index: 1000;
            background: white;
            padding: 25px;
            border-radius: 12px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.2);
            width: 450px;
            max-height: calc(100vh - 120px);
            overflow-y: auto;
            display: none;
        }
        
        .country-info.show {
            display: block;
        }
        
        .country-info h3 {
            margin: 0 0 20px 0;
            color: #667eea;
            font-size: 22px;
            padding-bottom: 10px;
            border-bottom: 2px solid #e5e7eb;
        }
        
        .close-btn {
            position: absolute;
            top: 20px;
            right: 20px;
            background: none;
            border: none;
            font-size: 28px;
            cursor: pointer;
            color: #999;
            line-height: 1;
        }
        
        .close-btn:hover {
            color: #667eea;
        }
        
        .score-section {
            margin: 20px 0;
        }
        
        .score-section h4 {
            font-size: 14px;
            color: #666;
            margin-bottom: 15px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .score-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 12px;
        }
        
        .score-card {
            background: linear-gradient(135deg, #f9fafb 0%, #ffffff 100%);
            padding: 15px;
            border-radius: 8px;
            border: 1px solid #e5e7eb;
            text-align: center;
        }
        
        .score-card .label {
            font-size: 11px;
            color: #666;
            text-transform: uppercase;
            margin-bottom: 8px;
            font-weight: 600;
        }
        
        .score-card .value {
            font-size: 28px;
            font-weight: bold;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .score-card.large {
            grid-column: span 2;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        
        .score-card.large .label {
            color: rgba(255,255,255,0.9);
        }
        
        .score-card.large .value {
            color: white;
            -webkit-text-fill-color: white;
        }
        
        #countryChart {
            margin-top: 20px;
            max-height: 250px;
        }
        
        .compare-section {
            margin-top: 20px;
            padding-top: 20px;
            border-top: 2px solid #e5e7eb;
        }
        
        .compare-btn {
            width: 100%;
            padding: 12px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 8px;
            font-weight: 600;
            cursor: pointer;
            font-size: 14px;
            transition: transform 0.2s;
        }
        
        .compare-btn:hover {
            transform: translateY(-2px);
        }
        
        /* Stats Panel */
        .stats-panel {
            position: absolute;
            bottom: 30px;
            right: 20px;
            z-index: 1000;
            background: white;
            padding: 15px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.15);
            font-size: 11px;
        }
        
        .stats-panel strong {
            color: #667eea;
        }
    </style>
</head>
<body>
    <div class="header">
        <div>
            <h1>🌍 Global Resilience Atlas</h1>
            <div class="header-subtitle">Interactive Dashboard • World Bank + INFORM Risk Data • 324 Countries</div>
        </div>
    </div>
    
    <div id="map"></div>
    
    <!-- Search Box -->
    <div class="search-container">
        <input type="text" class="search-box" id="searchBox" placeholder="🔍 Search country name or ISO3 code..." autocomplete="off">
        <div class="search-results" id="searchResults"></div>
    </div>
    
    <!-- Controls -->
    <div class="controls">
        <h2>📊 View Mode</h2>
        <div class="toggle-buttons">
            <button onclick="setView('overall')" class="active" id="btn-overall">🌐 Overall Score</button>
            <button onclick="setView('financial')" id="btn-financial">💰 Financial</button>
            <button onclick="setView('social')" id="btn-social">👥 Social</button>
            <button onclick="setView('institutional')" id="btn-institutional">🏛️ Institutional</button>
            <button onclick="setView('infrastructure')" id="btn-infrastructure">🏗️ Infrastructure</button>
        </div>
    </div>
    
    <!-- Legend -->
    <div class="legend">
        <h4>Resilience Score</h4>
        <div class="legend-item">
            <div class="legend-color" style="background: #d32f2f;"></div>
            <span>Low (&lt; 0.45)</span>
        </div>
        <div class="legend-item">
            <div class="legend-color" style="background: #ff9800;"></div>
            <span>Below Avg (0.45 - 0.53)</span>
        </div>
        <div class="legend-item">
            <div class="legend-color" style="background: #ffeb3b;"></div>
            <span>Average (0.53 - 0.60)</span>
        </div>
        <div class="legend-item">
            <div class="legend-color" style="background: #9ccc65;"></div>
            <span>Above Avg (0.60 - 0.66)</span>
        </div>
        <div class="legend-item">
            <div class="legend-color" style="background: #2e7d32;"></div>
            <span>High (&gt; 0.66)</span>
        </div>
    </div>
    
    <!-- Stats Panel -->
    <div class="stats-panel">
        <div>Countries shown: <strong id="statsCount">0</strong></div>
        <div>Avg score: <strong id="statsAvg">0.000</strong></div>
    </div>
    
    <!-- Country Info -->
    <div class="country-info" id="countryInfo">
        <button class="close-btn" onclick="closeInfo()">×</button>
        <h3 id="countryName"></h3>
        
        <div class="score-section">
            <div class="score-grid">
                <div class="score-card large">
                    <div class="label">Overall Resilience</div>
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
        </div>
        
        <div class="score-section">
            <h4>Performance Breakdown</h4>
            <canvas id="countryChart"></canvas>
        </div>
        
        <div class="compare-section" id="compareSection" style="display: none;">
            <button class="compare-btn" onclick="addToCompare()">+ Add to Comparison</button>
        </div>
    </div>

    <script>
// Embedded data
const RESILIENCE_DATA = ''' + json.dumps(resilience_lookup) + ''';
const WORLD_GEOJSON = ''' + json.dumps(world_geojson) + ''';

let map;
let geoJsonLayer;
let currentView = 'overall';
let currentChart = null;
let currentCountry = null;

// Initialize map
map = L.map('map', {
    center: [20, 0],
    zoom: 2.5,
    minZoom: 2,
    maxBounds: [[-90, -180], [90, 180]]
}).setView([20, 0], 2.5);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap',
    noWrap: true
}).addTo(map);

// Color scale
function getColor(score) {
    if (!score || score === 0) return '#e0e0e0';
    if (score < 0.45) return '#d32f2f';
    if (score < 0.53) return '#ff9800';
    if (score < 0.60) return '#ffeb3b';
    if (score < 0.66) return '#9ccc65';
    return '#2e7d32';
}

// Style function
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

function highlightFeature(e) {
    const layer = e.target;
    layer.setStyle({
        weight: 3,
        color: '#667eea',
        fillOpacity: 1
    });
    layer.bringToFront();
}

function resetHighlight(e) {
    geoJsonLayer.resetStyle(e.target);
}

function showCountryInfo(e) {
    const feature = e.target.feature;
    const iso3 = feature.properties['ISO3166-1-Alpha-3'];
    const countryData = RESILIENCE_DATA[iso3];
    
    if (!countryData) return;
    
    currentCountry = countryData;
    
    document.getElementById('countryName').textContent = feature.properties.name;
    document.getElementById('scoreOverall').textContent = (countryData.score || 0).toFixed(3);
    document.getElementById('scoreFinancial').textContent = (countryData.financial || 0).toFixed(3);
    document.getElementById('scoreSocial').textContent = (countryData.social || 0).toFixed(3);
    document.getElementById('scoreInstitutional').textContent = (countryData.institutional || 0).toFixed(3);
    document.getElementById('scoreInfrastructure').textContent = (countryData.infrastructure || 0).toFixed(3);
    
    document.getElementById('countryInfo').classList.add('show');
    
    updateChart(countryData);
}

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
                label: 'Score',
                data: [
                    countryData.score || 0,
                    countryData.financial || 0,
                    countryData.social || 0,
                    countryData.institutional || 0,
                    countryData.infrastructure || 0
                ],
                backgroundColor: ['#667eea', '#f59e0b', '#10b981', '#ec4899', '#8b5cf6'],
                borderRadius: 6,
                barThickness: 30
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            scales: {
                y: {
                    beginAtZero: true,
                    max: 1,
                    ticks: { font: { size: 11 } }
                },
                x: {
                    ticks: { font: { size: 10 } }
                }
            },
            plugins: {
                legend: { display: false }
            }
        }
    });
}

function closeInfo() {
    document.getElementById('countryInfo').classList.remove('show');
    currentCountry = null;
}

function onEachFeature(feature, layer) {
    layer.on({
        mouseover: highlightFeature,
        mouseout: resetHighlight,
        click: showCountryInfo
    });
}

function loadGeoJSON() {
    if (geoJsonLayer) {
        map.removeLayer(geoJsonLayer);
    }
    
    geoJsonLayer = L.geoJSON(WORLD_GEOJSON, {
        style: style,
        onEachFeature: onEachFeature
    }).addTo(map);
    
    // Update stats
    const scores = Object.values(RESILIENCE_DATA).filter(c => c.score > 0);
    document.getElementById('statsCount').textContent = scores.length;
    const avg = scores.reduce((a, b) => a + b.score, 0) / scores.length;
    document.getElementById('statsAvg').textContent = avg.toFixed(3);
}

function setView(view) {
    currentView = view;
    
    document.querySelectorAll('.toggle-buttons button').forEach(btn => {
        btn.classList.remove('active');
    });
    document.getElementById('btn-' + view).classList.add('active');
    
    loadGeoJSON();
}

// Search functionality
const searchBox = document.getElementById('searchBox');
const searchResults = document.getElementById('searchResults');

searchBox.addEventListener('input', function(e) {
    const query = e.target.value.toLowerCase();
    
    if (query.length < 2) {
        searchResults.classList.remove('show');
        return;
    }
    
    const matches = Object.values(RESILIENCE_DATA)
        .filter(c => 
            c.name.toLowerCase().includes(query) || 
            c.iso3.toLowerCase().includes(query)
        )
        .slice(0, 10);
    
    if (matches.length > 0) {
        searchResults.innerHTML = matches.map(c => 
            `<div class="search-item" onclick="zoomToCountry('${c.iso3}')">
                <strong>${c.name}</strong> (${c.iso3})
                <br>
                <small>Score: ${c.score.toFixed(3)}</small>
            </div>`
        ).join('');
        searchResults.classList.add('show');
    } else {
        searchResults.classList.remove('show');
    }
});

function zoomToCountry(iso3) {
    searchResults.classList.remove('show');
    searchBox.value = '';
    
    // Find and trigger click on the country
    const feature = WORLD_GEOJSON.features.find(f => 
        f.properties['ISO3166-1-Alpha-3'] === iso3
    );
    
    if (feature && RESILIENCE_DATA[iso3] && RESILIENCE_DATA[iso3].lat) {
        map.setView([RESILIENCE_DATA[iso3].lat, RESILIENCE_DATA[iso3].lon], 5);
        
        // Show country info
        currentCountry = RESILIENCE_DATA[iso3];
        document.getElementById('countryName').textContent = RESILIENCE_DATA[iso3].name;
        document.getElementById('scoreOverall').textContent = RESILIENCE_DATA[iso3].score.toFixed(3);
        document.getElementById('scoreFinancial').textContent = RESILIENCE_DATA[iso3].financial.toFixed(3);
        document.getElementById('scoreSocial').textContent = RESILIENCE_DATA[iso3].social.toFixed(3);
        document.getElementById('scoreInstitutional').textContent = RESILIENCE_DATA[iso3].institutional.toFixed(3);
        document.getElementById('scoreInfrastructure').textContent = RESILIENCE_DATA[iso3].infrastructure.toFixed(3);
        document.getElementById('countryInfo').classList.add('show');
        updateChart(RESILIENCE_DATA[iso3]);
    }
}

// Initialize
loadGeoJSON();
console.log('✅ Map loaded with', Object.keys(RESILIENCE_DATA).length, 'countries');
    </script>
</body>
</html>
'''

# Write the HTML file
output_file = 'resilience_dashboard.html'
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(html_template)

print(f"\n✅ Created {output_file}")
print("   Features:")
print("   - 🔍 Search functionality (by name or ISO3)")
print("   - 📊 Interactive charts and statistics")
print("   - 🎨 Enhanced color scheme")
print("   - 📱 Modern responsive design")
print("   - 🌐 324 countries with INFORM Risk + World Bank data")
print("   - 📈 Real-time statistics display")
