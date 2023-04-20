import http.server
import ssl
import sys
from functools import partial

class CORSRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.send_header('Access-Control-Max-Age', '3600')

        # Cross-Origin-Embedder-Policy
        self.send_header('Cross-Origin-Embedder-Policy', 'require-corp')

        # Cross-Origin-Opener-Policy
        self.send_header('Cross-Origin-Opener-Policy', 'same-origin')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200, "OK")
        self.end_headers()

serve_directory = 'build/bin'

HandlerClass = partial(CORSRequestHandler, directory=serve_directory)
httpd = http.server.HTTPServer(('0.0.0.0', 8443), HandlerClass)
httpd.socket = ssl.wrap_socket(httpd.socket, keyfile='key.pem', certfile='cert.pem', server_side=True)

print("Serving HTTPS with CORS headers on localhost, port 8443...")
sys.stdout.flush()
httpd.serve_forever()