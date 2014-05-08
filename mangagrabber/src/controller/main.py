import tornado.web
import tornado.template
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
        my_watchlist = []
        ms = MangaStreamChecker(my_watchlist)
        ms.debug = True
        results = ms.get_updates()

        loader = tornado.template.Loader("templates")

        current_time = time.localtime()
        current_time = time.strftime('%a, %d %b %Y %H:%M:%S GMT', current_time)

        last_updated = str(datetime.date.today()) + " " + str(current_time)

        watched_sites = ['mangastream', 'mangapanda', 'mangafox']
        watched_mangas = ['Bleach', 'One Piece', 'Naruto']

        self.write(loader.load("main_template.html").generate(
            datetime=last_updated,
            mangas=watched_mangas,
            sites=watched_sites,
            update_info=results
            ))
