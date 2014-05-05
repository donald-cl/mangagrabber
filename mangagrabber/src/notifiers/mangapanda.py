import os
import sys
sys.path.insert(0, os.getcwd())

from base_notifier import SiteChecker

class MangaPandaChecker(SiteChecker):
    def __init__(self, manga_watchlist, sitename="mangapanda", homepage='http://mangapanda.com/'):
        SiteChecker.__init__(self, manga_watchlist, sitename, homepage)

    def scrape_updates(self):
        parsed_html = self.parse_page()
        todays_items = parsed_html.find('table', attrs={'class':'updates'})
        new_items = todays_items.findAll('tr', attrs={'class':'c2'})

        all_updates = ''

        for item in new_items:

            anchor = item.find('a', attrs={'class':'chaptersrec'}, recursive=True)
            href = anchor['href']
            info = anchor.text.split(' ')
            manga_name = info[0]
            chapter_num = info[1]

            if len(self.manga_watchlist) == 0 or manga_name in self.manga_watchlist:
                if self.debug:
                    print href
                    print manga_name
                    print chapter_num
                all_updates += href + manga_name + chapter_num

        return all_updates

def main():
    #my_watchlist = ['bleach', 'naruto', 'one piece']
    my_watchlist = []
    ms = MangaPandaChecker(my_watchlist)
    ms.debug = True
    ms.get_updates()

if __name__ == '__main__':
    main()
