from tornado import ioloop, web

from .handler.timed import TimedHandler


if __name__ == "__main__":
    application = web.Application([
        (r"/", TimedHandler),
    ])

    application.listen(8888)
    ioloop.IOLoop.instance().start()
