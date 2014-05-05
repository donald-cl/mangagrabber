import os
import sys
sys.path.insert(0, os.getcwd())

from base_notifier import SiteChecker

class ChapterInfo(object):
    def __init__(self, manga_name, chapter_title, chapter_num, href):
        self.manga_name = manga_name
        self.chapter_title = chapter_title
        self.chapter_num = chapter_num
        self.href = href

    def __str__(self):
        return self.href + self.chapter_title + self.chapter_num

class UpdateInfo(object):
    def __init__(self, manga_name, new_chapters):
        self.manga_name = manga_name
        self.new_chapters = new_chapters

    def __str__(self):
        info_str = self.manga_name
        for chapter in self.new_chapters:
            info_str += str(chapter)

        return info_str

class MangaFoxChecker(SiteChecker):
    def __init__(self, manga_watchlist, sitename="mangafox", homepage='http://mangafox.me/releases/'):
        SiteChecker.__init__(self, manga_watchlist, sitename, homepage)

    def scrape_updates(self):
        parsed_html = self.parse_page()
        update_list = parsed_html.find('ul', attrs={'id':'updates'})
        list_items = update_list.findAll('li')
        item_divs = [ item.find('div') for item in list_items ]

        all_updates = ''

        for item in item_divs:

            all_chapters = item.findAll('dt', recursive=True)

            for chapter in all_chapters:
                is_new = chapter.find('em')
                if is_new.text == 'Today':

                    header = item.find('h3', attrs={'class':'title'})
                    main_anchor = header.find('a')
                    manga_name = main_anchor.text

                    chapter_spans = chapter.findAll('span', attrs={'class':'chapter nowrap'})
                    chapter_infos = []

                    for span in chapter_spans:
                        anchor = span.find('a')
                        href = anchor['href']
                        info = anchor.text.split(' ')
                        chapter_title = info[0]
                        chapter_num = info[1]

                        ci = ChapterInfo(manga_name, chapter_title, chapter_num, href)
                        chapter_infos.append(ci)

                    ui = UpdateInfo(manga_name, chapter_infos)

            if len(self.manga_watchlist) == 0 or manga_name in self.manga_watchlist:
                if self.debug:
                    print str(ui)
                all_updates += str(ui)

        return all_updates

def main():
    #my_watchlist = ['bleach', 'naruto', 'one piece']
    my_watchlist = []
    ms = MangaFoxChecker(my_watchlist)
    ms.debug = True
    ms.get_updates()

if __name__ == '__main__':
    main()
