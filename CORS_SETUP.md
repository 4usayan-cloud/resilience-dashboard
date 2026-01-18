# CORS Setup Guide

## Problem Solved
Fixed CORS (Cross-Origin Resource Sharing) policy errors when accessing external APIs from the dashboard.

## Solution Implemented

### 1. **CORS Proxy Server** (`cors_server.py`)
- Custom Python HTTP server with CORS headers enabled
- Proxies external API requests through `/proxy/` endpoint
- Supports Reddit, Inshorts, BBC RSS, and other APIs

### 2. **Updated Dashboard**
- Modified API calls to use proxy endpoint
- Pattern: `/proxy/[encoded-url]`
- Example: `/proxy/https%3A%2F%2Fwww.reddit.com%2Fr%2Fworldnews%2Ftop%2F.json%3Flimit%3D10`

## Running the Server

### Start Server
```bash
cd /Users/sayansen/Desktop/resilience_map_source
python3 cors_server.py 8082
```

Or run in background:
```bash
python3 cors_server.py 8082 &
```

### Stop Server
```bash
pkill -f "cors_server.py"
```

### Check if Running
```bash
lsof -i :8082
```

## How It Works

1. **Dashboard** makes request to `/proxy/[url]`
2. **CORS Server** receives request
3. Server adds CORS headers:
   - `Access-Control-Allow-Origin: *`
   - `Access-Control-Allow-Methods: GET, POST, OPTIONS`
   - `Access-Control-Allow-Headers: Content-Type`
4. Server fetches data from external API
5. Server returns data with CORS headers to dashboard
6. **Dashboard** receives data without CORS errors

## Supported APIs

✅ **Reddit** - `/proxy/https://www.reddit.com/r/worldnews/top/.json?limit=10`
✅ **Inshorts** - `/proxy/https://inshortsapi.vercel.app/news?category=all`
✅ **BBC RSS** - `/proxy/https://api.rss2json.com/v1/api.json?rss_url=...`

## Local HTTPS (Alternative Approach)

If you prefer HTTPS instead of HTTP with CORS proxy:

### Generate Self-Signed Certificate
```bash
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes
```

### Create HTTPS Server
```python
import http.server
import ssl

server_address = ('localhost', 8443)
httpd = http.server.HTTPServer(server_address, http.server.SimpleHTTPRequestHandler)
httpd.socket = ssl.wrap_socket(httpd.socket, 
                                server_side=True,
                                certfile='cert.pem',
                                keyfile='key.pem',
                                ssl_version=ssl.PROTOCOL_TLS)
httpd.serve_forever()
```

Access at: `https://localhost:8443` (accept certificate warning in browser)

## Deployment Options

### GitHub Pages (Recommended for Production)
- No CORS issues with GitHub Pages
- Free hosting
- HTTPS enabled by default
- Just push to repository: `4usayan-cloud/resilience-dashboard`

### Local Development
- Use `cors_server.py` for local testing
- Avoids certificate warnings
- Easy to debug

## Troubleshooting

### Still Getting CORS Errors?
1. Check server is running: `lsof -i :8082`
2. Clear browser cache: Cmd+Shift+R (Mac) or Ctrl+Shift+R (Windows)
3. Check console for error messages
4. Verify proxy URL encoding is correct

### Port Already in Use?
```bash
# Find process using port 8082
lsof -i :8082

# Kill process
kill -9 [PID]

# Or change port
python3 cors_server.py 8083
```

### API Not Loading?
1. Check API is accessible: `curl https://www.reddit.com/r/worldnews/top/.json`
2. Check proxy logs in terminal
3. Verify URL encoding in browser DevTools Network tab

## Access Dashboard

**Local**: http://localhost:8082
**Production**: Deploy to GitHub Pages (no CORS issues)

---

© 2024-2026 Sayan Sen | Last Updated: January 18, 2026
