import json
import numpy as np

# Load the live data
with open('resilience_data_live.json', 'r') as f:
    data = json.load(f)

# Get all scores
scores = [c['score'] for c in data if c['score'] > 0]
scores.sort()

print(f"Total countries with scores: {len(scores)}")
print(f"\nScore distribution:")
print(f"  Min: {min(scores):.3f}")
print(f"  25th percentile: {np.percentile(scores, 25):.3f}")
print(f"  Median (50th): {np.percentile(scores, 50):.3f}")
print(f"  75th percentile: {np.percentile(scores, 75):.3f}")
print(f"  Max: {max(scores):.3f}")

print(f"\nCurrent color thresholds:")
print(f"  Red: < 0.20 → {sum(1 for s in scores if s < 0.20)} countries")
print(f"  Orange: 0.20-0.35 → {sum(1 for s in scores if 0.20 <= s < 0.35)} countries")
print(f"  Yellow: 0.35-0.50 → {sum(1 for s in scores if 0.35 <= s < 0.50)} countries")
print(f"  White: 0.50-0.70 → {sum(1 for s in scores if 0.50 <= s < 0.70)} countries")
print(f"  Green: >= 0.70 → {sum(1 for s in scores if s >= 0.70)} countries")

print(f"\nSuggested percentile-based thresholds:")
print(f"  Red: < {np.percentile(scores, 20):.3f} (bottom 20%)")
print(f"  Orange: {np.percentile(scores, 20):.3f} - {np.percentile(scores, 40):.3f}")
print(f"  Yellow: {np.percentile(scores, 40):.3f} - {np.percentile(scores, 60):.3f}")
print(f"  Light Green: {np.percentile(scores, 60):.3f} - {np.percentile(scores, 80):.3f}")
print(f"  Dark Green: >= {np.percentile(scores, 80):.3f} (top 20%)")
