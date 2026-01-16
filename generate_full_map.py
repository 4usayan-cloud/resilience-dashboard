#!/usr/bin/env python3
import json

print("Loading cleaned data...")
with open('resilience_data_cleaned.json', 'r') as f:
    countries = json.load(f)

print(f"Loaded {len(countries)} countries")

print("Loading template...")
with open('resilience_demo.html', 'r') as f:
    html = f.read()

# Replace the SAMPLE_DATA
sample_data_start = html.find('const SAMPLE_DATA = [')
sample_data_end = html.find('];', sample_data_start) + 2

if sample_data_start != -1 and sample_data_end != -1:
    print("Replacing data...")
    new_html = html[:sample_data_start] + 'const SAMPLE_DATA = ' + json.dumps(countries) + ';' + html[sample_data_end:]
    
    # Update titles and labels
    new_html = new_html.replace('Global Resilience Atlas - DEMO', 'Global Resilience Atlas')
    new_html = new_html.replace('Sample data - Replace with your resilience_pillars.json', f'Interactive resilience benchmarks across {len(countries)} economies')
    new_html = new_html.replace('<span class="pill">Demo Mode</span>', '<span class="pill">Updated 2016-2025</span>')
    
    # Remove alert box
    alert_start = new_html.find('<div class="alert">')
    if alert_start != -1:
        alert_end = new_html.find('</div>', alert_start) + 6
        new_html = new_html[:alert_start] + new_html[alert_end:]
    
    # Save
    with open('resilience_map_full.html', 'w', encoding='utf-8') as out:
        out.write(new_html)
    
    print(f"✅ Created resilience_map_full.html")
    print(f"   {len(countries)} countries")
    print(f"   File size: {len(new_html):,} bytes")
else:
    print("❌ Could not find SAMPLE_DATA")
