#! /usr/bin/python
# -*-coding:utf-8-*-
import json
import sys
import time
import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
session = requests.Session()
proxyDict = {
    'http': 'socks5://127.0.0.1:1081',
    'https': 'socks5://127.0.0.1:1081'
}
proxyDict2 = {
    'http': 'http://127.0.0.1:8001',
    'https': 'https://127.0.0.1:8001'
}
session.proxies.update(proxyDict2)
retry = Retry(connect=3, backoff_factor=0.5)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)


class coinmarket_bot():
    def __init__(self, x=0, y=0, width=80, height=15, is_view=True):
        self.is_stop = False
        self.num = 50
        self.pos_y = 2
        self.targetSymbol = ('BTC', 'ETH', 'XRP', 'BCH',
                             'LTC',  'DASH', 'USDT', 'DOGE')
        #self.coin_url = "https://pro-api.coinmarketcap.com/v1/ticker/?limit=%d"%self.num
        self.base_url = "https://coinmarketcap.com/"

    def stop(self):
        self.is_stop = True
        print('stopped')

    def list_price(self):
        print("Getting cryptocurrency info from url:", self.base_url)

        while not self.is_stop:
            cur_pos_x = 2
            headers = {
                'Accepts': 'application/json',
                'X-CMC_PRO_API_KEY': 'b22f9e6d-6c09-431d-ac9a-fd87131fc9a5',
            }
            #content = requests.get(self.coin_url).content
            content = session.get(self.base_url).content
            goods_title_imgs = []
            goods_detail_imgs = []
            soup = BeautifulSoup(content, "html.parser")
            coin_table = soup.find('table', class_='cmc-table')
            tb = coin_table.find('tbody')
            # print(soup)
            trs = tb.find_all('tr')
            print("List time:", time.strftime(
                "%Y-%m-%d %H:%M:%S", time.localtime()))
            for tr in trs[0:10]:
                # print(len(trs))
                # print(tr.get_text())
                all_td = tr.find_all('td')
                coin_seq = all_td[1].find('p').get_text()
                coin_name = all_td[2].find(
                    'div', class_='sc-16r8icm-0').find('p').get_text()
                coin_name_simp = all_td[2].find(
                    'div', class_='sc-1teo54s-2').find('p').get_text()
                coin_price = all_td[3].get_text()
                coin_price_change_24h = all_td[4].get_text()
                coin_price_change_7d = all_td[5].get_text()
                coin_market_cap = all_td[6].get_text()
                coin_volume = all_td[7].get_text()
                coin_image = all_td[9].find('img').get('src')
                print(coin_seq, coin_name, coin_name_simp, coin_price, coin_price_change_24h, coin_price_change_7d,
                      coin_market_cap, coin_volume)

                # return
            time.sleep(10)


if __name__ == "__main__":
    coinmarket_bot = coinmarket_bot()
    try:
        coinmarket_bot.list_price()
    except KeyboardInterrupt as e:
        coinmarket_bot.stop()
