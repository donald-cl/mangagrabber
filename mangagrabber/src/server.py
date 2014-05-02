"""
    Author: Donald Hui
    Date: May 2nd 2014
    Description: Tornado server main file.
"""

################################################################################

import tornado.ioloop
import tornado.web

import controller
import os.path

PY_PORT = 8889

################################################################################

""" Standard tornado application intialization """
settings = dict(
    autoreload=True,
    login_url="/login",
    cookie_secret="mg",
    template_path=os.path.join(os.path.dirname(__file__), "static"),
)

application = tornado.web.Application([
    (r"/", controller.MainHandler),
    (r"/login", controller.LoginHandler),
    (r"/static/(.*)", tornado.web.StaticFileHandler, {"path": "static"}),
], **settings)

""" Make sure we autoreload templates """
for (path, dirs, files) in os.walk(settings["template_path"]):
    for item in files:
        tornado.autoreload.watch(os.path.join(path, item))

################################################################################

def main():
    print "Starting mangagrabber on port %d" % PY_PORT
    application.listen(PY_PORT)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    main()
