#! /usr/bin/python
# -*-coding:utf-8-*-
# import urllib.request

import json
import sys
import time
import logging
import requests
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


class binance_bot():
    def __init__(self):
        self.is_stop = False
        self.num = 50
        self.view_mode = 'complete'
        self.method = ('depth', 'ticker', 'trades', 'info')
        self.trade_list = ('BTCUSDT', 'LTCUSDT', 'ETHUSDT',
                           'XRPUSDT', 'LTCDOWNUSDT')
        # self.coin_url = "https://api.coinmarketcap.com/v1/ticker/?limit=%d"%self.num
        self.base_url = 'https://api.binance.com/api/v3/ticker/price'
        self.send_headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.9,zh;q=0.8,zh-CN;q=0.7',
            'cookie': 'bnc-uuid=9cb5372f-b0fd-48ee-b7a8-521664a72f98; __BINANCE_USER_DEVICE_ID__={"a8a288ba27ecd5cb76395b0f870d37a1":{"date":1613791577084,"value":"1613791576722Gnx7kPrDOW49AuRXr0T"}}; userPreferredCurrency=USD_USD; _ga=GA1.2.303310618.1637422988; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2217d3e040491254-082a35d5a53cc5-1c306851-1296000-17d3e040492abd%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22%24device_id%22%3A%2217d3e040491254-082a35d5a53cc5-1c306851-1296000-17d3e040492abd%22%7D; fiat-prefer-currency=EUR; source=referral; campaign=www.binance.com; BNC_FV_KEY_EXPIRE=1638497486704',
            'sec-ch-ua': '"Google Chrome";v="95", "Chromium";v="95", ";Not A Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'
        }
        self.monitor_info = {}

    def stop(self):
        self.is_stop = True
        print('stopped')

    def list_price(self):
        print("Getting cryptocurrency info from url:", self.base_url)
        while not self.is_stop:
            # response = session.get(
            #    ticker_url, headers=self.send_headers, proxies=proxyDict2)
            response = session.get(self.base_url)
            json_obj = json.loads(response.content)
            self.monitor_info['time'] = time.strftime(
                "%Y-%m-%d %H:%M:%S", time.localtime())
            print("List time:", self.monitor_info['time'])
            for coin in json_obj:
                if coin['symbol'] in self.trade_list:
                    pair = coin['symbol']
                    if coin['symbol'] not in self.monitor_info:
                        self.monitor_info[coin['symbol']] = {'last': {
                            'price': -1, 'num': -1}, 'bid': {'price': -1, 'num': -1}, 'ask': {'price': -1, 'num': -1}}
                    self.monitor_info[coin['symbol']]['last']['price'] = float(
                        coin['price'])
                    self.monitor_info[coin['symbol']]['bid']['price'] = float(
                        coin['price'])
                    self.monitor_info[coin['symbol']]['ask']['price'] = float(
                        coin['price'])
                    print_content = "%7s \t%7.2f \t%7.2f \t%7.2f" % (pair, float(
                        coin['price']), float(coin['price']), float(coin['price']))
                    print(print_content)
            time.sleep(2)


if __name__ == "__main__":
    binance = binance_bot()
    try:
        binance.list_price()
    except KeyboardInterrupt as e:
        binance.stop()
