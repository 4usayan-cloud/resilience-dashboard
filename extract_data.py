#!/usr/bin/env python3
import re
import json

# Read the HTML file
with open('resilience_integrated_dashboard_v2.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

print("Extracting RESILIENCE_DATA...")
# Extract RESILIENCE_DATA
resilience_match = re.search(r'const RESILIENCE_DATA = (\[.*?\]);', html_content, re.DOTALL)
if resilience_match:
    data_str = resilience_match.group(1)
    # Use JSON to parse
    resilience_data = json.loads(data_str)
    with open('data/resilience_data.json', 'w', encoding='utf-8') as f:
        json.dump(resilience_data, f, separators=(',', ':'))
    print(f"✓ Extracted {len(resilience_data)} countries to data/resilience_data.json")
else:
    print("✗ Could not find RESILIENCE_DATA")

print("\nExtracting WORLD_GEOJSON...")
# Extract WORLD_GEOJSON
geo_match = re.search(r'const WORLD_GEOJSON = (\{.*?\});[\s\n]*\/\/ Get color', html_content, re.DOTALL)
if geo_match:
    geo_str = geo_match.group(1)
    geo_data = json.loads(geo_str)
    with open('data/world_geojson.json', 'w', encoding='utf-8') as f:
        json.dump(geo_data, f, separators=(',', ':'))
    print(f"✓ Extracted {len(geo_data['features'])} geographic features to data/world_geojson.json")
else:
    print("✗ Could not find WORLD_GEOJSON")

print("\n✓ Data extraction complete!")
