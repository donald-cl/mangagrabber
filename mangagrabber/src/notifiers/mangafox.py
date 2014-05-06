import os
import sys
sys.path.insert(0, os.getcwd())

from base_notifier import MangaSiteChecker
from core import *

class MangaFoxChecker(MangaSiteChecker):
    def __init__(self, manga_watchlist, sitename="mangafox", homepage='http://mangafox.me/releases/'):
        MangaSiteChecker.__init__(self, manga_watchlist, sitename, homepage)

    def scrape_updates(self):
        parsed_html = self.parse_page()
        update_list = parsed_html.find('ul', attrs={'id':'updates'})
        list_items = update_list.findAll('li')
        item_divs = [ item.find('div') for item in list_items ]

        update_infos = []

        all_updates = ''

        for item in item_divs:

            all_chapters = item.findAll('dt')
            chapter_infos = []
            manga_name = ''

            for chapter in all_chapters:
                is_new = chapter.find('em')
                if is_new.text == 'Today':

                    header = item.find('h3', attrs={'class':'title'})
                    main_anchor = header.find('a')
                    manga_name = main_anchor.text

                    span = chapter.find('span', attrs={'class':'chapter nowrap'})

                    anchor = span.find('a')
                    href = anchor['href']
                    info = anchor.text.split(' ')
                    chapter_title = info[0]
                    chapter_num = info[1]

                    ci = ChapterInfo(manga_name, chapter_title, chapter_num, href)
                    chapter_infos.append(ci)

            ui = UpdateInfo(manga_name, chapter_infos)

            if len(self.manga_watchlist) == 0 or manga_name in self.manga_watchlist and ui is not None:
                if self.debug:
                    print str(ui)
                all_updates += str(ui)
                update_infos.append(ui)

        update_info = ''
        for ui in update_infos:
            update_info += ui.toHtml()

        all_updates = update_info

        return all_updates, update_info

def main():
    #my_watchlist = ['bleach', 'naruto', 'one piece']
    my_watchlist = []
    ms = MangaFoxChecker(my_watchlist)
    ms.debug = True
    ms.get_updates()

if __name__ == '__main__':
    main()
