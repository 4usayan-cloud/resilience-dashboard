import json

# Load the data
print("Loading data...")
with open('resilience_data_cleaned.json', 'r') as f:
    data = json.load(f)
print(f"✓ Loaded {len(data)} countries")

# Read the HTML template
print("Reading HTML template...")
with open('resilience_map_enhanced.html', 'r') as f:
    html = f.read()

# Embed data directly in the HTML
print("Embedding data...")
data_str = json.dumps(data)
html = html.replace('const COUNTRIES_DATA = [];', f'const COUNTRIES_DATA = {data_str};')

# Remove fetch logic and replace with embedded loading
fetch_block = """// Load data from cleaned JSON file
        fetch('resilience_data_cleaned.json')
            .then(response => {
                if (!response.ok) throw new Error('Failed to load data');
                return response.json();
            })
            .then(data => {"""

replacement = """// Data is embedded directly
        (function() {
            const data = COUNTRIES_DATA;
            console.log('Loaded', data.length, 'countries');"""

html = html.replace(fetch_block, replacement)

# Remove the catch block
catch_block = """.catch(error => {
                console.error('Error loading data:', error);
                document.getElementById('info').innerHTML = '<p>Error loading data. Please ensure resilience_data_cleaned.json is in the same directory.</p>';
            });"""

html = html.replace(catch_block, '})();')

# Save standalone version
print("Saving standalone version...")
with open('resilience_map_standalone.html', 'w', encoding='utf-8') as f:
    f.write(html)

print(f'\n✅ Created resilience_map_standalone.html')
print(f'   - {len(data)} countries embedded')
print(f'   - File size: {len(html):,} bytes')
print('\nYou can now open resilience_map_standalone.html in your browser!')
