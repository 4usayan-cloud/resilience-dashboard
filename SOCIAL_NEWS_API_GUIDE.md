# Social Media & News API Integration Guide

## 🎉 New Features Added - January 17, 2026

### ✅ What's New

#### 1. **Multiple Timezone Display** 🌍
The dashboard header now shows real-time clocks for:
- **🇮🇳 IST (India Standard Time)** - UTC+5:30
- **🗾 Tokyo Time** - UTC+9
- **🦘 Sydney Time (AEDT/AEST)** - UTC+10/+11 (DST aware)
- **🇺🇸 EST (US Eastern)** - UTC-5/-4 (DST aware)

All times update every second automatically!

#### 2. **Social Media Feeds Tab** 📱
Access live social media content from:
- **Reddit** ✅ (Working - No auth required)
- **YouTube** (Requires API key)
- **X (Twitter)** (Requires auth token)
- **Instagram** (Requires access token)

#### 3. **Live News Feeds Tab** 📰
Access breaking news from:
- **Inshorts** ✅ (Working - Quick news summaries)
- **BBC World News** ✅ (Working - RSS feed)
- **NewsAPI** (Requires free API key)
- **Ground News** (Requires API subscription)

---

## 🚀 Currently Working (No Setup Required)

### ✅ Reddit Feed
- **Source**: r/worldnews
- **Update**: Real-time top posts
- **Content**: Title, upvotes, comments, timestamps
- **API**: Public JSON endpoint (no authentication)

### ✅ Inshorts News
- **Source**: Inshorts API
- **Update**: Latest short news summaries
- **Content**: Title, content, author, timestamp
- **API**: Free unofficial API

### ✅ BBC World News
- **Source**: BBC RSS feed
- **Update**: Latest world news headlines
- **Content**: Title, description, publication date
- **API**: RSS2JSON converter (free service)

---

## 🔑 APIs That Require Configuration

### 1. **YouTube Data API v3**

**Cost**: Free (10,000 quota units/day)

**Setup Steps:**
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable "YouTube Data API v3"
4. Create credentials (API Key)
5. Copy your API key

**Add to Dashboard:**
```javascript
// In resilience_dashboard_optimized.html, find loadYouTubeFeed function
const YOUTUBE_API_KEY = 'YOUR_API_KEY_HERE';
const response = await fetch(
    `https://www.googleapis.com/youtube/v3/search?part=snippet&q=world+news&type=video&maxResults=10&order=date&key=${YOUTUBE_API_KEY}`
);
```

**Free Quota**: 10,000 units/day (~1,000 searches)

---

### 2. **X (Twitter) API**

**Cost**: Free tier available (Basic plan)

**Setup Steps:**
1. Apply for developer account at [developer.twitter.com](https://developer.twitter.com/)
2. Create a new App
3. Get your Bearer Token
4. Enable OAuth 2.0

**Add to Dashboard:**
```javascript
// In resilience_dashboard_optimized.html, find loadTwitterFeed function
const TWITTER_BEARER_TOKEN = 'YOUR_BEARER_TOKEN_HERE';
const response = await fetch(
    'https://api.twitter.com/2/tweets/search/recent?query=world%20news&max_results=10',
    {
        headers: {
            'Authorization': `Bearer ${TWITTER_BEARER_TOKEN}`
        }
    }
);
```

**Free Limits**: 
- 500,000 tweets/month (read)
- 1,500 tweets/month (write)

---

### 3. **Instagram Basic Display API**

**Cost**: Free

**Setup Steps:**
1. Go to [Meta for Developers](https://developers.facebook.com/)
2. Create an App
3. Add "Instagram Basic Display" product
4. Get Access Token
5. Configure OAuth redirect

**Add to Dashboard:**
```javascript
// In resilience_dashboard_optimized.html, find loadInstagramFeed function
const INSTAGRAM_ACCESS_TOKEN = 'YOUR_ACCESS_TOKEN_HERE';
const response = await fetch(
    `https://graph.instagram.com/me/media?fields=id,caption,media_url,timestamp&access_token=${INSTAGRAM_ACCESS_TOKEN}`
);
```

**Note**: Only shows your own posts or accounts you have permission to access.

---

### 4. **NewsAPI.org**

**Cost**: Free tier available

**Setup Steps:**
1. Register at [newsapi.org/register](https://newsapi.org/register)
2. Get your API key (instant)
3. Copy API key

**Add to Dashboard:**
```javascript
// In resilience_dashboard_optimized.html, find loadNewsAPIFeed function
const NEWSAPI_KEY = 'YOUR_API_KEY_HERE';
const response = await fetch(
    `https://newsapi.org/v2/top-headlines?country=us&category=general&apiKey=${NEWSAPI_KEY}`
);
```

**Free Limits**:
- 100 requests per day
- Development mode only
- Top headlines and everything endpoints

---

### 5. **Ground News API**

**Cost**: Paid subscription required

**Setup Steps:**
1. Visit [ground.news/api](https://ground.news/api)
2. Request API access
3. Subscribe to API plan
4. Get API credentials

**Pricing**: Contact Ground News for pricing

**Features**:
- Multi-perspective news coverage
- Bias ratings
- Source diversity metrics
- Blindspot analysis

---

## 📁 Implementation Guide

### Where to Add API Keys

Open the file:
```
/Users/sayansen/Desktop/resilience_map_source/resilience_dashboard_optimized.html
```

Find the appropriate function and add your API key:

**Location in File:**
- **YouTube**: Search for `async function loadYouTubeFeed()` (around line 1380)
- **Twitter**: Search for `async function loadTwitterFeed()` (around line 1400)
- **Instagram**: Search for `async function loadInstagramFeed()` (around line 1420)
- **NewsAPI**: Search for `async function loadNewsAPIFeed()` (around line 1490)

### Security Best Practice

⚠️ **Never commit API keys to public repositories!**

For production use:
1. Store keys in environment variables
2. Use a backend proxy server
3. Implement key rotation
4. Monitor API usage

---

## 🌐 Free Alternatives (No Auth Required)

### Already Implemented ✅

1. **Reddit Public JSON API**
   - Any subreddit: `https://www.reddit.com/r/SUBREDDIT/.json`
   - No authentication needed
   - Rate limit: ~60 requests/minute

2. **RSS Feeds via RSS2JSON**
   - BBC: `http://feeds.bbci.co.uk/news/world/rss.xml`
   - Reuters: `http://feeds.reuters.com/reuters/topNews`
   - Al Jazeera: `https://www.aljazeera.com/xml/rss/all.xml`
   - Converted via: `https://api.rss2json.com/v1/api.json`

3. **Inshorts Unofficial API**
   - Endpoint: `https://inshortsapi.vercel.app/news`
   - Categories: all, national, business, sports, tech, etc.
   - No auth required

### Additional Free APIs You Can Add

#### NewsData.io
- **Free tier**: 200 requests/day
- **Signup**: [newsdata.io](https://newsdata.io/)
- **Endpoint**: `https://newsdata.io/api/1/news`

#### The Guardian API
- **Free tier**: 12 requests/second
- **Signup**: [open-platform.theguardian.com](https://open-platform.theguardian.com/)
- **Endpoint**: `https://content.guardianapis.com/search`

#### Currents API
- **Free tier**: 600 requests/day
- **Signup**: [currentsapi.services](https://currentsapi.services/)
- **Endpoint**: `https://api.currentsapi.services/v1/latest-news`

---

## 📊 Current Dashboard Status

### Working Features ✅
| Feature | Status | Auth Required | Updates |
|---------|--------|---------------|---------|
| IST Timezone | ✅ Working | No | Real-time |
| Tokyo Timezone | ✅ Working | No | Real-time |
| Sydney Timezone | ✅ Working | No | Real-time |
| EST Timezone | ✅ Working | No | Real-time |
| Reddit Feed | ✅ Working | No | Live |
| Inshorts News | ✅ Working | No | Live |
| BBC News | ✅ Working | No | Live |

### Requires Configuration 🔑
| Feature | Status | Auth Type | Free Tier |
|---------|--------|-----------|-----------|
| YouTube | ⚙️ Setup Required | API Key | 10k units/day |
| X (Twitter) | ⚙️ Setup Required | Bearer Token | 500k tweets/month |
| Instagram | ⚙️ Setup Required | Access Token | Yes |
| NewsAPI | ⚙️ Setup Required | API Key | 100 req/day |
| Ground News | ⚙️ Setup Required | Subscription | Paid only |

---

## 🎯 Testing the New Features

### 1. Access the Dashboard
Open your browser to:
```
http://localhost:8082/resilience_dashboard_optimized.html
```

### 2. Check Timezones
Look at the header - you should see 4 different time zones updating every second.

### 3. Navigate to Social Media Tab
Click **"📱 Social Media"** in the navigation:
- Reddit feed should load automatically
- YouTube, X, Instagram show setup instructions

### 4. Navigate to Live News Tab
Click **"📰 Live News"** in the navigation:
- Inshorts should load automatically
- BBC news should load automatically
- NewsAPI and Ground News show setup instructions

---

## 🔧 Troubleshooting

### Issue: Reddit feed not loading
**Solution**: Check CORS. Reddit's JSON API is public but may be blocked by some networks.
```javascript
// Try using a CORS proxy
const response = await fetch(
    'https://api.allorigins.win/get?url=' + 
    encodeURIComponent('https://www.reddit.com/r/worldnews/.json')
);
```

### Issue: Inshorts feed not loading
**Solution**: The unofficial API might be down. Switch to alternative:
```javascript
// Use RSS2JSON with Inshorts RSS
const response = await fetch(
    'https://api.rss2json.com/v1/api.json?rss_url=' +
    encodeURIComponent('https://www.inshorts.com/en/read/national')
);
```

### Issue: Timezones not showing
**Solution**: Check JavaScript console for errors. Ensure `updateTimestamp()` is being called.

### Issue: API rate limits exceeded
**Solution**: Implement caching:
```javascript
// Cache API responses for 5 minutes
const CACHE_DURATION = 5 * 60 * 1000;
```

---

## 📝 API Key Configuration Template

Create a file `api-config.js` (don't commit to Git!):

```javascript
// API Configuration
const API_KEYS = {
    youtube: 'YOUR_YOUTUBE_API_KEY',
    twitter: 'YOUR_TWITTER_BEARER_TOKEN',
    instagram: 'YOUR_INSTAGRAM_ACCESS_TOKEN',
    newsapi: 'YOUR_NEWSAPI_KEY',
    groundnews: 'YOUR_GROUNDNEWS_KEY'
};

// Export for use in dashboard
window.API_KEYS = API_KEYS;
```

Add to HTML:
```html
<script src="api-config.js"></script>
```

---

## 🎨 Customization Tips

### Change Timezone Display
Edit the timezones shown in header:
```javascript
// Add more timezones
const londonTime = new Date(now.toLocaleString('en-US', { 
    timeZone: 'Europe/London' 
}));

// Change format
toLocaleTimeString('en-US', { 
    hour: '2-digit', 
    minute: '2-digit',
    hour12: false // 24-hour format
});
```

### Change News Sources
Modify RSS feeds:
```javascript
// Add CNN RSS
const cnnResponse = await fetch(
    'https://api.rss2json.com/v1/api.json?rss_url=' +
    encodeURIComponent('http://rss.cnn.com/rss/edition_world.rss')
);
```

### Customize Social Media Display
Adjust post count and styling:
```javascript
// Show more posts
const response = await fetch(
    'https://www.reddit.com/r/worldnews/top/.json?limit=20'
);

// Different subreddit
const response = await fetch(
    'https://www.reddit.com/r/technology/hot/.json?limit=10'
);
```

---

## 📚 Additional Resources

- [Reddit API Documentation](https://www.reddit.com/dev/api/)
- [YouTube API Documentation](https://developers.google.com/youtube/v3)
- [Twitter API Documentation](https://developer.twitter.com/en/docs)
- [Instagram API Documentation](https://developers.facebook.com/docs/instagram-basic-display-api)
- [NewsAPI Documentation](https://newsapi.org/docs)
- [RSS2JSON Service](https://rss2json.com/)

---

**Created**: January 17, 2026  
**Author**: Sayan Sen  
**Version**: 4.0 - Social Media & News Integration  
**Last Updated**: January 17, 2026

---

## 🎯 Quick Start Checklist

- [x] Multiple timezones displaying
- [x] Social Media tab added
- [x] Live News tab added
- [x] Reddit feed working (no auth)
- [x] Inshorts feed working (no auth)
- [x] BBC feed working (no auth)
- [ ] YouTube API configured (optional)
- [ ] Twitter API configured (optional)
- [ ] Instagram API configured (optional)
- [ ] NewsAPI configured (optional)
- [ ] Ground News configured (optional)

**3/8 features working out of the box!** 🎉

Configure the remaining APIs to unlock all features.
