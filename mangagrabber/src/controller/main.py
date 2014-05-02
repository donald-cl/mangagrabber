import tornado.web
from cookie import COOKIE_NAME
from base import BaseAuthHandler

"""
    Request Handlers for Tornado Web Server
"""

class MainHandler(BaseAuthHandler):

    #@tornado.web.authenticated
    def get(self):
        #email = self.get_secure_cookie(COOKIE_NAME)
        #if email:
        pass
