import json

print("Creating forecast visualization dashboard...")

# Load forecast data
with open('resilience_forecasts_2025_2030.json', 'r') as f:
    forecast_data = json.load(f)

# Load world GeoJSON  
with open('world.geojson', 'r') as f:
    world_geojson = json.load(f)

# Create lookup
forecast_lookup = {c['iso3']: c for c in forecast_data}

print(f"✓ {len(forecast_lookup)} countries with forecasts")

# Create HTML dashboard
html = '''<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Resilience Forecast 2025-2030 | BSTS+DFM Model</title>
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; overflow: hidden; }
        
        #map { position: absolute; top: 0; bottom: 0; width: 100%; }
        
        .header {
            position: absolute; top: 0; left: 0; right: 0; height: 80px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white; padding: 20px 30px; z-index: 1001;
            box-shadow: 0 2px 20px rgba(0,0,0,0.3);
        }
        
        .header h1 { font-size: 26px; font-weight: 700; margin-bottom: 5px; }
        .header-subtitle { font-size: 13px; opacity: 0.95; }
        
        .year-slider-container {
            position: absolute; top: 100px; left: 50%; transform: translateX(-50%);
            z-index: 1000; background: white; padding: 20px 30px;
            border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.2);
            width: 600px; text-align: center;
        }
        
        .year-display {
            font-size: 32px; font-weight: 700;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
            margin-bottom: 15px;
        }
        
        .slider {
            width: 100%; height: 8px; border-radius: 4px;
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            outline: none; opacity: 0.7; transition: opacity 0.2s;
        }
        
        .slider:hover { opacity: 1; }
        
        .slider::-webkit-slider-thumb {
            -webkit-appearance: none; appearance: none;
            width: 24px; height: 24px; border-radius: 50%;
            background: white; cursor: pointer;
            box-shadow: 0 2px 10px rgba(0,0,0,0.3);
            border: 3px solid #667eea;
        }
        
        .play-controls {
            margin-top: 15px; display: flex; gap: 10px; justify-content: center;
        }
        
        .play-btn {
            padding: 10px 20px; border: none; border-radius: 8px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white; font-weight: 600; cursor: pointer;
            transition: transform 0.2s;
        }
        
        .play-btn:hover { transform: translateY(-2px); }
        
        .legend {
            position: absolute; bottom: 30px; left: 20px; z-index: 1000;
            background: white; padding: 15px; border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.15);
        }
        
        .legend h4 { margin: 0 0 10px 0; font-size: 14px; font-weight: 600; }
        .legend-item { display: flex; align-items: center; margin: 5px 0; font-size: 11px; }
        .legend-color { width: 30px; height: 18px; margin-right: 8px; border: 1px solid #ddd; border-radius: 3px; }
        
        .country-panel {
            position: absolute; top: 200px; right: 20px; z-index: 1000;
            background: white; padding: 25px; border-radius: 12px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.2); width: 400px;
            max-height: calc(100vh - 220px); overflow-y: auto; display: none;
        }
        
        .country-panel.show { display: block; }
        
        .country-panel h3 {
            margin: 0 0 20px 0; color: #667eea; font-size: 20px;
            padding-bottom: 10px; border-bottom: 2px solid #e5e7eb;
        }
        
        .close-btn {
            position: absolute; top: 20px; right: 20px; background: none;
            border: none; font-size: 28px; cursor: pointer; color: #999;
        }
        
        .close-btn:hover { color: #667eea; }
        
        .forecast-display {
            background: linear-gradient(135deg, #f9fafb 0%, #ffffff 100%);
            padding: 20px; border-radius: 8px; margin: 15px 0;
            border: 2px solid #667eea;
        }
        
        .forecast-value {
            font-size: 36px; font-weight: 700; text-align: center;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        }
        
        .forecast-label { text-align: center; color: #666; font-size: 12px; margin-top: 5px; }
        
        .confidence-interval {
            margin-top: 10px; padding: 10px; background: #f3f4f6;
            border-radius: 6px; font-size: 11px; text-align: center;
        }
        
        .trend-indicator {
            display: inline-block; padding: 5px 12px; border-radius: 20px;
            font-size: 12px; font-weight: 600; margin: 10px 0;
        }
        
        .trend-up { background: #d1fae5; color: #065f46; }
        .trend-down { background: #fee2e2; color: #991b1b; }
        .trend-stable { background: #e0e7ff; color: #3730a3; }
        
        #forecastChart { margin-top: 20px; max-height: 200px; }
        
        .model-info {
            position: absolute; bottom: 30px; right: 20px; z-index: 1000;
            background: white; padding: 15px; border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.15); font-size: 11px;
            max-width: 250px;
        }
        
        .model-info strong { color: #667eea; }
    </style>
</head>
<body>
    <div class="header">
        <h1>🔮 Resilience Forecast Dashboard</h1>
        <div class="header-subtitle">BSTS+DFM Model • Zero Percentile Weights • 2025-2030 Projections • 324 Countries</div>
    </div>
    
    <div id="map"></div>
    
    <div class="year-slider-container">
        <div class="year-display" id="yearDisplay">2026</div>
        <input type="range" min="0" max="5" value="0" class="slider" id="yearSlider">
        <div class="play-controls">
            <button class="play-btn" onclick="playAnimation()">▶ Play Animation</button>
            <button class="play-btn" onclick="resetYear()">⟲ Reset to 2026</button>
        </div>
    </div>
    
    <div class="legend">
        <h4>Forecast Resilience</h4>
        <div class="legend-item"><div class="legend-color" style="background: #d32f2f;"></div><span>Low (&lt; 0.45)</span></div>
        <div class="legend-item"><div class="legend-color" style="background: #ff9800;"></div><span>Below Avg (0.45-0.53)</span></div>
        <div class="legend-item"><div class="legend-color" style="background: #ffeb3b;"></div><span>Average (0.53-0.60)</span></div>
        <div class="legend-item"><div class="legend-color" style="background: #9ccc65;"></div><span>Above Avg (0.60-0.66)</span></div>
        <div class="legend-item"><div class="legend-color" style="background: #2e7d32;"></div><span>High (&gt; 0.66)</span></div>
    </div>
    
    <div class="model-info">
        <strong>Model:</strong> BSTS + DFM<br>
        <strong>Method:</strong> Bayesian Structural Time Series with Dynamic Factor Model<br>
        <strong>Weights:</strong> Zero Percentile (extreme values emphasized)<br>
        <strong>Confidence:</strong> 95% intervals
    </div>
    
    <div class="country-panel" id="countryPanel">
        <button class="close-btn" onclick="closePanel()">×</button>
        <h3 id="countryName"></h3>
        
        <div class="forecast-display">
            <div class="forecast-value" id="forecastValue">-</div>
            <div class="forecast-label">Predicted Resilience Score</div>
            <div class="confidence-interval" id="confidenceInterval">-</div>
        </div>
        
        <div id="trendIndicator"></div>
        
        <div style="margin-top: 20px;">
            <canvas id="forecastChart"></canvas>
        </div>
    </div>

    <script>
const FORECAST_DATA = ''' + json.dumps(forecast_lookup) + ''';
const WORLD_GEOJSON = ''' + json.dumps(world_geojson) + ''';
const YEARS = [2026, 2027, 2028, 2029, 2030];

let map, geoJsonLayer, currentYear = 2026, animationInterval = null, currentChart = null;

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
    const countryData = FORECAST_DATA[iso3];
    const score = countryData ? countryData.forecasts[currentYear.toString()]?.mean : 0;
    
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
    const countryData = FORECAST_DATA[iso3];
    
    if (!countryData) return;
    
    const forecast = countryData.forecasts[currentYear.toString()];
    const currentScore = countryData.current_score;
    const change = forecast.mean - currentScore;
    
    document.getElementById('countryName').textContent = feature.properties.name;
    document.getElementById('forecastValue').textContent = forecast.mean.toFixed(3);
    document.getElementById('confidenceInterval').textContent = 
        `95% CI: [${forecast.lower.toFixed(3)}, ${forecast.upper.toFixed(3)}]`;
    
    // Trend indicator
    let trendHTML = '';
    if (Math.abs(change) < 0.02) {
        trendHTML = '<span class="trend-indicator trend-stable">→ Stable</span>';
    } else if (change > 0) {
        trendHTML = `<span class="trend-indicator trend-up">↗ Improving +${(change*100).toFixed(1)}%</span>`;
    } else {
        trendHTML = `<span class="trend-indicator trend-down">↘ Declining ${(change*100).toFixed(1)}%</span>`;
    }
    document.getElementById('trendIndicator').innerHTML = trendHTML;
    
    document.getElementById('countryPanel').classList.add('show');
    
    updateChart(countryData);
}

function updateChart(countryData) {
    const ctx = document.getElementById('forecastChart');
    
    if (currentChart) currentChart.destroy();
    
    const years = YEARS.map(y => y.toString());
    const means = years.map(y => countryData.forecasts[y].mean);
    const uppers = years.map(y => countryData.forecasts[y].upper);
    const lowers = years.map(y => countryData.forecasts[y].lower);
    
    currentChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: ['2025', ...YEARS],
            datasets: [{
                label: 'Forecast',
                data: [countryData.current_score, ...means],
                borderColor: '#667eea',
                backgroundColor: 'rgba(102, 126, 234, 0.1)',
                borderWidth: 3,
                fill: true
            }, {
                label: 'Upper 95%',
                data: [countryData.current_score, ...uppers],
                borderColor: 'rgba(102, 126, 234, 0.3)',
                borderDash: [5, 5],
                borderWidth: 1,
                fill: false
            }, {
                label: 'Lower 95%',
                data: [countryData.current_score, ...lowers],
                borderColor: 'rgba(102, 126, 234, 0.3)',
                borderDash: [5, 5],
                borderWidth: 1,
                fill: false
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { display: true, position: 'bottom' },
                title: { display: true, text: 'Forecast Trend 2025-2030' }
            },
            scales: {
                y: { beginAtZero: true, max: 1 }
            }
        }
    });
}

function closePanel() {
    document.getElementById('countryPanel').classList.remove('show');
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
}

// Year slider
document.getElementById('yearSlider').addEventListener('input', function(e) {
    currentYear = YEARS[parseInt(e.target.value)];
    document.getElementById('yearDisplay').textContent = currentYear;
    loadGeoJSON();
});

function playAnimation() {
    if (animationInterval) {
        clearInterval(animationInterval);
        animationInterval = null;
        return;
    }
    
    let index = 0;
    animationInterval = setInterval(() => {
        if (index >= YEARS.length) {
            clearInterval(animationInterval);
            animationInterval = null;
            return;
        }
        
        document.getElementById('yearSlider').value = index;
        currentYear = YEARS[index];
        document.getElementById('yearDisplay').textContent = currentYear;
        loadGeoJSON();
        index++;
    }, 1500);
}

function resetYear() {
    currentYear = 2026;
    document.getElementById('yearSlider').value = 0;
    document.getElementById('yearDisplay').textContent = currentYear;
    loadGeoJSON();
}

loadGeoJSON();
console.log('✅ Forecast map loaded');
    </script>
</body>
</html>
'''

output_file = 'resilience_forecast_dashboard.html'
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"\n✅ Created {output_file}")
print("   Features:")
print("   - 🎬 Interactive year slider (2026-2030)")
print("   - ▶️ Play animation button")
print("   - 📊 Time series forecasts with confidence intervals")
print("   - 🎯 Zero Percentile Weights applied")
print("   - 📈 Trend indicators (improving/declining/stable)")
print("   - 🗺️ Interactive choropleth map")
