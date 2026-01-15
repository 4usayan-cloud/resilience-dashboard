"""
Simple Flask API for Global Resilience Dashboard
Provides dynamic data endpoints for the resilience map
"""

from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend requests

# Load data at startup
with open('resilience_pillars.json', 'r') as f:
    countries_data = json.load(f)

with open('world.geojson', 'r') as f:
    geojson_data = json.load(f)

@app.route('/')
def index():
    """Serve the main HTML file"""
    return send_from_directory('.', 'resilience_map.html')

@app.route('/api/countries', methods=['GET'])
def get_countries():
    """Get all countries with resilience data"""
    return jsonify(countries_data)

@app.route('/api/countries/<iso_code>', methods=['GET'])
def get_country(iso_code):
    """Get specific country data by ISO code"""
    if iso_code in countries_data:
        return jsonify(countries_data[iso_code])
    return jsonify({'error': 'Country not found'}), 404

@app.route('/api/geojson', methods=['GET'])
def get_geojson():
    """Get world geojson data"""
    return jsonify(geojson_data)

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get overall statistics"""
    scores = [c['score'] for c in countries_data.values() if 'score' in c]
    return jsonify({
        'total_countries': len(countries_data),
        'avg_score': sum(scores) / len(scores) if scores else 0,
        'max_score': max(scores) if scores else 0,
        'min_score': min(scores) if scores else 0
    })

@app.route('/api/top/<int:limit>', methods=['GET'])
def get_top_countries(limit):
    """Get top N countries by resilience score"""
    sorted_countries = sorted(
        countries_data.items(),
        key=lambda x: x[1].get('score', 0),
        reverse=True
    )[:limit]
    return jsonify([{
        'iso': iso,
        'name': data['name'],
        'score': data['score']
    } for iso, data in sorted_countries])

if __name__ == '__main__':
    app.run(debug=True, port=5000)
