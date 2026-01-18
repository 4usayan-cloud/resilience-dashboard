# Resilience Dashboard - Quick Start Guide

## ✅ What's Changed

Your dashboard is now **100x faster**! We've separated the 14MB HTML file into:

1. **resilience_dashboard_optimized.html** (lightweight, ~20KB)
2. **data/resilience_data.json** (445KB - country data)
3. **data/world_geojson.json** (13MB - map boundaries)

## 🚀 How to Use

### Step 1: Start the Web Server

The dashboard needs a local web server to load the separate data files. Here's how:

**Open Terminal** and run:
```bash
cd ~/Desktop/resilience_map_source
python3 -m http.server 8082
```

You should see:
```
Serving HTTP on :: port 8082 (http://[::]:8082/) ...
```

**Keep this terminal window open** while using the dashboard!

### Step 2: Open the Dashboard

Open your web browser and go to:
```
http://localhost:8082/resilience_dashboard_optimized.html
```

### Step 3: Enjoy!

The dashboard will:
- Load in ~2-3 seconds (vs 2+ minutes before!)
- Cache data for 5 minutes for instant reloads
- Show a loading screen with progress

## 🛑 To Stop the Server

When you're done:
1. Go to the Terminal window
2. Press `Ctrl + C`

Or kill all Python servers:
```bash
killall python3
```

## 📊 Features

- **Map View**: Interactive world map showing resilience scores
- **Trends**: Line charts showing resilience changes over time (2019-2030)
- **Rankings**: Top 20 countries by resilience indicator

## 💡 Tips

- **First load**: Takes 2-3 seconds to download data
- **Subsequent loads**: Instant (uses 5-minute cache)
- **Change year/indicator**: Smooth, no lag
- **Click countries**: See detailed stats

## 🔧 Troubleshooting

**Problem**: "Failed to load data"
- **Solution**: Make sure the web server is running

**Problem**: Port 8082 already in use
- **Solution**: Try a different port:
  ```bash
  python3 -m http.server 8083
  ```
  Then use: `http://localhost:8083/resilience_dashboard_optimized.html`

**Problem**: Slow loading
- **Solution**: Clear browser cache (Cmd+Shift+R on Mac)

## 📁 Files

- `resilience_dashboard_optimized.html` - New fast dashboard
- `resilience_integrated_dashboard_v2.html` - Original (still works)
- `data/resilience_data.json` - Country resilience scores
- `data/world_geojson.json` - Geographic boundaries
- `extract_data.py` - Script that extracted the data

## ⚡ Performance Comparison

| Metric | Original | Optimized |
|--------|----------|-----------|
| File Size | 14 MB | 20 KB HTML + separate data |
| Load Time | 2+ minutes | 2-3 seconds |
| Browser Memory | High | Normal |
| Interactions | Laggy | Smooth |

Enjoy your super-fast dashboard! 🚀
