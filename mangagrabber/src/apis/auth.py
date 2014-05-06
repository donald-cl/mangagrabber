import urllib2, base64
import requests
import random

def basic_http_auth(url, username, password):
    request = urllib2.Request(url)
    base64string = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
    request.add_header("Authorization", "Basic %s" % base64string)
    result = urllib2.urlopen(request)
    return result.read()

def basic_http_auth2(url, username, password, cookie=None):
    base64string = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
    headers = { "Authorization" : "Basic %s" % base64string }

    if cookie is None:
        cookie = random.random()

    cookies = dict(cookies_are=str(cookie))
    r = requests.get(url, headers=headers, cookies=cookies)
    return r.content

if __name__ == '__main__':
    pass
