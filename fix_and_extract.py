import json

# Read the file
with open('resilience_pillars.json', 'rb') as f:
    content = f.read()

# Try to decode
try:
    # Remove BOM if present
    if content.startswith(b'\xef\xbb\xbf'):
        content = content[3:]
    
    text = content.decode('utf-8')
    
    # The file appears to be a complete JSON but maybe with leading junk
    # Try to find the outermost structure
    # Look for ']}'  or ']}' pattern which suggests end of array in object
    
    # Try parsing from different positions
    attempts = [
        0,  # From start
        text.find('{'),  # From first brace
        text.find('['),  # From first bracket
    ]
    
    data = None
    for start_pos in attempts:
        if start_pos == -1:
            continue
        try:
            data = json.loads(text[start_pos:])
            print(f"✅ Successfully parsed from position {start_pos}")
            break
        except:
            continue
    
    if data is None:
        # Try to reconstruct - the file might be truncated at start
        # Based on what we see, it seems to be missing the opening
        # Let's try to prepend array start
        reconstructed = '[' + text
        try:
            data = json.loads(reconstructed)
            print("✅ Parsed after prepending '['")
        except:
            # Try wrapping in object
            for key in ['data', 'countries', 'results']:
                try:
                    reconstructed = '{"%s": [' % key + text + ']}'
                    data = json.loads(reconstructed)
                    print(f"✅ Parsed after wrapping in object with key '{key}'")
                    data = data[key]
                    break
                except:
                    continue
    
    if data:
        if isinstance(data, list):
            countries = data
        elif isinstance(data, dict):
            # Find the array
            for key, value in data.items():
                if isinstance(value, list) and len(value) > 0:
                    countries = value
                    print(f"✅ Found array at key: {key}")
                    break
            else:
                countries = []
        else:
            countries = []
        
        print(f"\n📊 Total countries: {len(countries)}")
        if countries:
            sample = countries[0]
            print(f"Sample: {sample.get('name', 'N/A')} - {sample.get('iso3', 'N/A')}")
            
            # Calculate scores and save
            processed = []
            for country in countries:
                if 'pillars' in country:
                    financial = country['pillars'].get('financial', {}).get('score', 0)
                    social = country['pillars'].get('social', {}).get('score', 0)
                    institutional = country['pillars'].get('institutional', {}).get('score', 0)
                    infrastructure = country['pillars'].get('infrastructure', {}).get('score', 0)
                    
                    scores = [s for s in [financial, social, institutional, infrastructure] if s > 0]
                    overall = sum(scores) / len(scores) if scores else 0
                    
                    processed.append({
                        'iso3': country.get('iso3'),
                        'name': country.get('name'),
                        'region': country.get('region'),
                        'income': country.get('income'),
                        'lat': country.get('lat'),
                        'lon': country.get('lon'),
                        'score': overall,
                        'financial': financial,
                        'social': social,
                        'institutional': institutional,
                        'infrastructure': infrastructure
                    })
            
            with open('resilience_data_cleaned.json', 'w', encoding='utf-8') as out:
                json.dump(processed, out, indent=2)
            
            print(f"✅ Saved {len(processed)} countries to resilience_data_cleaned.json")
    else:
        print("❌ Could not parse JSON")
        
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
