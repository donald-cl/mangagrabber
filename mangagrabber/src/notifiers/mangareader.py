from base_notifier import SiteChecker

class MangaReaderChecker(SiteChecker):
    def __init__(self, manga_watchlist, sitename="mangareader", homepage='http://mangareader.net/'):
        SiteChecker.__init__(self, manga_watchlist, sitename, homepage)

    def scrape_updates(self):
        parsed_html = self.parse_page()
        todays_items = parsed_html.find('table', attrs={'class':'updates'})
        new_items = todays_items.findAll('tr', attrs={'class':'c3'})

        all_updates = ''

        for item in new_items:

            anchor = item.find('a', attrs={'class':'chaptersrec'}, recursive=True)
            if anchor:
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

        return all_updates, None

def main():
    #my_watchlist = ['bleach', 'naruto', 'one piece']
    my_watchlist = []
    ms = MangaReaderChecker(my_watchlist)
    ms.debug = True
    ms.get_updates()

if __name__ == '__main__':
    main()
