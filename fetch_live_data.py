"""
Fetch live resilience data from multiple sources
- World Bank API (Financial, Social, Institutional, Infrastructure indicators)
- INFORM Risk scores
- Process and normalize into resilience scores
"""

import json
import requests
import pandas as pd
from datetime import datetime
import time

print("=" * 80)
print("GLOBAL RESILIENCE DATA FETCHER")
print("=" * 80)

# Configuration
BASE_URL_WB = "https://api.worldbank.org/v2"
DATE_RANGE = "2019:2025"  # Most recent 5 years
ALL_COUNTRIES = "all"

# Indicator mappings
INDICATORS = {
    'financial': {
        'gdp': 'NY.GDP.MKTP.CD',
        'debt_to_gdp': 'GC.DOD.TOTL.GD.ZS',
        'fx_reserves': 'FI.RES.XGLD.MO',
        'fdi': 'BX.KLT.DINV.WD.GD.ZS',
        'trade_balance': 'NE.RSB.GNFS.ZS',
        'gdp_growth': 'NY.GDP.MKTP.KD.ZG'
    },
    'social': {
        'gini': 'SI.POV.GINI',
        'consumption': 'NE.CON.PRVT.PC.KD',
        'savings': 'NY.GNS.ICTR.ZS',
        'water': 'SH.H2O.BASW.ZS',
        'life_expectancy': 'SP.DYN.LE00.IN',
        'poverty': 'SI.POV.DDAY'
    },
    'institutional': {
        'corruption_control': 'CC.EST',
        'govt_effectiveness': 'GE.EST',
        'rule_of_law': 'RL.EST',
        'regulatory_quality': 'RQ.EST',
        'political_stability': 'PV.EST',
        'voice_accountability': 'VA.EST'
    },
    'infrastructure': {
        'road_density': 'IS.ROD.DNST.K2',
        'paved_roads': 'IS.ROD.PAVE.ZS',
        'electricity': 'EG.ELC.ACCS.ZS',
        'internet': 'IT.NET.USER.ZS',
        'mobile': 'IT.CEL.SETS.P2',
        'logistics': 'LP.LPI.OVRL.XQ'
    }
}

def fetch_indicator(indicator_code, max_retries=3):
    """Fetch data for a single indicator from World Bank API"""
    url = f"{BASE_URL_WB}/country/{ALL_COUNTRIES}/indicator/{indicator_code}"
    params = {
        'format': 'json',
        'date': DATE_RANGE,
        'per_page': 20000
    }
    
    for attempt in range(max_retries):
        try:
            response = requests.get(url, params=params, timeout=30)
            if response.status_code == 200:
                data = response.json()
                if len(data) > 1 and data[1]:
                    return data[1]
            time.sleep(1)  # Rate limiting
        except Exception as e:
            print(f"  ⚠️  Attempt {attempt + 1} failed: {e}")
            time.sleep(2)
    
    return []

def process_indicator_data(data_list):
    """Process raw indicator data into country-year dictionary"""
    result = {}
    for item in data_list:
        if item['value'] is not None:
            country_code = item['countryiso3code']
            year = int(item['date'])
            value = float(item['value'])
            
            if country_code not in result or year > result[country_code]['year']:
                result[country_code] = {'value': value, 'year': year}
    
    return result

def normalize_score(value, min_val, max_val, reverse=False):
    """Normalize a value to 0-1 scale"""
    if value is None or pd.isna(value):
        return 0
    
    if reverse:
        # For indicators where lower is better (e.g., debt, Gini)
        normalized = 1 - ((value - min_val) / (max_val - min_val))
    else:
        # For indicators where higher is better
        normalized = (value - min_val) / (max_val - min_val)
    
    return max(0, min(1, normalized))

def calculate_pillar_score(country_data, pillar):
    """Calculate resilience score for a pillar based on available indicators"""
    scores = []
    
    for indicator, value_info in country_data.get(pillar, {}).items():
        if value_info and 'value' in value_info:
            value = value_info['value']
            
            # Normalize based on indicator type
            if pillar == 'financial':
                if indicator in ['debt_to_gdp']:
                    score = normalize_score(value, 0, 200, reverse=True)
                elif indicator == 'fx_reserves':
                    score = normalize_score(value, 0, 12, reverse=False)
                elif indicator == 'fdi':
                    score = normalize_score(value, -5, 10, reverse=False)
                elif indicator == 'gdp_growth':
                    score = normalize_score(value, -10, 15, reverse=False)
                else:
                    score = 0.5
            
            elif pillar == 'social':
                if indicator == 'gini':
                    score = normalize_score(value, 25, 65, reverse=True)
                elif indicator == 'poverty':
                    score = normalize_score(value, 0, 50, reverse=True)
                elif indicator in ['water', 'life_expectancy']:
                    score = normalize_score(value, 40, 100, reverse=False)
                elif indicator == 'savings':
                    score = normalize_score(value, -10, 40, reverse=False)
                else:
                    score = 0.5
            
            elif pillar == 'institutional':
                # WGI indicators are typically -2.5 to +2.5
                score = normalize_score(value, -2.5, 2.5, reverse=False)
            
            elif pillar == 'infrastructure':
                if indicator in ['electricity', 'internet', 'paved_roads']:
                    score = normalize_score(value, 0, 100, reverse=False)
                elif indicator == 'road_density':
                    score = normalize_score(value, 0, 200, reverse=False)
                elif indicator == 'logistics':
                    score = normalize_score(value, 1, 5, reverse=False)
                else:
                    score = 0.5
            
            else:
                score = 0.5
            
            scores.append(score)
    
    return sum(scores) / len(scores) if scores else 0

print("\n📊 Fetching data from World Bank API...")
print(f"Date range: {DATE_RANGE}")

# Fetch all indicators
all_data = {}
total_indicators = sum(len(indicators) for indicators in INDICATORS.values())
current = 0

for pillar, indicators in INDICATORS.items():
    print(f"\n{pillar.upper()} Pillar:")
    all_data[pillar] = {}
    
    for name, code in indicators.items():
        current += 1
        print(f"  [{current}/{total_indicators}] Fetching {name} ({code})...", end=" ")
        
        raw_data = fetch_indicator(code)
        if raw_data:
            processed = process_indicator_data(raw_data)
            all_data[pillar][name] = processed
            print(f"✓ {len(processed)} countries")
        else:
            print("✗ No data")
        
        time.sleep(0.5)  # Rate limiting

print("\n" + "=" * 80)
print("PROCESSING AND CALCULATING RESILIENCE SCORES")
print("=" * 80)

# Get list of all countries
all_countries = set()
for pillar_data in all_data.values():
    for indicator_data in pillar_data.values():
        all_countries.update(indicator_data.keys())

print(f"\n✓ Found {len(all_countries)} countries with data")

# Build country dataset
country_dataset = []

# Load existing data for coordinates and names
try:
    with open('resilience_data_cleaned.json', 'r') as f:
        existing_data = {c['iso3']: c for c in json.load(f)}
except:
    existing_data = {}

for iso3 in sorted(all_countries):
    # Skip aggregate regions
    if iso3 in ['WLD', 'EAS', 'ECS', 'LCN', 'MEA', 'NAC', 'SAS', 'SSF']:
        continue
    
    # Gather all indicator values for this country
    country_indicators = {}
    for pillar in INDICATORS.keys():
        country_indicators[pillar] = {}
        for indicator in INDICATORS[pillar].keys():
            if indicator in all_data[pillar] and iso3 in all_data[pillar][indicator]:
                country_indicators[pillar][indicator] = all_data[pillar][indicator][iso3]
    
    # Calculate pillar scores
    financial_score = calculate_pillar_score(country_indicators, 'financial')
    social_score = calculate_pillar_score(country_indicators, 'social')
    institutional_score = calculate_pillar_score(country_indicators, 'institutional')
    infrastructure_score = calculate_pillar_score(country_indicators, 'infrastructure')
    
    # Calculate overall score (average of pillars)
    pillar_scores = [financial_score, social_score, institutional_score, infrastructure_score]
    overall_score = sum(pillar_scores) / 4 if any(pillar_scores) else 0
    
    # Get country info from existing data
    existing = existing_data.get(iso3, {})
    
    country_entry = {
        'iso3': iso3,
        'name': existing.get('name', iso3),
        'region': existing.get('region', ''),
        'income': existing.get('income', ''),
        'lat': existing.get('lat'),
        'lon': existing.get('lon'),
        'score': round(overall_score, 3),
        'financial': round(financial_score, 3),
        'social': round(social_score, 3),
        'institutional': round(institutional_score, 3),
        'infrastructure': round(infrastructure_score, 3),
        'last_updated': datetime.now().strftime('%Y-%m-%d')
    }
    
    country_dataset.append(country_entry)

# Save to file
output_file = 'resilience_data_live.json'
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(country_dataset, f, indent=2, ensure_ascii=False)

print(f"\n✅ Saved {len(country_dataset)} countries to {output_file}")

# Statistics
scores_with_data = [c for c in country_dataset if c['score'] > 0]
if scores_with_data:
    scores = [c['score'] for c in scores_with_data]
    print(f"\n📈 Statistics:")
    print(f"   Countries with scores: {len(scores_with_data)}")
    print(f"   Score range: {min(scores):.3f} to {max(scores):.3f}")
    print(f"   Average score: {sum(scores)/len(scores):.3f}")
    
    # Top 5 most resilient
    top5 = sorted(scores_with_data, key=lambda x: x['score'], reverse=True)[:5]
    print(f"\n🏆 Top 5 Most Resilient:")
    for i, country in enumerate(top5, 1):
        print(f"   {i}. {country['name']} ({country['iso3']}): {country['score']:.3f}")
    
    # Bottom 5
    bottom5 = sorted(scores_with_data, key=lambda x: x['score'])[:5]
    print(f"\n⚠️  Bottom 5:")
    for i, country in enumerate(bottom5, 1):
        print(f"   {i}. {country['name']} ({country['iso3']}): {country['score']:.3f}")

print("\n" + "=" * 80)
print("✅ DONE! Run 'python create_choropleth_map.py' with the new data file.")
print("=" * 80)
