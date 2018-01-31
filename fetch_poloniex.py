#! /usr/bin/python
#-*-coding:utf-8-*- 
import urllib,urllib2
import json
import sys, time
import curses
import hmac,hashlib
import conf
import console_view as cv
import logging
class fetch_poloniex(cv.console_view):
    def __init__(self, x = 0, y = 16, width = 80, height = 15, is_view = True):
        cv.console_view.__init__(self, x, y, width, height, is_view)
        self.is_stop = False
        self.num = 50
        self.pos_y = 2
        self.target_symbol = ('USDT_BTC','USDT_LTC','USDT_BCH','USDT_ETH','USDT_XRP', 'USDT_DASH',  'BTC_DOGE')
        self.method = ('depth','ticker','trades', 'info')
        self.trade_list = ('ltc_usd', 'btc_usd', 'eth_usd', 'bcc_usd', 'dash_usd', 'doge_usd') 
        #self.coin_url = "https://api.coinmarketcap.com/v1/ticker/?limit=%d"%self.num
        self.base_url = 'https://poloniex.com/public?command=returnTicker'
        self.order_book_url = 'https://poloniex.com/public?command=returnOrderBook&&currencyPair=all&depth=1'
        self.send_headers = {
 'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
 'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:55.0) Gecko/20100101 Firefox/55.0',
 'Cookie':'__cfduid=d92eb21c1dd0e150a8e730ef1e8780fd61516264900; cf_clearance=e61fba35a2c2bdc9cd35af99cb5ca9112244f353-1516613184-1800'
} 
        #keys_conf = conf.TradeKeys()
        #self.apikey = keys_conf.keys_info['poloniex']['public']
        #self.secret = keys_conf.keys_info['poloniex']['secret']
        self.apikey = 'aaa'
        self.secret = 'bbb'
        #self.display_pos = {'x':0, 'y':16, 'width':80, 'height':15}
	#print(self.secret)
	#print(self.apikey)
        self.monitor_info = {
                'time':time.time(),
                'BTC':{'last':{'price':-1, 'num':-1}, 'bid':{'price':-1, 'num':-1}, 'ask':{'price':-1, 'num':-1}, 'change':-1, 'isFrozen':-1},
                'LTC':{'last':{'price':-1, 'num':-1}, 'bid':{'price':-1, 'num':-1}, 'ask':{'price':-1, 'num':-1}, 'change':-1, 'isFrozen':-1},
                'ETH':{'last':{'price':-1, 'num':-1}, 'bid':{'price':-1, 'num':-1}, 'ask':{'price':-1, 'num':-1}, 'change':-1, 'isFrozen':-1},
                'XRP':{'last':{'price':-1, 'num':-1}, 'bid':{'price':-1, 'num':-1}, 'ask':{'price':-1, 'num':-1}, 'change':-1, 'isFrozen':-1},
                'DASH':{'last':{'price':-1, 'num':-1}, 'bid':{'price':-1, 'num':-1}, 'ask':{'price':-1, 'num':-1}, 'change':-1,'isFrozen':-1},
                'DOGE':{'last':{'price':-1, 'num':-1}, 'bid':{'price':-1, 'num':-1}, 'ask':{'price':-1, 'num':-1}, 'change':-1,'isFrozen':-1}
            }
        self.symbol_info_pair = {'USDT_BTC':'BTC','USDT_LTC':'LTC','USDT_ETH':'ETH','USDT_XRP':'XRP', 'BTC_DOGE':'DOGE', 'USDT_DASH':'DASH'}
	
    def stop(self):
        self.is_stop = True
        print('stopped')
    def get_ticker(self):
        ticker_url = self.base_url
            #myreq  = {}
            #myreq['command'] = 'returnTicker' 
            #myreq['nonce'] = int(time.time()*1000)
            #post_data = urllib.urlencode(myreq)

            #mysign = hmac.new(self.secret, post_data, hashlib.sha512).hexdigest()
            #self.send_headers['Sign'] = mysign
            #elf.send_headers['Key'] = self.apikey
            #    'Sign': mysign,
            #    'Key': self.apikey
            #}
        req = urllib2.Request(ticker_url, headers=self.send_headers)
        try:
            res = urllib2.urlopen(req,timeout=5)
            page = res.read()
            json_obj = json.loads(page)
            self.monitor_info['time'] = time.time()
            for pair in self.target_symbol:
                if self.symbol_info_pair.has_key(pair):
                    self.monitor_info[self.symbol_info_pair[pair]]['last']['price'] = float(json_obj[pair]['last'])
                    self.monitor_info[self.symbol_info_pair[pair]]['bid']['price'] = float(json_obj[pair]['highestBid'])
                    self.monitor_info[self.symbol_info_pair[pair]]['ask']['price'] = float(json_obj[pair]['lowestAsk'])
                    self.monitor_info[self.symbol_info_pair[pair]]['change'] = float(json_obj[pair]['percentChange'])
        except Exception,e:
            err = 'Get poloniex ticker error'
            logging.info(err)
            time.sleep(1)
    def get_order_book(self):
        ticker_url = self.order_book_url
        req = urllib2.Request(ticker_url, headers=self.send_headers)
        try:
            res = urllib2.urlopen(req,timeout=5)
            page = res.read()
            json_obj = json.loads(page)
            self.monitor_info['time'] = time.time()
            for pair in self.target_symbol:
                if self.symbol_info_pair.has_key(pair):
                    self.monitor_info[self.symbol_info_pair[pair]]['bid']['price'] = float(json_obj[pair]['bids'][0][0])
                    self.monitor_info[self.symbol_info_pair[pair]]['ask']['price'] = float(json_obj[pair]['asks'][0][0])
                    self.monitor_info[self.symbol_info_pair[pair]]['bid']['num'] = float(json_obj[pair]['bids'][0][1])
                    self.monitor_info[self.symbol_info_pair[pair]]['ask']['num'] = float(json_obj[pair]['asks'][0][1])
                    self.monitor_info[self.symbol_info_pair[pair]]['isFrozen'] = int(json_obj[pair]['isFrozen'])
        except Exception,e:
            err = 'Get poloniex order book error'
            logging.info(err)
            time.sleep(1)
        
    def get_open_info(self):
        while not self.is_stop:
            self.get_ticker()
            self.get_order_book()
            #print '{:}'.format(self.monitor_info)
            time.sleep(2)

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='test.log',
                    filemode='w')
    info = fetch_poloniex()
    try:
        info.get_open_info()
    except KeyboardInterrupt as e:
        info.stop()
    

    

