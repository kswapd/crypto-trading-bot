#! /usr/bin/python
#-*-coding:utf-8-*- 
import urllib.request
import json
import sys, time
import curses
import console_view as cv
from PIL import Image
import requests
from io import BytesIO
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
session = requests.Session()
retry = Retry(connect=3, backoff_factor=0.5)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)
class fetch_coinmarket(cv.console_view):
    def __init__(self, x = 0, y = 0, width = 80, height = 15, is_view = True):
        cv.console_view.__init__(self, x, y, width, height, is_view)
        self.is_stop = False
        self.num = 50
        self.pos_y = 2 
        self.targetSymbol = ('BTC','ETH','XRP', 'BCH', 'LTC',  'DASH', 'USDT', 'DOGE')
        #self.coin_url = "https://pro-api.coinmarketcap.com/v1/ticker/?limit=%d"%self.num
        self.coin_url = "https://coinmarketcap.com/"
    def stop(self):
        self.is_stop = True
        print('stopped')
    def test(self):
        WIDTH = 128
        HEIGHT = 160
        img2 = Image.open('./kqy.jpeg')
        imgcoin0 = img2.resize((WIDTH, HEIGHT))
        imgResp = session.get(coin_image)
                
        imgRemote = Image.open(BytesIO(imgResp.content))
        imgRemote = imgRemote.resize((WIDTH, 30))
        imgRemoteNew = Image.new("RGB", imgRemote.size, (255, 255, 255))
        imgRemoteNew.paste(imgRemote, mask=imgRemote.split()[3]) # 3 is the alpha channel

        print(imgcoin0.mode)
        print(imgcoin0.size)
        print(imgRemote.mode)
        print(imgRemote.size)
                #imgRemote = imgRemote.convert(imgcoin0.mode)
        print(imgRemote.mode)
        imgRemote.show()
        imgcoin0.paste(imgRemoteNew, (0, 105, WIDTH, 135))
                
        imgcoin0.show()    
    def start(self):
        print(self.coin_url)

        while not self.is_stop:
            cur_pos_x = 2;
            headers = {
                'Accepts': 'application/json',
                'X-CMC_PRO_API_KEY': 'b22f9e6d-6c09-431d-ac9a-fd87131fc9a5',
                }
            #req = urllib.request.Request(url=self.coin_url, headers=headers)
            #res = urllib.request.urlopen(req)
            #page = res.read()
            #json_obj = json.loads(page)
            #print(json_obj)

            #response = requests.get(self.coin_url)
            #img = Image.open(BytesIO(response.content))
            #img.show()
            #ghost = Ghost(wait_timeout=4)
            #ghost.open(self.coin_url)
            #ghost.capture_to('screen_shot.png')
            #DRIVER = 'chromedriver'
            #driver = webdriver.Chrome(DRIVER)
            #driver.get(self.coin_url)
            #screenshot = driver.save_screenshot('my_screenshot.png')
            #driver.quit()
            content = requests.get(self.coin_url).content
            goods_title_imgs = []
            goods_detail_imgs = []
            soup = BeautifulSoup(content,"html.parser") 
            coin_table = soup.find('table', class_='cmc-table')
            tb = coin_table.find('tbody')
            
            trs = tb.find_all('tr')
            for tr in trs[0:10]:
                #print(len(trs))
                #print(tr.get_text())
                all_td = tr.find_all('td')
                coin_seq = all_td[1].find('p').get_text()
                coin_name = all_td[2].find('div', class_='sc-16r8icm-0').find('p').get_text()
                coin_name_simp = all_td[2].find('div', class_='sc-1teo54s-2').find('p').get_text()
                coin_price = all_td[3].get_text()
                coin_price_change_24h = all_td[4].get_text()
                coin_price_change_7d = all_td[5].get_text()
                coin_market_cap = all_td[6].get_text()
                coin_volume = all_td[7].get_text()
                coin_image = all_td[9].find('img').get('src')
                print(coin_seq,coin_name,coin_name_simp,coin_price,coin_price_change_24h,coin_price_change_7d,
                coin_market_cap,coin_volume,coin_image)
                
                #return 
            time.sleep(10)
if __name__ == "__main__":
    #curses.initscr()
    coin_market = fetch_coinmarket()
    try:
        coin_market.start()
    except KeyboardInterrupt as e:
        coin_market.stop()
    

    

