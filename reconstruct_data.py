#!/usr/bin/env python3
import json
import re

print("Reading file...")
with open('resilience_pillars.json', 'r', encoding='utf-8') as f:
    content = f.read()

print(f"File size: {len(content)} bytes")

# The file structure from what we saw:
# - Ends with: ] }
# - Contains country objects with "iso3", "name", "pillars"
# - Likely structure: { "key": [ ...countries... ] }
#  But the beginning is truncated

# Strategy: Find the first complete country object and work from there
# Look for pattern like: { "iso3": "...", "name": "..."

# Find the first "iso3" occurrence
first_iso3_pos = content.find('"iso3"')
print(f"First 'iso3' found at position: {first_iso3_pos}")

if first_iso3_pos != -1:
    # Back up to find the opening brace of this object
    search_pos = first_iso3_pos
    brace_count = 0
    found_start = -1
    
    while search_pos > 0:
        if content[search_pos] == '}':
            brace_count += 1
        elif content[search_pos] == '{':
            if brace_count == 0:
                found_start = search_pos
                break
            brace_count -= 1
        search_pos -= 1
    
    if found_start != -1:
        print(f"Found country object start at position: {found_start}")
        
        # Now search backward to see if there's a '[' before this
        array_start = -1
        for i in range(found_start - 1, max(0, found_start - 100), -1):
            if content[i] == '[':
                array_start = i
                break
        
        if array_start == -1:
            # No array start found, assume it's missing and prepend
            print("Array start '[' not found, reconstructing...")
            # Check if there's a comma before the first object
            prefix = content[max(0, found_start-10):found_start].strip()
            if prefix.endswith(','):
                # There's a comma, meaning this is not the first object
                # We need to find where the array really starts
                reconstructed = '[' + content[found_start:]
            else:
                reconstructed = '[' + content[found_start:]
        else:
            print(f"Found array start at position: {array_start}")
            reconstructed = content[array_start:]
        
        # The file structure is: [ ...countries... ]
        # There might be a } after the ] which was part of the outer object
        # Find the last ] and trim after that
        last_bracket = reconstructed.rfind(']')
        if last_bracket != -1:
            # Trim to include the last bracket only
            reconstructed = reconstructed[:last_bracket + 1]
            print(f"Trimmed to closing ] at position {last_bracket + 1}")
        
        # Try to parse
        try:
            data = json.loads(reconstructed)
            if isinstance(data, list):
                countries = data
            else:
                print(f"Unexpected data type: {type(data)}")
                countries = []
        except json.JSONDecodeError as e:
            print(f"JSON Error after reconstruction: {e}")
            print("Trying alternative approach...")
            
            # Maybe it needs to be wrapped in an object
            reconstructed_wrapped = '{"countries":' + reconstructed + '}'
            try:
                data = json.loads(reconstructed_wrapped)
                countries = data['countries']
            except Exception as e2:
                print(f"Second attempt failed: {e2}")
                countries = []
        
        if countries:
            print(f"\n✅ Successfully extracted {len(countries)} countries!")
            
            #Process
            processed = []
            for c in countries:
                if 'pillars' in c:
                    p = c['pillars']
                    f = p.get('financial', {}).get('score', 0) or 0
                    s = p.get('social', {}).get('score', 0) or 0
                    i = p.get('institutional', {}).get('score', 0) or 0
                    inf = p.get('infrastructure', {}).get('score', 0) or 0
                    
                    scores = [x for x in [f, s, i, inf] if x > 0]
                    overall = sum(scores) / len(scores) if scores else 0
                    
                    processed.append({
                        'iso3': c.get('iso3'),
                        'name': c.get('name'),
                        'region': c.get('region'),
                        'income': c.get('income'),
                        'lat': c.get('lat'),
                        'lon': c.get('lon'),
                        'score': round(overall, 4),
                        'financial': round(f, 4),
                        'social': round(s, 4),
                        'institutional': round(i, 4),
                        'infrastructure': round(inf, 4)
                    })
            
            # Save
            with open('resilience_data_cleaned.json', 'w', encoding='utf-8') as out:
                json.dump(processed, out, indent=2)
            
            print(f"✅ Saved {len(processed)} countries to resilience_data_cleaned.json\n")
            
            # Show stats
            scores = [c['score'] for c in processed if c['score'] > 0]
            if scores:
                print(f"Score range: {min(scores):.3f} to {max(scores):.3f}")
                print(f"Average score: {sum(scores)/len(scores):.3f}")
                print(f"\nSample countries:")
                for c in processed[:5]:
                    print(f"  {c['name']}: {c['score']:.3f}")
        else:
            print("❌ No countries extracted")
    else:
        print("❌ Could not find country object start")
else:
    print("❌ No 'iso3' field found in file")
