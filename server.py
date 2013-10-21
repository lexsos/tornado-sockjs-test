import tornado
from tornado import web, ioloop
from sockjs.tornado import SockJSRouter, SockJSConnection

class EchoConnection(SockJSConnection):

    clients = set()

    def on_open(self, info):
        print 'New client'
        self.clients.add(self)

    def on_message(self, msg):
        print 'Msg:', msg
        self.broadcast(self.clients, msg)

    def on_close(self):
        print 'Client left'
        self.clients.remove(self)


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")
        if EchoConnection.clients:
            list(EchoConnection.clients)[0].broadcast(EchoConnection.clients, "br msg")
            print "br msg"

if __name__ == '__main__':
    EchoRouter = SockJSRouter(EchoConnection, '/test')

    app = web.Application(EchoRouter.urls)
    app.listen(9999)


    application = tornado.web.Application([(r"/", MainHandler),])
    application.listen(8888)

    ioloop.IOLoop.instance().start()