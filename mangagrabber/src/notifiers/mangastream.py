from base_notifier import SiteChecker

class MangaStreamChecker(SiteChecker):
    def __init__(self, manga_watchlist, sitename="mangastream", homepage='http://mangastream.com/'):
        SiteChecker.__init__(self, manga_watchlist, sitename, homepage)

    def scrape_updates(self):
        parsed_html = self.parse_page()
        update_list = parsed_html.find('ul', attrs={'class':'new-list'})
        new_items = update_list.findAll('li', attrs={'class':'active'})
        anchors = [item.find('a') for item in new_items]

        all_updates = ''

        for anchor in anchors:
            href = anchor['href']
            last_updated = anchor.find('span').text
            chapter_num = anchor.find('strong').text
            caption = anchor.find('em').text
            info = anchor.text
            info = info.replace(last_updated, '')
            info = info.replace(chapter_num, '')
            info = info.replace(caption, '')
            info = info.lower()
            if len(self.manga_watchlist) == 0 or info in self.manga_watchlist:
                if self.debug:
                    print href
                    print last_updated
                    print info
                    print caption
                    print chapter_num
                all_updates += href + info + caption + chapter_num

        return all_updates, None

def main():
    #my_watchlist = ['bleach', 'naruto', 'one piece']
    my_watchlist = []
    ms = MangaStreamChecker(my_watchlist)
    ms.debug = True
    ms.get_updates()

if __name__ == '__main__':
    main()
