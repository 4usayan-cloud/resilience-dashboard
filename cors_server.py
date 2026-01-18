#!/usr/bin/env python3
"""
CORS-enabled HTTP server for resilience dashboard
Handles CORS issues when fetching external APIs
"""

from http.server import SimpleHTTPRequestHandler, HTTPServer
import urllib.request
import json
import sys
import ssl

class CORSRequestHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        # Add CORS headers to all responses
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        super().end_headers()
    
    def do_OPTIONS(self):
        # Handle preflight requests
        self.send_response(200)
        self.end_headers()
    
    def do_GET(self):
        # Proxy requests to external APIs
        if self.path.startswith('/proxy/'):
            self.handle_proxy_request()
        else:
            # Serve local files
            super().do_GET()
    
    def handle_proxy_request(self):
        """Handle proxy requests for external APIs"""
        try:
            # Extract the target URL from the path
            target_url = self.path.replace('/proxy/', '', 1)
            
            # Decode URL encoding
            import urllib.parse
            target_url = urllib.parse.unquote(target_url)
            
            # Fetch from external API
            req = urllib.request.Request(
                target_url,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
                }
            )
            
            with urllib.request.urlopen(req, timeout=10) as response:
                data = response.read()
                
                # Send response
                self.send_response(200)
                self.send_header('Content-Type', response.headers.get('Content-Type', 'application/json'))
                self.end_headers()
                self.wfile.write(data)
                
        except Exception as e:
            # Send error response
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            error_msg = json.dumps({'error': str(e)}).encode()
            self.wfile.write(error_msg)
    
    def log_message(self, format, *args):
        # Custom logging
        print(f"[{self.log_date_time_string()}] {format % args}")

def run_server(port=8082, use_https=True):
    """Start the CORS-enabled server"""
    server_address = ('', port)
    httpd = HTTPServer(server_address, CORSRequestHandler)
    
    if use_https:
        # Wrap with SSL
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain('cert.pem', 'key.pem')
        httpd.socket = context.wrap_socket(httpd.socket, server_side=True)
        protocol = "https"
    else:
        protocol = "http"
    
    print(f"""
╔══════════════════════════════════════════════════════════╗
║  Resilience Dashboard CORS Server                        ║
║  Running on: {protocol}://localhost:{port}                      ║
║  CORS enabled for external API requests                  ║
║  Press Ctrl+C to stop                                    ║
╚══════════════════════════════════════════════════════════╝
    """)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\nServer stopped.")
        sys.exit(0)

if __name__ == '__main__':
    port = 8082
    use_https = False  # HTTP by default for local development (Chrome-friendly)
    
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print(f"Invalid port number. Using default: {port}")
    
    if len(sys.argv) > 2:
        use_https = sys.argv[2].lower() in ['https', 'ssl', 'true']
    
    run_server(port, use_https)
