import json

# Read and fix the JSON file
with open('resilience_pillars.json', 'r', encoding='utf-8') as f:
    content = f.read()

# Remove any BOM
if content.startswith('\ufeff'):
    content = content[1:]

# Try to parse
try:
    data = json.loads(content)
    if isinstance(data, list):
        countries = data
    elif isinstance(data, dict):
        # Find the array in the dict
        countries = None
        for key, value in data.items():
            if isinstance(value, list) and len(value) > 0:
                countries = value
                print(f"Found array at key: {key}")
                break
        if not countries:
            print("No array found in dict")
            exit(1)
    else:
        print(f"Unexpected type: {type(data)}")
        exit(1)
        
    print(f"✅ Successfully loaded {len(countries)} countries")
    if countries:
        print(f"Sample: {countries[0].get('name', 'Unknown')}")
        
except json.JSONDecodeError as e:
    print(f"JSON Error: {e}")
    print("First 500 chars:")
    print(content[:500])
    exit(1)
