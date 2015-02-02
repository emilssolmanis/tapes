from tornado import ioloop, web, httpserver

from .handler.timed import TimedHandler


if __name__ == "__main__":
    application = web.Application([
        (r"/", TimedHandler),
    ])

    server = httpserver.HTTPServer(application)
    server.bind(8888)
    server.start(0)
    ioloop.IOLoop.instance().start()
