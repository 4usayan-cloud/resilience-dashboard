import json
import re

with open('resilience_pillars.json', 'r', encoding='utf-8') as f:
    content = f.read()

# Remove any leading whitespace and find the actual start
content = content.lstrip()

# Try to find the complete JSON structure
# Look for matching brackets
bracket_count = 0
brace_count = 0
json_start = -1
json_end = -1

for i, char in enumerate(content):
    if char == '[':
        if json_start == -1:
            json_start = i
        bracket_count += 1
    elif char == ']':
        bracket_count -= 1
        if bracket_count == 0 and json_start != -1 and json_end == -1:
            json_end = i + 1
            break
    elif char == '{':
        if json_start == -1:
            json_start = i
        brace_count += 1
    elif char == '}':
        brace_count -= 1
        if brace_count == 0 and bracket_count == 0 and json_start != -1 and json_end == -1:
            json_end = i + 1
            break

if json_start != -1 and json_end != -1:
    valid_json = content[json_start:json_end]
    try:
        data = json.loads(valid_json)
        
        if isinstance(data, list):
            countries = data
        elif isinstance(data, dict):
            countries = [data]
        else:
            countries = []
        
        print(f"✅ Extracted {len(countries)} countries")
        if countries:
            sample = countries[0]
            print(f"Sample: {sample.get('name', 'N/A')} ({sample.get('iso3', 'N/A')})")
        
        # Save cleaned data
        with open('resilience_data_cleaned.json', 'w', encoding='utf-8') as out:
            json.dump(countries, out, indent=2)
        
        print("✅ Saved to resilience_data_cleaned.json")
        
    except Exception as e:
        print(f"❌ Parse error: {e}")
else:
    print("❌ Could not find valid JSON structure")
