#!/usr/bin/env python3
import json
from json import JSONDecoder

print("Reading resilience_pillars.json...")
with open('resilience_pillars.json', 'r', encoding='utf-8') as f:
    content = f.read()

print(f"File size: {len(content)} characters")

# Use JSONDecoder to find valid JSON
decoder = JSONDecoder()
idx = 0
found_data = None

print("Scanning for valid JSON...")
while idx < len(content):
    # Skip whitespace
    while idx < len(content) and content[idx] in ' \t\n\r':
        idx += 1
    
    if idx >= len(content):
        break
    
    # Try to decode from this position
    if content[idx] in '[{':
        try:
            obj, end_idx = decoder.raw_decode(content, idx)
            found_data = obj
            print(f"✅ Found valid JSON starting at position {idx}")
            break
        except Exception as e:
            idx += 1
    else:
        idx += 1

if found_data:
    # Extract countries array
    if isinstance(found_data, list):
        countries = found_data
    elif isinstance(found_data, dict):
        countries = None
        for key, value in found_data.items():
            if isinstance(value, list) and len(value) > 0:
                countries = value
                print(f"Found array at key: '{key}'")
                break
        if not countries:
            countries = [found_data]
    else:
        countries = []
    
    print(f"\n📊 Total countries found: {len(countries)}")
    
    # Process countries
    processed = []
    for c in countries:
        if 'pillars' in c:
            p = c['pillars']
            f = p.get('financial', {}).get('score', 0)
            s = p.get('social', {}).get('score', 0)
            i = p.get('institutional', {}).get('score', 0)
            inf = p.get('infrastructure', {}).get('score', 0)
            
            scores = [x for x in [f, s, i, inf] if x > 0]
            overall = sum(scores) / len(scores) if scores else 0
            
            processed.append({
                'iso3': c.get('iso3'),
                'name': c.get('name'),
                'region': c.get('region'),
                'income': c.get('income'),
                'lat': c.get('lat'),
                'lon': c.get('lon'),
                'score': overall,
                'financial': f,
                'social': s,
                'institutional': i,
                'infrastructure': inf
            })
    
    # Save processed data
    with open('resilience_data_cleaned.json', 'w', encoding='utf-8') as out:
        json.dump(processed, out, indent=2)
    
    print(f"✅ Saved {len(processed)} countries to resilience_data_cleaned.json")
    if processed:
        sample = processed[0]
        print(f"\nSample country: {sample['name']} ({sample['iso3']})")
        print(f"  Overall Score: {sample['score']:.3f}")
        print(f"  Financial: {sample['financial']:.3f}")
        print(f"  Social: {sample['social']:.3f}")
        print(f"  Institutional: {sample['institutional']:.3f}")
        print(f"  Infrastructure: {sample['infrastructure']:.3f}")
else:
    print("❌ No valid JSON structure found in file")
