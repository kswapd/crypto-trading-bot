import urllib2
class fetch_url:
    def __init__(self):
        print 'init'
    def start(self):
        req = urllib2.Request('http://www.baidu.com')
        res = urllib2.urlopen(req)
        page = res.read()
        print page

