import tornado.web
from cookie import COOKIE_NAME
from base import BaseAuthHandler
from notifiers import *
import datetime
import time

"""
    Request Handlers for Tornado Web Server
"""

class MainHandler(BaseAuthHandler):

    #@tornado.web.authenticated
    def get(self):
        #email = self.get_secure_cookie(COOKIE_NAME)
        #if email:
        now = str(datetime.date.today()) + " --- " + str(time.time())
        my_watchlist = []
        ms = MangaStreamChecker(my_watchlist)
        ms.debug = True
        results = ms.get_updates()
        self.write("<div>got updates for you: " + now + "</div><div>" + results + "</div>")
