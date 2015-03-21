from six.moves.BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
import json

from . import Reporter
from threading import Thread


class HTTPReporter(Reporter):
    """Exposes metrics via HTTP.

    For web applications, you should almost certainly just use your existing framework's capabilities. This is for
    applications that don't have HTTP easily available.
    """
    def __init__(self, port, registry=None):
        """
        :param port: Port to listen on
        :param registry: The registry to report from, defaults to the global one
        """
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
