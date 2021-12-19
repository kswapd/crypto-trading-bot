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
import conf
import urllib.request
import json
import sys
import hmac
import hashlib
from urllib.request import urlretrieve
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
        self.account_base_url = 'https://api.binance.com/api/v3/account'
        self.send_headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.9,zh;q=0.8,zh-CN;q=0.7',
            'cookie': 'bnc-uuid=9cb5372f-b0fd-48ee-b7a8-521664a72f98; __BINANCE_USER_DEVICE_ID__={"a8a288ba27ecd5cb76395b0f870d37a1":{"date":1613791577084,"value":"1613791576722Gnx7kPrDOW49AuRXr0T"}}; userPreferredCurrency=USD_USD; _ga=GA1.2.303310618.1637422988; source=referral; campaign=www.binance.com; theme=light; _gid=GA1.2.1555737304.1639897837; BNC_FV_KEY=310c8d25f3a0a48585a582f244778ec80f9a18de; BNC_FV_KEY_EXPIRE=1639984362225; gtId=cfa43601-224e-487d-b854-079a6f61b0f4; cr00=A266C00E73472CBC91968E97E2A74B60; d1og=web.23985229.442E5B30A1404A0F1F75A0A958ADA36A; r2o1=web.23985229.0CCD5B8C549B770AD83A999B78D81D86; f30l=web.23985229.4CCA3F9F69293F38FE8246CB8F3A5494; logined=y; fiat-prefer-currency=USD; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2223985229%22%2C%22first_id%22%3A%2217d3e040491254-082a35d5a53cc5-1c306851-1296000-17d3e040492abd%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E8%87%AA%E7%84%B6%E6%90%9C%E7%B4%A2%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC%22%2C%22%24latest_referrer%22%3A%22https%3A%2F%2Fwww.google.com%2F%22%7D%2C%22%24device_id%22%3A%2217d3e040491254-082a35d5a53cc5-1c306851-1296000-17d3e040492abd%22%7D; lang=en',
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

        keys_conf = conf.TradeKeys()
        self.cur_balances = {}
        self.open_orders = {}
        self.apikey = keys_conf.keys_info['binance']['public']
        self.secret = keys_conf.keys_info['binance']['secret']

    def stop(self):
        self.is_stop = True
        print('stopped')
    def get_balance(self):
        #self.send_headers['Sign'] = mysign
        self.send_headers = {}
        self.send_headers['X-MBX-APIKEY'] = self.apikey
        self.cur_balances = {}
        myreq = {}
        myreq['timestamp'] = int(time.time()*1000)
        post_data = urllib.parse.urlencode(myreq, encoding='utf-8')

        mysign = hmac.new(self.secret.encode('utf-8'), post_data.encode('utf-8'),
                          hashlib.sha256).hexdigest()
        myreq['signature'] = mysign

        post_data = urllib.parse.urlencode(myreq, encoding='utf-8')

        finalReq = self.account_base_url + '?' + post_data
        print('Request url:', finalReq)
        #req = urllib.request.Request(
            #self.account_base_url, post_data.encode('utf-8'), headers=self.send_headers, method="GET")
        """
        req = urllib.request.Request(
            finalReq, headers=self.send_headers, method="GET")
        req.set_proxy('127.0.0.1:8001', 'http')
        req.set_proxy('127.0.0.1:8001', 'https')
        res = urllib.request.urlopen(url=req, timeout=5000)
        page = res.read()
        json_obj = json.loads(page)

        """
        response = session.get(finalReq, headers=self.send_headers)
        json_obj = json.loads(response.content)




        for m in json_obj['balances']:
            if float(m['free']) > 0.0001:
                self.cur_balances[m['asset']] = float(m['free'])

        print('Get balances:'+'{:}'.format(self.cur_balances))
        
    def list_price(self):
        print("Getting cryptocurrency info from url:", self.base_url)
        while not self.is_stop:
            # response = session.get(
            #    ticker_url, headers=self.send_headers, proxies=proxyDict2)
            #response = session.get(self.base_url, headers=self.send_headers)
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
        #binance.list_price()
        binance.get_balance()
    except KeyboardInterrupt as e:
        binance.stop()
