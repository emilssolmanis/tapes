from six.moves.BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
import json


def http_reporter(port):
    def _serve(registry):
        class _RequestHandler(BaseHTTPRequestHandler):
            def do_GET(self):
                self.send_response(200)
                response_string = json.dumps(registry.get_stats())
                self.send_header('Content-Type', 'application/json')
                self.send_header('Content-Length', len(response_string))
                self.end_headers()
                self.wfile.write(response_string.encode('utf-8'))

        server_address = '', port
        httpd = HTTPServer(server_address, _RequestHandler)
        httpd.serve_forever()

    return _serve
