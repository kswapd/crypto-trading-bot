import urllib.request
class fetch_url:
    def __init__(self):
        print('init')
    def start(self):
        req = urllib.request.Request('http://www.baidu.com')
        res = urllib.request.urlopen(req)
        page = res.read()
        print(page)

