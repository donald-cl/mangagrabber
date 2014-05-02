from BeautifulSoup import BeautifulSoup
from os.path import expanduser
import time
import hashlib
import smtplib
import urllib2
import urllib

HOME = expanduser("~")
PROJ = "mangagrabber"

def get_mangagrabber_dir():
    path = "%s/%s/"
    return path % (HOME, PROJ)

def authenticate():
    f = open(get_mangagrabber_dir() + 'auth.txt', 'r')
    lines = f.readlines()
    lines[0] = lines[0].replace('\n', '')
    lines[1] = lines[1].replace('\n', '')

    email = lines[0]
    pw = lines[1]

    return email, pw

def send_email(email, pw, receivers, content):
    gmail_user = email
    gmail_pwd = pw
    FROM = email
    TO = receivers
    TIME = time.time()
    SUBJECT = "New manga has been released! --- " + str(TIME)

    # Prepare actual message
    message = """\From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, content)
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587) #or port 465 doesn't seem to work!
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_pwd)
        server.sendmail(FROM, TO, message)
        #server.quit()
        print 'successfully sent the mail'
    except Exception as e:
        print e
        print "failed to send mail"

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

    def get_updates(self):
        raise NotImplementedError("Abstract class Site Checker has no implementation of get_updates")

def set_cache_site_diff(sitename, all_updates):
    dirname = get_mangagrabber_dir() + "/mangagrabber/updates/" + sitename + "_updates"
    f = open(dirname, 'w')
    f.write(all_updates)
    f.close()

def get_cache_site_diff(sitename, all_updates):
    dirname = get_mangagrabber_dir() + "/mangagrabber/updates/" + sitename + "_updates"
    f = open(dirname, 'r+')
    current_content = f.read()
    f.close()
    return current_content

class MangaStreamChecker(SiteChecker):
    def __init__(self, manga_watchlist, sitename="mangastream", homepage='http://mangastream.com/'):
        SiteChecker.__init__(self, manga_watchlist, sitename, homepage)

    def get_updates(self):
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
            email, pw = authenticate()
            send_email(email, pw, ['donaldhui@gmail.com'], all_updates)
            # scrap new chapters?
        elif self.debug:
            print "no new content"

def main():
    #my_watchlist = ['bleach', 'naruto', 'one piece']
    my_watchlist = []
    ms = MangaStreamChecker(my_watchlist)
    ms.debug = True
    ms.get_updates()

if __name__ == '__main__':
    main()
