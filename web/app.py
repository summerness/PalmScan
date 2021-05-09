import tornado.httpserver
from web.routing import routings
import tornado.ioloop
import tornado.web

class Application(tornado.web.Application):
    def __init__(self):
        super(Application, self).__init__(routings)


if __name__ == '__main__':
    application = Application()
    http_server = tornado.httpserver.HTTPServer(application, xheaders=True)
    http_server.listen(port=8888)
    tornado.ioloop.IOLoop.instance().start()