import json

# Load enhanced data
with open('resilience_data_enhanced.json', 'r') as f:
    data = json.load(f)

# Create data string
data_js = json.dumps(data)

# Create complete HTML with embedded data and charts
html_content = f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Global Resilience Atlas with Charts</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.css" />
    <script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; height: 100vh; display: flex; flex-direction: column; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }}
        header {{ background: rgba(0, 0, 0, 0.3); backdrop-filter: blur(10px); color: white; padding: 20px 30px; box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3); }}
        h1 {{ margin: 0; font-size: 28px; font-weight: 600; }}
        .subtitle {{ margin-top: 5px; opacity: 0.9; font-size: 14px; }}
        .container {{ flex: 1; display: flex; padding: 20px; gap: 20px; overflow: hidden; }}
        #map {{ flex: 2; border-radius: 12px; box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3); }}
        .sidebar {{ flex: 1; background: white; border-radius: 12px; padding: 20px; overflow-y: auto; box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3); max-width: 450px; }}
        .toggle-bar {{ background: white; padding: 15px; border-radius: 12px; margin-bottom: 20px; display: flex; gap: 8px; flex-wrap: wrap; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1); }}
        .toggle-btn {{ background: #f1f5f9; border: none; padding: 10px 16px; border-radius: 8px; cursor: pointer; font-size: 13px; font-weight: 600; transition: all 0.2s; color: #64748b; }}
        .toggle-btn.active {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; transform: scale(1.05); }}
        .toggle-btn:hover {{ transform: translateY(-2px); }}
        .country-info {{ background: #f8f9fa; padding: 20px; border-radius: 10px; margin-bottom: 20px; }}
        .country-name {{ font-size: 22px; font-weight: 700; color: #1e293b; margin-bottom: 15px; }}
        .score-item {{ display: flex; justify-content: space-between; padding: 12px 0; border-bottom: 1px solid #e2e8f0; }}
        .score-item:last-child {{ border-bottom: none; }}
        .score-label {{ font-weight: 600; color: #475569; }}
        .score-value {{ font-weight: 700; color: #1e293b; font-size: 16px; }}
        .chart-container {{ margin-top: 20px; height: 250px; }}
        .legend {{ background: white; padding: 15px; border-radius: 10px; margin-top: 15px; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1); }}
        .legend-title {{ font-weight: 700; margin-bottom: 10px; color: #1e293b; }}
        .legend-item {{ display: flex; align-items: center; gap: 10px; padding: 5px 0; }}
        .legend-color {{ width: 30px; height: 20px; border-radius: 4px; border: 1px solid #ddd; }}
        .placeholder {{ padding: 40px 20px; text-align: center; color: #64748b; font-style: italic; }}
    </style>
</head>
<body>
    <header>
        <h1>🌍 Global Resilience Atlas</h1>
        <p class="subtitle">Interactive map with 4 pillars: Financial, Social, Institutional & Infrastructure</p>
    </header>
    <div class="container">
        <div id="map"></div>
        <div class="sidebar">
            <div class="toggle-bar">
                <button class="toggle-btn active" onclick="setView('overall')">Overall Score</button>
                <button class="toggle-btn" onclick="setView('financial')">Financial</button>
                <button class="toggle-btn" onclick="setView('social')">Social</button>
                <button class="toggle-btn" onclick="setView('institutional')">Institutional</button>
                <button class="toggle-btn" onclick="setView('infrastructure')">Infrastructure</button>
            </div>
            <div class="legend">
                <div class="legend-title">Resilience Scale</div>
                <div class="legend-item"><div class="legend-color" style="background: #22c55e;"></div><span>High (0.70+) - Most Resilient</span></div>
                <div class="legend-item"><div class="legend-color" style="background: #ffffff;"></div><span>Good (0.50-0.70)</span></div>
                <div class="legend-item"><div class="legend-color" style="background: #fbbf24;"></div><span>Medium (0.35-0.50)</span></div>
                <div class="legend-item"><div class="legend-color" style="background: #f97316;"></div><span>Low (0.20-0.35)</span></div>
                <div class="legend-item"><div class="legend-color" style="background: #ef4444;"></div><span>Very Low (&lt;0.20) - Least Resilient</span></div>
            </div>
            <div id="country-details"><div class="placeholder">Click on any country to see detailed scores and charts</div></div>
        </div>
    </div>
    <script>
        const COUNTRIES_DATA = {data_js};
        const map = L.map('map').setView([20, 0], 2);
        L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{ attribution: '© OpenStreetMap', maxZoom: 18 }}).addTo(map);
        let currentView = 'overall';
        let markers = {{}};
        let pillarChart = null;
        
        function getColor(score) {{
            if (score >= 0.70) return '#22c55e';
            if (score >= 0.50) return '#ffffff';
            if (score >= 0.35) return '#fbbf24';
            if (score >= 0.20) return '#f97316';
            return '#ef4444';
        }}
        
        function loadCountries() {{
            console.log('Loading', COUNTRIES_DATA.length, 'countries...');
            COUNTRIES_DATA.forEach(country => {{
                if (country.lat && country.lon && country.score > 0) {{
                    const score = country[currentView === 'overall' ? 'score' : currentView] || 0;
                    const marker = L.circleMarker([country.lat, country.lon], {{
                        radius: 8, fillColor: getColor(score), color: '#fff', weight: 2, opacity: 1, fillOpacity: 0.9
                    }});
                    marker.bindPopup(`<b>${{country.name}}</b><br>Score: ${{score.toFixed(3)}}`);
                    marker.on('click', () => showCountry(country));
                    marker.addTo(map);
                    markers[country.iso3] = marker;
                }}
            }});
            console.log('✓ Added', Object.keys(markers).length, 'countries');
        }}
        
        function updateMarkers() {{
            COUNTRIES_DATA.forEach(country => {{
                if (markers[country.iso3]) {{
                    const score = country[currentView === 'overall' ? 'score' : currentView] || 0;
                    markers[country.iso3].setStyle({{ fillColor: getColor(score) }});
                }}
            }});
        }}
        
        function setView(view) {{
            currentView = view;
            document.querySelectorAll('.toggle-btn').forEach(btn => btn.classList.remove('active'));
            event.target.classList.add('active');
            updateMarkers();
        }}
        
        function showCountry(country) {{
            const html = `<div class="country-info">
                <div class="country-name">${{country.name}}</div>
                <div class="score-item"><span class="score-label">Overall:</span><span class="score-value">${{country.score.toFixed(3)}}</span></div>
                <div class="score-item"><span class="score-label">Financial:</span><span class="score-value">${{country.financial.toFixed(3)}}</span></div>
                <div class="score-item"><span class="score-label">Social:</span><span class="score-value">${{country.social.toFixed(3)}}</span></div>
                <div class="score-item"><span class="score-label">Institutional:</span><span class="score-value">${{country.institutional.toFixed(3)}}</span></div>
                <div class="score-item"><span class="score-label">Infrastructure:</span><span class="score-value">${{country.infrastructure.toFixed(3)}}</span></div>
            </div><div class="chart-container"><canvas id="pillarChart"></canvas></div>`;
            document.getElementById('country-details').innerHTML = html;
            
            if (pillarChart) pillarChart.destroy();
            const ctx = document.getElementById('pillarChart').getContext('2d');
            pillarChart = new Chart(ctx, {{
                type: 'bar',
                data: {{
                    labels: ['Financial', 'Social', 'Institutional', 'Infrastructure'],
                    datasets: [{{
                        label: 'Pillar Scores',
                        data: [country.financial, country.social, country.institutional, country.infrastructure],
                        backgroundColor: ['rgba(102, 126, 234, 0.8)', 'rgba(118, 75, 162, 0.8)', 'rgba(34, 197, 94, 0.8)', 'rgba(251, 191, 36, 0.8)'],
                        borderColor: ['rgba(102, 126, 234, 1)', 'rgba(118, 75, 162, 1)', 'rgba(34, 197, 94, 1)', 'rgba(251, 191, 36, 1)'],
                        borderWidth: 2
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {{ y: {{ beginAtZero: true, max: 1 }} }},
                    plugins: {{ legend: {{ display: false }}, title: {{ display: true, text: 'Pillar Performance Analysis', font: {{ size: 16, weight: 'bold' }} }} }}
                }}
            }});
        }}
        
        loadCountries();
    </script>
</body>
</html>'''

# Save
with open('resilience_map_with_charts.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"✅ Created resilience_map_with_charts.html")
print(f"   - {len(data)} countries embedded")
print(f"   - Interactive charts included")
print(f"   - File size: {len(html_content):,} bytes")
