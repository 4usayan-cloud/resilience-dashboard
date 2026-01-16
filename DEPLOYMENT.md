# 🚀 Deployment Guide - Resilience Dashboard Online

## Quick Start - Deploy in 3 Steps

### Option 1: GitHub Pages (Recommended - Free & Easy)

#### Step 1: Create GitHub Repository
```bash
# Navigate to your project folder (already done)
cd /Users/sayansen/Desktop/resilience_map_source

# Create a new repository on GitHub.com:
# 1. Go to https://github.com/new
# 2. Name it: resilience-dashboard
# 3. Make it public
# 4. Don't initialize with README (we have one)
```

#### Step 2: Connect and Push
```bash
# Replace YOUR_USERNAME with your GitHub username
git remote add origin https://github.com/YOUR_USERNAME/resilience-dashboard.git
git branch -M main
git push -u origin main
```

#### Step 3: Enable GitHub Pages
1. Go to your repository on GitHub
2. Click **Settings** → **Pages**
3. Under "Build and deployment":
   - Source: **GitHub Actions**
4. Wait 2-3 minutes for deployment
5. Your dashboard will be live at: `https://YOUR_USERNAME.github.io/resilience-dashboard/`

✅ **That's it!** The GitHub Actions workflow (`.github/workflows/deploy.yml`) will automatically deploy on every push.

---

### Option 2: Netlify (Alternative - Free with Drag & Drop)

#### Deploy via Netlify Drop
1. Go to https://app.netlify.com/drop
2. Drag and drop the entire `resilience_map_source` folder
3. Wait 30 seconds
4. Get your live URL: `https://random-name-123.netlify.app`

#### Deploy via Git (Better for updates)
1. Go to https://app.netlify.com/
2. Click **Add new site** → **Import an existing project**
3. Connect your Git provider (GitHub)
4. Select your repository
5. Build settings (leave default):
   - Build command: (leave empty)
   - Publish directory: `.`
6. Click **Deploy**

🎯 Your dashboard will be live at: `https://your-site-name.netlify.app`

**Custom Domain:** Settings → Domain management → Add custom domain

---

### Option 3: Vercel (Alternative - Free & Fast)

#### Deploy via Vercel CLI
```bash
# Install Vercel CLI (one-time)
npm install -g vercel

# Deploy
cd /Users/sayansen/Desktop/resilience_map_source
vercel

# Follow prompts:
# - Setup and deploy? Yes
# - Which scope? Your account
# - Link to existing project? No
# - Project name? resilience-dashboard
# - Directory? ./
# - Override settings? No
```

🎯 Your dashboard will be live at: `https://resilience-dashboard.vercel.app`

#### Deploy via Vercel Website
1. Go to https://vercel.com/new
2. Import your Git repository
3. Click **Deploy**

---

## 🔗 What You Get

### Live URLs (after deployment)
- **Main Dashboard:** `/resilience_integrated_dashboard_v2.html`
- **Auto-redirect:** `/` → redirects to main dashboard
- **Legacy versions:** All other HTML files remain accessible

### Features
✅ 8 Timezones with live DST detection  
✅ 11 API integrations updating every 5 minutes  
✅ Interactive map with real-time data layers  
✅ 253 countries with historical & forecast data  
✅ Fully responsive (mobile, tablet, desktop)  
✅ No server required - pure static hosting  
✅ Auto HTTPS/SSL certificate  
✅ Global CDN distribution  

---

## 📊 API Status & Rate Limits

### ✅ Working APIs (No Authentication Required)
- **Reddit** - 60 requests/minute
- **GDELT** - Unlimited (free tier)
- **World Bank** - Unlimited
- **GDACS** - Unlimited

### ⚠️ APIs with Limitations (Simulated Data Currently)
- **YouTube** - Requires API key (10,000 quota/day free)
- **Alpha Vantage** - Requires API key (5 requests/minute free)
- **Google Trends** - No official API (simulated)
- **IMF/OECD** - Complex authentication (simulated for now)

### 🔧 To Add Real API Keys
Edit `resilience_integrated_dashboard_v2.html`:

```javascript
// Add your API keys here (lines ~2600-2700)
const API_KEYS = {
    youtube: 'YOUR_YOUTUBE_API_KEY',
    alphaVantage: 'YOUR_ALPHA_VANTAGE_KEY',
    fred: 'YOUR_FRED_API_KEY'
};
```

**Get Free API Keys:**
- YouTube: https://console.cloud.google.com/apis/credentials
- Alpha Vantage: https://www.alphavantage.co/support/#api-key
- FRED: https://fred.stlouisfed.org/docs/api/api_key.html

---

## 🔒 Security & Performance

### CORS Proxy (Included)
The dashboard uses `https://corsproxy.io/` for APIs that block cross-origin requests. This proxy is:
- Free and reliable
- Handles CORS headers automatically
- No authentication needed

### Caching (Configured)
- HTML files: 1 hour cache
- JSON/GeoJSON: 1 hour cache
- API responses: 5 minute auto-refresh

### Headers (Configured)
✅ X-Content-Type-Options: nosniff  
✅ X-Frame-Options: DENY  
✅ X-XSS-Protection enabled  

---

## 📱 Testing Your Deployment

### Before Pushing
```bash
# Test locally
open resilience_integrated_dashboard_v2.html

# Check for JavaScript errors
# Open browser console (F12) and look for errors
```

### After Deployment
1. **Check timezones** - Should update every second
2. **Check APIs** - Open Live Data Panel, verify data loading
3. **Check map** - Zoom, click countries, toggle layers
4. **Check mobile** - Open on phone, test responsiveness
5. **Check performance** - Google PageSpeed Insights

---

## 🐛 Troubleshooting

### Dashboard not loading?
- Check browser console (F12) for errors
- Ensure `resilience_timeline_2019_2030.json` and `world.geojson` are in same directory
- Files must be served via HTTP/HTTPS (not `file://`)

### APIs not working?
- Some APIs may be blocked by CORS - this is normal
- The dashboard includes fallback simulated data
- Check network tab (F12) to see which API calls fail

### GitHub Pages not deploying?
- Go to repository → Actions tab
- Check if workflow ran successfully
- Enable GitHub Pages in Settings → Pages
- Ensure repository is public (or have GitHub Pro for private)

---

## 🎨 Customization

### Change Primary Color
Edit line ~10-15 in HTML:
```css
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
/* Change to your colors */
background: linear-gradient(135deg, #YOUR_COLOR_1 0%, #YOUR_COLOR_2 100%);
```

### Add More Timezones
Edit lines ~2475-2500, add to array:
```javascript
{ id: 'mumbai', zone: 'Asia/Kolkata', dstLabel: '' }
```

### Modify API Refresh Rate
Edit line ~2860:
```javascript
}, 300000); // Change from 5 minutes (300000ms) to your preference
```

---

## 📈 Analytics (Optional)

### Add Google Analytics
Add before `</head>` tag:
```html
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-XXXXXXXXXX');
</script>
```

---

## 🆘 Support

### File Structure
```
resilience_map_source/
├── .github/workflows/deploy.yml    # GitHub Actions deployment
├── .gitignore                      # Git ignore rules
├── netlify.toml                    # Netlify config
├── vercel.json                     # Vercel config
├── README.md                       # Documentation
├── resilience_integrated_dashboard_v2.html  # Main dashboard ⭐
├── resilience_timeline_2019_2030.json       # Data file (898KB)
└── world.geojson                           # Map boundaries (14MB)
```

### Need Help?
- **GitHub Issues:** Best for code-related questions
- **Browser Console:** Check for JavaScript errors (F12)
- **Network Tab:** See which API calls succeed/fail

---

## ✨ You're Live!

Once deployed, share your dashboard:
- **GitHub Pages:** `https://YOUR_USERNAME.github.io/resilience-dashboard/`
- **Netlify:** `https://your-site-name.netlify.app`
- **Vercel:** `https://resilience-dashboard.vercel.app`

🎉 **Congratulations! Your dashboard is now online and dynamic with real-time data!**

---

**Last Updated:** January 16, 2026  
**Dashboard Version:** 3.0 (Live & Dynamic)
