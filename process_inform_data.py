#!/usr/bin/env python3
"""
Process INFORM Risk data and merge with existing resilience data
"""
import pandas as pd
import json
import numpy as np

print("=" * 60)
print("PROCESSING INFORM RISK DATA")
print("=" * 60)

# Read the INFORM Risk Excel file
print("\n1. Reading INFORM Risk Excel file...")
try:
    df = pd.read_excel('/Users/sayansen/Desktop/INFORM_Risk_Mid_2025_v071.xlsx', sheet_name=0)
    print(f"✓ Loaded {len(df)} rows")
    print(f"✓ Columns: {df.columns.tolist()[:10]}...")  # Show first 10 columns
except Exception as e:
    print(f"✗ Error reading Excel: {e}")
    exit(1)

# Load existing resilience data
print("\n2. Loading existing resilience data...")
try:
    with open('resilience_data_cleaned.json', 'r') as f:
        existing_data = json.load(f)
    print(f"✓ Loaded {len(existing_data)} countries from existing data")
except Exception as e:
    print(f"✗ Error loading JSON: {e}")
    exit(1)

# Create a mapping of country names/codes
existing_countries = {c['iso3']: c for c in existing_data}
existing_names = {c['name'].lower(): c['iso3'] for c in existing_data}

print("\n3. Processing INFORM Risk indicators...")

# Map INFORM data to countries
enhanced_data = []
matched = 0
unmatched = 0

for _, row in df.iterrows():
    country_name = str(row.get('Country', row.get('Iso3', 'Unknown'))).strip()
    iso3 = str(row.get('Iso3', '')).strip().upper()
    
    # Try to find matching country in existing data
    country_data = None
    if iso3 and iso3 in existing_countries:
        country_data = existing_countries[iso3].copy()
        matched += 1
    elif country_name.lower() in existing_names:
        iso3 = existing_names[country_name.lower()]
        country_data = existing_countries[iso3].copy()
        matched += 1
    else:
        # Create new country entry
        country_data = {
            'iso3': iso3 if iso3 else country_name[:3].upper(),
            'name': country_name,
            'region': '',
            'income': '',
            'lat': None,
            'lon': None,
            'score': 0,
            'financial': 0,
            'social': 0,
            'institutional': 0,
            'infrastructure': 0
        }
        unmatched += 1
    
    # Extract INFORM Risk scores (if available)
    # INFORM Risk typically has columns like:
    # - INFORM Risk, Hazard & Exposure, Vulnerability, Lack of Coping Capacity
    
    try:
        # Try to extract relevant columns (adjust based on actual Excel structure)
        inform_risk = float(row.get('INFORM Risk', row.get('INFORM RISK', 0)))
        
        # Convert INFORM Risk (0-10 scale, higher = worse) to resilience (0-1 scale, higher = better)
        # Resilience = 1 - (Risk / 10)
        if inform_risk > 0:
            resilience_score = max(0, min(1, 1 - (inform_risk / 10)))
            
            # If we don't have existing scores, use INFORM-based estimates
            if country_data['score'] == 0:
                country_data['score'] = resilience_score
                # Distribute to pillars (approximate)
                country_data['financial'] = resilience_score * 0.9  # Economic tends to be better
                country_data['social'] = resilience_score * 1.1     # Social may vary
                country_data['institutional'] = resilience_score    # Governance
                country_data['infrastructure'] = resilience_score * 1.05  # Infrastructure
                
                # Normalize to ensure all are within [0, 1]
                for key in ['financial', 'social', 'institutional', 'infrastructure']:
                    country_data[key] = min(1.0, max(0.0, country_data[key]))
    except:
        pass
    
    enhanced_data.append(country_data)

print(f"✓ Matched {matched} countries with existing data")
print(f"✓ Added {unmatched} new countries from INFORM")

# Remove duplicates and sort
seen_iso3 = set()
final_data = []
for country in enhanced_data:
    if country['iso3'] not in seen_iso3:
        seen_iso3.add(country['iso3'])
        final_data.append(country)

print(f"\n4. Final dataset: {len(final_data)} countries")

# Calculate statistics
scores = [c['score'] for c in final_data if c['score'] > 0]
print(f"   Score range: {min(scores):.3f} to {max(scores):.3f}")
print(f"   Average: {np.mean(scores):.3f}")

# Save enhanced data
output_file = 'resilience_data_enhanced.json'
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(final_data, f, indent=2)

print(f"\n✅ Saved to {output_file}")

# Also copy to the name the HTML expects
import shutil
shutil.copy(output_file, 'resilience_data_cleaned.json')
print(f"✅ Copied to resilience_data_cleaned.json (for HTML)")

print("\n" + "=" * 60)
print("PROCESSING COMPLETE!")
print("=" * 60)
print("\nYou can now open resilience_map_enhanced.html")
