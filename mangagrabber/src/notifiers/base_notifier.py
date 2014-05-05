import os
import sys
sys.path.insert(0, os.getcwd())
from os.path import isfile

from BeautifulSoup import BeautifulSoup
import urllib2

from mailers import mail
from utils import util

class SiteChecker(object):
    def __init__(self, manga_watchlist, sitename, homepage):
        self.sitename = sitename
        self.homepage = homepage
        self.manga_watchlist = set(manga_watchlist)
        self.debug = False

    def parse_page(self):
        resp = urllib2.urlopen(self.homepage)
        html = resp.read()
        parsed_html = BeautifulSoup(html)
        return parsed_html

    def scrape_updates(self):
        raise NotImplementedError("Abstract class Site Checker has no implementation of scrape_updates")

    def get_updates(self):
        all_updates = self.scrape_updates()
        current_content = get_cache_site_diff(self.sitename, all_updates)

        if self.debug:
            print current_content
            print "============="
            print all_updates
            print "============="

        if current_content is None:
            set_cache_site_diff(self.sitename, all_updates)
        elif current_content != all_updates:
            set_cache_site_diff(self.sitename, all_updates)
            mail.ez_send_email(['donaldhui@gmail.com'], all_updates)
        elif self.debug:
            print "no new content"

        if self.debug:
            return all_updates

def set_cache_site_diff(sitename, all_updates):
    dirname = util.get_mangagrabber_dir() + "mangagrabber/updates/" + sitename + "_updates"
    if isfile(dirname):
        f = open(dirname, 'w')
    else:
        f = open(dirname, 'w+')

    f.write(all_updates)
    f.close()

def get_cache_site_diff(sitename, all_updates):
    dirname = util.get_mangagrabber_dir() + "mangagrabber/updates/" + sitename + "_updates"

    if isfile(dirname):
        f = open(dirname, 'r+')
        current_content = f.read()
        f.close()
    else:
        current_content = ""

    return current_content
