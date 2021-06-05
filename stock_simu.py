#! /usr/bin/python
#-*-coding:utf-8-*- 
import urllib.request
import json
import sys, time
import curses
import console_view as cv
import requests
import _thread
from io import BytesIO
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import sched, time
import random
session = requests.Session()
retry = Retry(connect=3, backoff_factor=0.5)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)

def print_time(sc, a='default'):
    print("From print_time", time.time(), a)
    sc.enter(2, 1, print_time, (sc,a))
def print_time2(a='default'):
    print("From print_time2", time.time(), a)
#def cur_random_price(delta_value=1):

class timer_loop():
    
    def __init__(self, interval, func, *args):
        self.interval = interval
        self.func = func
        self.param = args
        self.schedule = sched.scheduler(time.time, time.sleep)
        #self.schedule.enter(self.interval, 1, self.event_func,())
        #self.schedule.run()
        self.thread = _thread.start_new_thread(self.event_func,())
        #self.event_func()
    def event_func(self):
        #print("ddddd:", self.param)
        self.func(self.param)
        self.schedule.enter(self.interval, 1, self.event_func,())
        self.schedule.run()
    def start(self):
        self.schedule.run()
    #td1 = _thread.start_new_thread( start_coin_market,('55',2) )
class stock_market():
    def __init__(self, duration=1000):
        self.is_stop = False
        self.num = 50
        self.pos_y = 2 
        self.targetSymbol = ('BTC','ETH','XRP', 'BCH', 'LTC',  'DASH', 'USDT', 'DOGE')
        self.coin_url = "https://coinmarketcap.com/"
        self.duration = duration
        self.cur_price = 10.00
        #self.schedule = sched.scheduler(time.time, time.sleep)
        #self.schedule.enter(2, 1, print_time,(self.schedule,'default'))
        #self.schedule.run()
        print("duration", self.duration)
        a = timer_loop(1, self.change_stock_price)
        b = timer_loop(3, self.print_time3)
        #a.start()
    def print_time3(self, a='default'):
        print("From print_time3", time.time(), a)
    def change_stock_price(self, delta_value=1):
        if bool(random.getrandbits(1)):
            print('ascend')
            self.cur_price = self.cur_price + 0.01
        else:
            print('descend')
            self.cur_price = self.cur_price - 0.01
        self.cur_price = round(self.cur_price,2)
        print("current price:", self.cur_price)
    def stop(self):
        self.is_stop = True
        print('stopped')  
    def start(self):
        print(self.coin_url)

        while not self.is_stop:
            pass
            continue
            cur_pos_x = 2;
            headers = {
                'Accepts': 'application/json',
                'X-CMC_PRO_API_KEY': 'b22f9e6d-6c09-431d-ac9a-fd87131fc9a5',
                }
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
            time.sleep(10)
if __name__ == "__main__":
    stock_simu = stock_market(500)
    try:
        stock_simu.start()
    except KeyboardInterrupt as e:
        stock_simu.stop()
    

    

