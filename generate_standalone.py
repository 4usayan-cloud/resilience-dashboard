#!/usr/bin/env python3
"""Generate standalone HTML with embedded data"""
import json

# Load the data
with open('resilience_pillars.json', 'r') as f:
    countries_data = json.load(f)

# Note: world.geojson is too large, we'll use a simpler approach
# Just embed country data and use a marker-based map

html_template = '''<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Global Resilience Atlas</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Fraunces:wght@500;650&family=Space+Grotesk:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.css" />
    <script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.js"></script>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        :root {
            --ink: #0f172a;
            --muted: #64748b;
            --accent: #0ea5a4;
            --accent-dark: #0f766e;
            --accent-soft: rgba(14, 165, 164, 0.14);
            --panel: #ffffff;
            --shadow: 0 16px 40px rgba(15, 23, 42, 0.12);
            --radius-lg: 20px;
        }
        html, body { width: 100%; height: 100%; font-family: 'Space Grotesk', sans-serif; color: var(--ink); }
        body {
            display: flex;
            flex-direction: column;
            background: radial-gradient(circle at 20% 20%, #fef3c7 0%, transparent 50%), radial-gradient(circle at 80% 10%, #ccfbf1 0%, transparent 45%), linear-gradient(135deg, #f8fafc 0%, #eef2f7 100%);
        }
        header {
            background: linear-gradient(120deg, #0f172a 0%, #0f766e 60%, #14b8a6 100%);
            color: #f8fafc;
            padding: 18px 28px;
            flex-shrink: 0;
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-shadow: 0 10px 30px rgba(15, 23, 42, 0.25);
        }
        header h1 {
            margin: 0;
            font-size: 26px;
            font-weight: 650;
            font-family: 'Fraunces', serif;
            letter-spacing: 0.3px;
        }
        header p { margin: 6px 0 0 0; font-size: 14px; opacity: 0.9; }
        .brand { display: flex; flex-direction: column; gap: 8px; }
        .title-row { display: flex; align-items: center; gap: 12px; }
        .brand-mark { font-size: 26px; }
        .meta-pills { display: flex; flex-wrap: wrap; gap: 8px; }
        .pill {
            background: rgba(255, 255, 255, 0.15);
            border: 1px solid rgba(255, 255, 255, 0.25);
            padding: 6px 12px;
            border-radius: 999px;
            font-size: 12px;
            text-transform: uppercase;
            letter-spacing: 0.8px;
        }
        .info-btn {
            background: #f8fafc;
            color: #0f172a;
            border: none;
            padding: 10px 18px;
            border-radius: 999px;
            cursor: pointer;
            font-size: 13px;
            font-weight: 600;
            transition: all 0.2s ease;
            box-shadow: 0 8px 18px rgba(15, 23, 42, 0.25);
        }
        .info-btn:hover { transform: translateY(-2px); }
        .wrapper { display: flex; flex: 1; position: relative; gap: 18px; padding: 18px; }
        #map {
            flex: 1;
            cursor: crosshair;
            border-radius: var(--radius-lg);
            overflow: hidden;
            box-shadow: var(--shadow);
        }
        .sidebar {
            width: 360px;
            background: var(--panel);
            border-radius: var(--radius-lg);
            overflow-y: auto;
            padding: 22px;
            box-shadow: var(--shadow);
            animation: riseIn 0.4s ease;
        }
        .sidebar h2 { font-size: 18px; color: var(--ink); margin-bottom: 6px; font-weight: 600; }
        .sidebar p.helper { font-size: 13px; color: var(--muted); margin-bottom: 14px; }
        .search-box { margin-bottom: 15px; }
        .search-box input {
            width: 100%;
            padding: 12px 14px;
            border: 1px solid #e2e8f0;
            border-radius: 12px;
            font-size: 14px;
            transition: border 0.2s, box-shadow 0.2s;
            background: #f8fafc;
        }
        .search-box input:focus { outline: none; border-color: var(--accent); box-shadow: 0 0 0 3px var(--accent-soft); }
        .search-results { max-height: 200px; overflow-y: auto; background: white; border: 1px solid #e0e0e0; border-radius: 8px; margin-top: 5px; display: none; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
        .search-result-item { padding: 10px 12px; cursor: pointer; border-bottom: 1px solid #f0f0f0; transition: background 0.2s; }
        .search-result-item:hover { background: #f0f8ff; }
        .search-result-item:last-child { border-bottom: none; }
        .country-name { font-weight: 600; font-size: 16px; color: #333; margin-bottom: 8px; }
        .score-box {
            background: linear-gradient(135deg, rgba(14, 165, 164, 0.16) 0%, rgba(15, 118, 110, 0.08) 100%);
            padding: 16px;
            border-radius: 14px;
            margin: 12px 0;
            border: 1px solid rgba(15, 118, 110, 0.2);
        }
        .score-label { font-size: 11px; color: var(--muted); margin-bottom: 6px; text-transform: uppercase; letter-spacing: 0.8px; font-weight: 600; }
        .score-value { font-size: 34px; font-weight: 700; color: var(--accent-dark); }
        .pillar {
            font-size: 12px;
            margin: 8px 0;
            padding: 10px 12px;
            background: #f8fafc;
            border-radius: 10px;
            transition: all 0.2s;
            border-left: 3px solid transparent;
            cursor: help;
        }
        .pillar:hover { background: #f1f5f9; border-left-color: var(--accent); transform: translateX(3px); }
        .pillar-val { font-weight: bold; color: var(--accent-dark); float: right; font-size: 13px; }
        .legend {
            background: #f8fafc;
            padding: 16px;
            border-radius: 14px;
            margin-top: 20px;
            font-size: 12px;
            border: 1px solid #e2e8f0;
        }
        .legend-title { font-weight: 600; margin-bottom: 10px; color: var(--ink); font-size: 13px; }
        .legend-row { margin: 6px 0; display: flex; align-items: center; }
        .legend-color { display: inline-block; width: 16px; height: 16px; margin-right: 8px; border: 1px solid #999; border-radius: 3px; }
        .default { color: #999; text-align: center; padding: 20px; }
        .modal { display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.6); z-index: 1000; justify-content: center; align-items: center; animation: fadeIn 0.2s; }
        .modal.show { display: flex; }
        @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
        .modal-content { background: white; border-radius: 18px; padding: 30px; max-width: 650px; max-height: 85vh; overflow-y: auto; box-shadow: 0 10px 40px rgba(0,0,0,0.3); animation: slideUp 0.3s; }
        @keyframes slideUp { from { transform: translateY(20px); opacity: 0; } to { transform: translateY(0); opacity: 1; } }
        .modal-close { float: right; cursor: pointer; font-size: 28px; font-weight: bold; color: #999; line-height: 1; transition: all 0.2s; }
        .modal-close:hover { color: #dc143c; transform: rotate(90deg); }
        .modal h2 { color: #0066cc; margin-bottom: 20px; margin-top: 0; font-size: 24px; }
        .modal h3 { color: #0066cc; margin-top: 20px; margin-bottom: 10px; font-size: 16px; font-weight: 600; }
        .modal p { font-size: 13px; line-height: 1.6; margin-bottom: 12px; color: #333; }
        .pillar-card { background: #f9f9f9; padding: 12px; border-radius: 6px; margin: 10px 0; border-left: 4px solid #0066cc; transition: all 0.2s; }
        .pillar-card:hover { background: #f0f8ff; transform: translateX(3px); }
        .pillar-card strong { color: #0066cc; }
        @keyframes riseIn { from { transform: translateY(12px); opacity: 0; } to { transform: translateY(0); opacity: 1; } }
        @media (max-width: 768px) {
            header { flex-direction: column; align-items: flex-start; gap: 14px; }
            header h1 { font-size: 20px; }
            .wrapper { flex-direction: column; padding: 12px; }
            #map { min-height: 50vh; }
            .sidebar { width: 100%; max-height: 42vh; }
            .modal-content { padding: 20px; max-width: 90%; }
        }
        .marker-cluster { background: rgba(14, 165, 164, 0.6); border-radius: 50%; text-align: center; color: white; font-weight: bold; }
    </style>
</head>
<body>
<header>
    <div>
        <div class="brand">
            <div class="title-row">
                <span class="brand-mark">🌍</span>
                <div>
                    <h1>Global Resilience Atlas</h1>
                    <p>Interactive resilience benchmarks across ''' + str(len(countries_data)) + ''' economies</p>
                </div>
            </div>
            <div class="meta-pills">
                <span class="pill">Updated 2016-2025</span>
                <span class="pill">Scores normalized 0-1</span>
            </div>
        </div>
    </div>
    <button class="info-btn" onclick="showMethodology()">Methodology</button>
</header>

<div class="wrapper">
    <div id="map"></div>
    <div class="sidebar">
        <h2>Country Explorer</h2>
        <p class="helper">Search by name or click on a marker to explore pillar scores.</p>
        <div class="search-box">
            <input type="text" id="country-search" placeholder="Search for a country..." />
            <div id="search-results" class="search-results"></div>
        </div>
        <div id="sidebar-content">
            <p class="default">👆 Search above or click any marker on the map</p>
            <div class="legend">
                <div class="legend-title">📊 Resilience Color Scale</div>
                <div class="legend-row"><span class="legend-color" style="background:#228b22;"></span><b>Excellent</b> (0.65+) Top 25%</div>
                <div class="legend-row"><span class="legend-color" style="background:#ffff00;"></span><b>Good</b> (0.45-0.65) Average</div>
                <div class="legend-row"><span class="legend-color" style="background:#ff8c00;"></span><b>Fair</b> (0.30-0.45) Below Avg</div>
                <div class="legend-row"><span class="legend-color" style="background:#dc143c;"></span><b>Critical</b> (&lt;0.30) Needs Attention</div>
                <div style="margin-top:10px;padding-top:10px;border-top:1px solid #e0e0e0;font-size:11px;color:#666;">💡 Tip: Hover over pillars for details</div>
            </div>
        </div>
    </div>
</div>

<div id="methodology-modal" class="modal">
    <div class="modal-content">
        <span class="modal-close" onclick="closeMethodology()">&times;</span>
        <h2>Methodology & Data</h2>
        
        <h3>🎯 Overall Score</h3>
        <p>Average of four resilience pillars (Financial, Social, Institutional, Infrastructure). Normalized to 0-1 scale where 0.5 = global average.</p>
        
        <h3>📊 Normalization Method</h3>
        <p><strong>Z-Score → Percentile:</strong> Raw World Bank indicators are converted to z-scores, then mapped to cumulative normal distribution (CDF) percentiles.</p>
        
        <h3>💰 Financial Resilience</h3>
        <div class="pillar-card">
            <strong>Indicators:</strong> GDP per capita, Tax revenue %, Gross savings %
        </div>
        
        <h3>👥 Social Resilience</h3>
        <div class="pillar-card">
            <strong>Indicators:</strong> Life expectancy, Primary enrollment %, Health spending per capita
        </div>
        
        <h3>🏛️ Institutional Resilience</h3>
        <div class="pillar-card">
            <strong>Indicators:</strong> Control of Corruption, Government Effectiveness, Political Stability, Rule of Law, Regulatory Quality, Voice and Accountability
        </div>
        
        <h3>🌐 Infrastructure Resilience</h3>
        <div class="pillar-card">
            <strong>Indicators:</strong> Electricity access %, Internet users %, Water access %
        </div>
        
        <h3>📈 Data Source</h3>
        <p><strong>Source:</strong> World Bank Open Data API</p>
        <p><strong>Historical:</strong> 2016-2022 | <strong>Forecast:</strong> 2023-2025</p>
    </div>
</div>

<script>
// Embedded data
const COUNTRIES_DATA = ''' + json.dumps(countries_data) + ''';

console.log('=== RESILIENCE MAP ===');
console.log('Loaded', COUNTRIES_DATA.length, 'countries');

let countriesData = {};

// Process data
COUNTRIES_DATA.forEach(country => {
    if (country.iso3 && country.pillars) {
        const financial = country.pillars.financial?.score || 0;
        const social = country.pillars.social?.score || 0;
        const institutional = country.pillars.institutional?.score || 0;
        const infrastructure = country.pillars.infrastructure?.score || 0;
        
        const scores = [financial, social, institutional, infrastructure].filter(s => s > 0);
        const overallScore = scores.length > 0 ? scores.reduce((a, b) => a + b) / scores.length : 0;
        
        countriesData[country.iso3] = {
            iso: country.iso3,
            name: country.name,
            region: country.region,
            income: country.income,
            lat: country.lat,
            lon: country.lon,
            score: overallScore,
            financial: financial,
            social: social,
            institutional: institutional,
            infrastructure: infrastructure
        };
    }
});

// Initialize map
const map = L.map('map').setView([20, 0], 2);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '© OpenStreetMap'
}).addTo(map);

function getColor(score) {
    if (!score) return '#ddd';
    if (score < 0.30) return '#dc143c';
    if (score < 0.45) return '#ff8c00';
    if (score < 0.65) return '#ffff00';
    return '#228b22';
}

function showCountry(country) {
    const scoreLevel = country.score >= 0.65 ? 'Excellent' : country.score >= 0.45 ? 'Good' : country.score >= 0.30 ? 'Fair' : 'Critical';
    const scoreColor = getColor(country.score);
    const html = `
        <div class="country-name">${country.name}</div>
        <div class="score-box">
            <div class="score-label">OVERALL RESILIENCE SCORE</div>
            <div class="score-value" style="color:${scoreColor}">${country.score.toFixed(3)}</div>
            <div style="font-size:11px;color:#666;margin-top:5px;">Rating: <strong>${scoreLevel}</strong></div>
        </div>
        <div class="pillar" title="GDP per capita, Tax revenue, Gross savings"><b>💰 Financial</b> <span class="pillar-val">${country.financial.toFixed(3)}</span></div>
        <div class="pillar" title="Life expectancy, Education enrollment, Health spending"><b>👥 Social</b> <span class="pillar-val">${country.social.toFixed(3)}</span></div>
        <div class="pillar" title="Control of corruption, Government effectiveness, Political stability"><b>🏛️ Institutional</b> <span class="pillar-val">${country.institutional.toFixed(3)}</span></div>
        <div class="pillar" title="Electricity, Internet, Water access"><b>🌐 Infrastructure</b> <span class="pillar-val">${country.infrastructure.toFixed(3)}</span></div>
        <div style="margin-top:15px;padding:10px;background:#f0f8ff;border-radius:6px;font-size:11px;color:#666;">
            💡 <strong>Quick Info:</strong> ${country.region || 'N/A'} • ${country.income || 'N/A'}
        </div>
    `;
    document.getElementById('sidebar-content').innerHTML = html;
}

function showMethodology() {
    document.getElementById('methodology-modal').classList.add('show');
}

function closeMethodology() {
    document.getElementById('methodology-modal').classList.remove('show');
}

// Add markers for each country
let markerCount = 0;
Object.values(countriesData).forEach(country => {
    if (country.lat && country.lon) {
        const color = getColor(country.score);
        const marker = L.circleMarker([country.lat, country.lon], {
            radius: 6,
            fillColor: color,
            color: '#fff',
            weight: 1,
            opacity: 1,
            fillOpacity: 0.8
        });
        
        marker.bindPopup('<b>' + country.name + '</b><br>Score: ' + country.score.toFixed(3));
        marker.on('click', () => {
            showCountry(country);
        });
        marker.addTo(map);
        markerCount++;
    }
});

console.log('✓ Added', markerCount, 'markers to map');

// Search functionality
const searchInput = document.getElementById('country-search');
const searchResults = document.getElementById('search-results');

searchInput.addEventListener('input', (e) => {
    const query = e.target.value.toLowerCase().trim();
    if (query.length < 2) {
        searchResults.style.display = 'none';
        return;
    }
    
    const matches = Object.values(countriesData)
        .filter(c => c.name.toLowerCase().includes(query))
        .slice(0, 8);
    
    if (matches.length > 0) {
        searchResults.innerHTML = matches.map(c => 
            `<div class="search-result-item" onclick="selectCountry('${c.iso}')">
                <div style="font-weight:600;">${c.name}</div>
                <div style="font-size:11px;color:#666;">Score: ${c.score.toFixed(3)} • ${c.region || ''}</div>
            </div>`
        ).join('');
        searchResults.style.display = 'block';
    } else {
        searchResults.innerHTML = '<div style="padding:10px;color:#999;">No results found</div>';
        searchResults.style.display = 'block';
    }
});

function selectCountry(iso) {
    const country = countriesData[iso];
    if (country) {
        showCountry(country);
        searchResults.style.display = 'none';
        searchInput.value = '';
        if (country.lat && country.lon) {
            map.setView([country.lat, country.lon], 5);
        }
    }
}

// Close modal on background click
document.getElementById('methodology-modal').addEventListener('click', (e) => {
    if (e.target.id === 'methodology-modal') {
        closeMethodology();
    }
});
</script>
</body>
</html>
'''

# Write the standalone HTML file
with open('resilience_map_standalone.html', 'w', encoding='utf-8') as f:
    f.write(html_template)

print("✅ Generated: resilience_map_standalone.html")
print(f"📊 Embedded {len(countries_data)} countries")
print("🌐 Open the file in any browser - no server needed!")
