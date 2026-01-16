#!/usr/bin/env python3
import pandas as pd
import json
import numpy as np

print("=" * 60)
print("PROCESSING INFORM RISK DATA - Enhanced")
print("=" * 60)

# Read the main INFORM Risk sheet with proper header
print("\n1. Reading INFORM Risk Excel file...")
df = pd.read_excel('/Users/sayansen/Desktop/INFORM_Risk_Mid_2025_v071.xlsx', 
                   sheet_name='INFORM Risk Mid 2025 (a-z)',
                   header=1)  # Use row 1 as header

print(f"✓ Loaded {len(df)} countries")
print(f"✓ Columns: {list(df.columns)[:5]}...")

# Load existing resilience data
print("\n2. Loading existing resilience data...")
with open('resilience_data_cleaned.json', 'r') as f:
    existing_data = json.load(f)

print(f"✓ Loaded {len(existing_data)} countries from existing data")

# Create mappings
existing_by_iso3 = {c['iso3']: c for c in existing_data}
existing_by_name = {c['name'].lower(): c for c in existing_data}

print("\n3. Merging INFORM Risk data with existing data...")

# Process each country
merged_data = []
matched = 0
new_countries = 0

for _, row in df.iterrows():
    country_name = str(row.iloc[0]).strip()  # First column is country name
    
    # Skip if empty or header row
    if pd.isna(country_name) or country_name == '' or country_name == '(a-z)':
        continue
    
    # Try to find in existing data
    country_data = None
    
    # Check by name match
    if country_name.lower() in existing_by_name:
        country_data = existing_by_name[country_name.lower()].copy()
        matched += 1
    else:
        # Try partial matching
        for existing_name, existing_country in existing_by_name.items():
            if country_name.lower() in existing_name or existing_name in country_name.lower():
                country_data = existing_data[list(existing_by_name.values()).index(existing_country)].copy()
                matched += 1
                break
    
    if not country_data:
        # Create new entry
        country_data = {
            'iso3': country_name[:3].upper(),
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
        new_countries += 1
    
    # Try to extract INFORM Risk score from the dataframe
    # Look for 'INFORM Risk' column
    try:
        for col in df.columns:
            col_str = str(col).strip()
            if 'INFORM' in col_str and 'Risk' in col_str and 'Hazard' not in col_str:
                inform_value = row[col]
                if pd.notna(inform_value) and inform_value > 0:
                    # Convert from risk (0-10, higher=worse) to resilience (0-1, higher=better)
                    resilience = max(0, min(1, 1 - (float(inform_value) / 10)))
                    
                    # Update if we don't have a score
                    if country_data['score'] == 0:
                        country_data['score'] = round(resilience, 4)
                        # Estimate pillar scores
                        country_data['financial'] = round(min(1.0, resilience * 0.95), 4)
                        country_data['social'] = round(min(1.0, resilience * 1.05), 4)
                        country_data['institutional'] = round(min(1.0, resilience), 4)
                        country_data['infrastructure'] = round(min(1.0, resilience * 1.02), 4)
                    break
    except Exception as e:
        pass
    
    merged_data.append(country_data)

print(f"✓ Matched {matched} countries with existing data")
print(f"✓ Created {new_countries} new country entries")

# Add existing countries that weren't in INFORM
for existing in existing_data:
    if not any(c['iso3'] == existing['iso3'] for c in merged_data):
        merged_data.append(existing)

print(f"\n4. Final dataset: {len(merged_data)} countries")

# Calculate statistics
scores = [c['score'] for c in merged_data if c['score'] > 0]
if scores:
    print(f"   Score range: {min(scores):.3f} to {max(scores):.3f}")
    print(f"   Average: {np.mean(scores):.3f}")
    print(f"   Countries with scores: {len(scores)}")

# Save
with open('resilience_data_cleaned.json', 'w', encoding='utf-8') as f:
    json.dump(merged_data, f, indent=2)

print(f"\n✅ Saved to resilience_data_cleaned.json")
print(f"\n{'='*60}")
print("✅ DATA READY! Refresh resilience_map_enhanced.html")
print(f"{'='*60}")
