"""
Integrate INFORM Risk data with World Bank data for comprehensive resilience scores
"""
import pandas as pd
import json

print("=" * 80)
print("INTEGRATING INFORM RISK DATA WITH WORLD BANK DATA")
print("=" * 80)

# Load INFORM data from Excel
print("\n📂 Loading INFORM Risk data...")
inform_file = '/Users/sayansen/Desktop/INFORM_Risk_Mid_2025_v071.xlsx'
inform_df = pd.read_excel(inform_file, sheet_name=0, header=1)

print(f"✓ Loaded {len(inform_df)} countries from INFORM dataset")
print(f"Columns: {list(inform_df.columns[:10])}")

# Load existing World Bank data
print("\n📂 Loading World Bank data...")
with open('resilience_data_live.json', 'r') as f:
    wb_data = json.load(f)

print(f"✓ Loaded {len(wb_data)} countries from World Bank data")

# Create lookup by country name and ISO3
wb_lookup = {c['iso3']: c for c in wb_data}
wb_by_name = {c['name'].lower(): c for c in wb_data}

# Merge INFORM data with World Bank data
merged_data = []
inform_matched = 0
inform_added = 0

for idx, row in inform_df.iterrows():
    country_name = row.get('Country', '')
    iso3 = row.get('ISO3', '')
    inform_risk = row.get('INFORM Risk', None)
    
    if pd.isna(country_name) or pd.isna(iso3):
        continue
    
    # Convert INFORM Risk (0-10 scale, higher = worse) to resilience (0-1 scale, higher = better)
    resilience_from_inform = 0
    if inform_risk and not pd.isna(inform_risk):
        resilience_from_inform = (10 - float(inform_risk)) / 10
    
    # Check if country exists in World Bank data
    if iso3 in wb_lookup:
        country = wb_lookup[iso3]
        # Add INFORM-specific score
        country['inform_risk'] = float(inform_risk) if inform_risk and not pd.isna(inform_risk) else 0
        country['inform_resilience'] = round(resilience_from_inform, 3)
        
        # Recalculate overall score to include INFORM data (weighted average)
        # Weight: 60% World Bank pillars, 40% INFORM
        wb_score = (country['financial'] + country['social'] + 
                   country['institutional'] + country['infrastructure']) / 4
        
        if country['inform_resilience'] > 0:
            country['score'] = round(wb_score * 0.6 + country['inform_resilience'] * 0.4, 3)
        
        merged_data.append(country)
        inform_matched += 1
    else:
        # New country from INFORM
        new_country = {
            'iso3': iso3,
            'name': country_name,
            'region': '',
            'income': '',
            'lat': None,
            'lon': None,
            'score': round(resilience_from_inform, 3),
            'financial': 0,
            'social': 0,
            'institutional': 0,
            'infrastructure': 0,
            'inform_risk': float(inform_risk) if inform_risk and not pd.isna(inform_risk) else 0,
            'inform_resilience': round(resilience_from_inform, 3),
            'last_updated': pd.Timestamp.now().strftime('%Y-%m-%d')
        }
        merged_data.append(new_country)
        inform_added += 1

# Add WB countries not in INFORM
for country in wb_data:
    if country['iso3'] not in [c['iso3'] for c in merged_data]:
        country['inform_risk'] = 0
        country['inform_resilience'] = 0
        merged_data.append(country)

# Load country coordinates from a public source
print("\n📍 Adding country coordinates...")
try:
    # Try to get coordinates from existing data or world.geojson
    with open('world.geojson', 'r') as f:
        world = json.load(f)
    
    coords_added = 0
    for country in merged_data:
        if not country['lat'] or not country['lon']:
            # Find matching feature
            for feature in world['features']:
                if feature['properties'].get('ISO3166-1-Alpha-3') == country['iso3']:
                    # Calculate centroid
                    geom = feature['geometry']
                    if geom['type'] == 'Polygon':
                        coords = geom['coordinates'][0]
                        lons = [c[0] for c in coords]
                        lats = [c[1] for c in coords]
                        country['lon'] = sum(lons) / len(lons)
                        country['lat'] = sum(lats) / len(lats)
                        coords_added += 1
                        break
                    elif geom['type'] == 'MultiPolygon':
                        # Use first polygon
                        coords = geom['coordinates'][0][0]
                        lons = [c[0] for c in coords]
                        lats = [c[1] for c in coords]
                        country['lon'] = sum(lons) / len(lons)
                        country['lat'] = sum(lats) / len(lats)
                        coords_added += 1
                        break
    
    print(f"✓ Added coordinates for {coords_added} countries")
except Exception as e:
    print(f"⚠️  Could not load coordinates: {e}")

# Save merged dataset
output_file = 'resilience_data_complete.json'
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(merged_data, f, indent=2, ensure_ascii=False)

print(f"\n✅ Saved {len(merged_data)} countries to {output_file}")
print(f"   - {inform_matched} countries merged with INFORM data")
print(f"   - {inform_added} new countries from INFORM")

# Statistics
scores_with_data = [c for c in merged_data if c['score'] > 0]
if scores_with_data:
    scores = [c['score'] for c in scores_with_data]
    print(f"\n📈 Statistics:")
    print(f"   Countries with scores: {len(scores_with_data)}")
    print(f"   Score range: {min(scores):.3f} to {max(scores):.3f}")
    print(f"   Average score: {sum(scores)/len(scores):.3f}")
    
    # Top 10 most resilient
    top10 = sorted(scores_with_data, key=lambda x: x['score'], reverse=True)[:10]
    print(f"\n🏆 Top 10 Most Resilient:")
    for i, country in enumerate(top10, 1):
        inform_str = f" (INFORM: {country['inform_risk']:.2f})" if country['inform_risk'] > 0 else ""
        print(f"   {i:2d}. {country['name']:30s} {country['score']:.3f}{inform_str}")
    
    # Bottom 10
    bottom10 = sorted(scores_with_data, key=lambda x: x['score'])[:10]
    print(f"\n⚠️  Bottom 10:")
    for i, country in enumerate(bottom10, 1):
        inform_str = f" (INFORM: {country['inform_risk']:.2f})" if country['inform_risk'] > 0 else ""
        print(f"   {i:2d}. {country['name']:30s} {country['score']:.3f}{inform_str}")

print("\n" + "=" * 80)
print("✅ DONE! Now creating enhanced user-friendly map...")
print("=" * 80)
