from six.moves.BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
import json

from . import Reporter
from threading import Thread


class HTTPReporter(Reporter):
    def __init__(self, port, registry=None):
        super(HTTPReporter, self).__init__(registry)
        self.port = port
        self.thread = None
        self.httpd = None

    def start(self):
        class _RequestHandler(BaseHTTPRequestHandler):
            def do_GET(inner_self):
                inner_self.send_response(200)
                response_string = json.dumps(self.registry.get_stats())
                inner_self.send_header('Content-Type', 'application/json')
                inner_self.send_header('Content-Length', len(response_string))
                inner_self.end_headers()
                inner_self.wfile.write(response_string.encode('utf-8'))

        server_address = '', self.port

        self.httpd = HTTPServer(server_address, _RequestHandler)
        self.thread = Thread(target=self.httpd.serve_forever)
        self.thread.start()

    def stop(self):
        self.httpd.shutdown()
        self.thread.join()
