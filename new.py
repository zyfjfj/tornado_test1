import tornado.ioloop
import tornado.web
from tornado import gen
from tornado.web import RequestHandler
import time
import tornado.options
from tornado.concurrent import Future


class GenAsyncHandler(RequestHandler):   
    @gen.coroutine
    def get(self):
        respones=yield self.api()
        self.write(respones)
    @gen.coroutine
    def api(self):
        gen.sleep(100)
        return "future"

def make_app():
    return tornado.web.Application([
        (r"/", GenAsyncHandler),
    ])


if __name__ == "__main__":
    tornado.options.parse_command_line()

    app = make_app()
    app.listen(5555)
    tornado.ioloop.IOLoop.current().start()