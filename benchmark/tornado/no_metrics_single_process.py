from tornado import ioloop, web

from .handler.untimed import UntimedHandler


if __name__ == "__main__":
    application = web.Application([
        (r"/", UntimedHandler),
    ])

    application.listen(8888)
    ioloop.IOLoop.instance().start()
