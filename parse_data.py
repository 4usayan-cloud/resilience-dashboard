import json
import sys

try:
    with open('resilience_pillars.json', 'r', encoding='utf-8') as f:
        content = f.read().strip()
        
        # Find where valid JSON starts
        start_bracket = content.find('[')
        start_brace = content.find('{')
        
        if start_bracket == -1 and start_brace == -1:
            print("ERROR: No JSON structure found")
            sys.exit(1)
        
        # Use whichever comes first
        if start_bracket != -1 and (start_brace == -1 or start_bracket < start_brace):
            content = content[start_bracket:]
        elif start_brace != -1:
            content = content[start_brace:]
        
        # Parse JSON
        data = json.loads(content)
        
        if isinstance(data, list):
            countries = data
        elif isinstance(data, dict):
            # If it's a dict, try to find the array
            countries = None
            for key, value in data.items():
                if isinstance(value, list):
                    countries = value
                    break
            if not countries:
                countries = list(data.values())
        else:
            countries = []
        
        print(f"✅ SUCCESS: Found {len(countries)} countries")
        if countries:
            print(f"First: {countries[0].get('name', countries[0].get('iso3', 'Unknown'))}")
        
        # Save cleaned version
        with open('resilience_data_cleaned.json', 'w', encoding='utf-8') as out:
            json.dump(countries, out, indent=2)
        
        print("✅ Saved to resilience_data_cleaned.json")
        
except Exception as e:
    print(f"❌ ERROR: {e}")
    import traceback
    traceback.print_exc()
