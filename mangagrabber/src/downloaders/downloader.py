from BeautifulSoup import BeautifulSoup
import urllib2
import urllib
from threading import Thread

THREADS = 4
manga = 'One_Piece'
chapter = 745

already_seen_hrefs = set()

class PageDownloader(Thread):
    def __init__(self, url, page_num):
        Thread.__init__(self)
        self.url = url
        self.page_num = page_num

    def scrape(self):
        raise NotImplementedError("Abstract class Page Downloader has no implementation of scrape")

    def run(self):
        self.scrape()

class MangaStreamDownloader(PageDownloader):
    def __init__(self, start_url, offset, url, page_num):
        PageDownloader.__init__(self, url, page_num)

    def scrape(self):
        resp = urllib2.urlopen(self.url)
        html = resp.read()
        parsed_html = BeautifulSoup(html)

        img_tag = parsed_html.body.find('img', attrs={'id' : 'manga-page'}, recursive=True)
        if img_tag:
            src = img_tag['src']
            print src
            fname = '_'.join([str(name) for name in [manga, chapter, self.page_num]])
            urllib.urlretrieve(src, "../grabs/"+fname+".jpg")

    def run(self):
        self.scrape()

def download_chapter(start_url, offset):

    resp = urllib2.urlopen(start_url)
    html = resp.read()
    parsed_html = BeautifulSoup(html)

    control_div = parsed_html.body.find('div', attrs={'class':'controls'}, recursive=True)
    control_btns = control_div.findAll('div', attrs={'class':'btn-group'})
    page_items = control_btns[1].find('ul', attrs={'class':'dropdown-menu'}, recursive=True).findAll('li')
    page_links = [item.find('a') for item in page_items]
    page_hrefs = [link['href'] for link in page_links]
    print page_hrefs

    for i, href in enumerate(page_hrefs):
        if href not in already_seen_hrefs:
            t = MangaStreamDownloader(start_url, offset, href, offset + i)
            t.start()
            already_seen_hrefs.add(href)

def main():

    start_urls = ['http://readms.com/r/one_piece/745/2351/1', 'http://readms.com/r/one_piece/745/2351/16']
    download_chapter(start_urls[0], 0)
    download_chapter(start_urls[1], 16)

if __name__ == '__main__':
    main()
