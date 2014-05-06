'''
    Author: Donald Hui
    Date: May 5 2014
    Description: Base crawler classes / utils
'''

################################################################################

from BeautifulSoup import BeautifulSoup
from mechanize import Browser
from threading import Thread
import requests
import random
import urllib2

################################################################################

THREADS = 4

################################################################################

class AbstractCrawler(Thread):
    def __init__(self, site_name, site_url):
        Thread.__init__(self)

    def parse_page(self, url):
        resp = urllib2.urlopen(url)
        html = resp.read()
        parsed_html = BeautifulSoup(html)
        return parsed_html

    def parse_page_cookies(self, url, cookie=None):

        headers = {
                'User-Agent' : 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.24) Gecko/20111107 Linux Mint/9 (Isadora) Firefox/3.6.24',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'pl,en;q=0.7,en-us;q=0.3',
                'Accept-Encoding': 'gzip,deflate',
                'Accept-Charset': 'ISO-8859-2,utf-8;q=0.7,*;q=0.7',
                'Keep-Alive': '115',
                'Connection': 'keep-alive',
                }
        if cookie is None:
            cookie = random.random()

        cookies = dict(cookies_are=str(cookie))
        r = requests.get(url, headers=headers, cookies=cookies)
        parsed_html = BeautifulSoup(r.content)
        return parsed_html

    def parse_page_mechanize(self, url):
        br = Browser()
        br.set_handle_robots(False)
        response = br.open(url)
        parsed_html = BeautifulSoup(response.read())
        return parsed_html

    def crawl(self):
        raise NotImplementedError(
                "Abstract class AbstractCrawler has no implementation of crawl")

    def run(self):
        self.crawl()

################################################################################

class MyanimelistSearchCrawler(AbstractCrawler):
    def __init__(self, site_name, site_url):
        AbstractCrawler.__init__(self, site_name, site_url)

    class AnimeItem(object):
        def __init__(self, name, num_eps, score, members, rank, mal_url):
            self.name = name
            self.num_eps = num_eps
            self.score = score
            self.members = members
            self.rank = rank
            self.mal_url = mal_url

    def find_anime_items(self, parsed_html):
        items = parsed_html.findAll('tr', recursive=True)
        for item in items:
            tds = item.findAll('td')
            if tds and len(tds) >= 3:
                anime_item = tds[2]
                name_anchor = anime_item.find('a')
                print name_anchor.text

    def crawl(self, url_pool):
        while url_pool:
            current_url = url_pool.pop(0)
            parsed_html = self.parse_page_cookies(current_url)
            print parsed_html
            self.find_anime_items(parsed_html)

################################################################################

def main():

    visit_pool = []

    base_url = 'http://myanimelist.net/topanime.php?type=&limit='
    for i in xrange(0, 9171, 30):
        next_page = base_url + str(i)
        visit_pool.append(next_page)

    #print visit_pool

    #debug
    visit_pool = [visit_pool[0]]

    mal = MyanimelistSearchCrawler("myanimelist", "http://myanimelist.net")
    mal.crawl(visit_pool)

if __name__ == '__main__':
    main()
