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
import requests
class fetch_poloniex(cv.console_view):
    def __init__(self, x = 0, y = 16, width = 80, height = 15, is_view = True):
        cv.console_view.__init__(self, x, y, width, height, is_view)
        self.is_stop = False
        self.num = 50
        self.pos_y = 2
        self.fee_rate = 0.0025
        self.target_symbol = ('USDT_BTC','USDT_LTC','USDT_BCH','USDT_ETH','USDT_XRP', 'USDT_DASH',  'BTC_DOGE')
        self.method = ('depth','ticker','trades', 'info')
        self.trade_list = ('ltc_usd', 'btc_usd', 'eth_usd', 'bcc_usd', 'dash_usd', 'doge_usd') 
        #self.coin_url = "https://api.coinmarketcap.com/v1/ticker/?limit=%d"%self.num
        self.base_url = 'https://poloniex.com/public?command=returnTicker'
        self.trade_base_url ='https://poloniex.com/tradingApi'
        self.order_book_url = 'https://poloniex.com/public?command=returnOrderBook&&currencyPair=all&depth=1'
        self.send_headers = {
 'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
 'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:55.0) Gecko/20100101 Firefox/55.0',
 'Cookie':'__cfduid=d92eb21c1dd0e150a8e730ef1e8780fd61516264900; cf_clearance=e61fba35a2c2bdc9cd35af99cb5ca9112244f353-1516613184-1800'
} 
        keys_conf = conf.TradeKeys()
        self.cur_balances = {}
        self.apikey = keys_conf.keys_info['poloniex']['public']
        self.secret = keys_conf.keys_info['poloniex']['secret']
        ##self.apikey = 'aaa'
        #self.secret = 'bbb'
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
        self.symbol_info_pair_inv = {}
        for key,val in self.symbol_info_pair.items():
            self.symbol_info_pair_inv[val] = key
    def stop(self):
        self.is_stop = True
        print('stopped')
    def sell(self, symbol, price, num):
        logging.info('start sell:%s,%.2f,%.5f'%(symbol, price, num))
        self.get_balance()
        if(not self.cur_balances.has_key(symbol)):
            logging.info('not get this symbol:%s, return'%symbol)
            return
        to_sell_num = num
        if self.cur_balances[symbol] <  to_sell_num:
            to_sell_num = self.cur_balances[symbol]
        if to_sell_num*price < 1:
            logging.info('total must > 1, drop this order')
            return
        logging.info('selling num:%.5f'%to_sell_num)

        self.send_headers = {}
        myreq  = {}
        myreq['currencyPair'] = self.symbol_info_pair_inv[symbol]
        myreq['rate'] = price
        myreq['amount'] = to_sell_num
        myreq['command'] = 'sell' 
        myreq['nonce'] = int(time.time()*1000)
        post_data = urllib.urlencode(myreq)
        mysign = hmac.new(self.secret, post_data, hashlib.sha512).hexdigest()
        self.send_headers['Sign'] = mysign
        self.send_headers['Key'] = self.apikey
        req = urllib2.Request(self.trade_base_url,post_data, headers=self.send_headers)
        try:
            #res = urllib2.urlopen(req,timeout=5)
            #page = res.read()
            #json_obj = json.loads(page)

            ret = requests.post(self.trade_base_url, data=myreq, headers=self.send_headers)
            json_obj = json.loads(ret.text)
            logging.info('sell success'+'{:}'.format(json_obj))
        except Exception,e:
            err = 'sell at poloniex error'
            logging.info(err)
            logging.info(e)
            time.sleep(1)


    def buy(self, symbol, price, num):
        logging.info('start buy:%s,%.2f,%.5f'%(symbol, price, num))
        self.get_balance()
        if(not self.cur_balances.has_key('USDT')):
            logging.info('not have money usdt, return')
            return
        to_buy_num = num
        if self.cur_balances['USDT'] <  to_buy_num*price:
            to_buy_num = self.cur_balances['USDT']/(price)
            logging.info('not have enough money:%.2f,change buy amount %.2f-->%.2f', self.cur_balances['USDT'], num, to_buy_num)
        if to_buy_num*price < 1:
            logging.info('total must > 1, drop this order')
            return
        logging.info('buy amount:%.5f'%to_buy_num)

        self.send_headers = {}
        myreq  = {}
        myreq['currencyPair'] = self.symbol_info_pair_inv[symbol]
        myreq['rate'] = price
        myreq['amount'] = to_buy_num
        myreq['command'] = 'buy' 
        myreq['nonce'] = int(time.time()*1000)
        post_data = urllib.urlencode(myreq)
        mysign = hmac.new(self.secret, post_data, hashlib.sha512).hexdigest()
        self.send_headers['Sign'] = mysign
        self.send_headers['Key'] = self.apikey
        req = urllib2.Request(self.trade_base_url,post_data, headers=self.send_headers)
        try:
            #res = urllib2.urlopen(req,timeout=5)
            #page = res.read()
            #json_obj = json.loads(page)

            ret = requests.post(self.trade_base_url, data=myreq, headers=self.send_headers)
            json_obj = json.loads(ret.text)
            logging.info('buy success'+'{:}'.format(json_obj))
        except Exception,e:
            err = 'buy at poloniex error'
            logging.info(err)
            logging.info(e)
            time.sleep(1)
    def get_balance(self):
        self.cur_balances = {}
        self.send_headers = {}
        myreq  = {}
        myreq['command'] = 'returnBalances' 
        myreq['nonce'] = int(time.time()*1000)
        post_data = urllib.urlencode(myreq)
        #print (self.secret, self.apikey)
        mysign = hmac.new(self.secret, post_data, hashlib.sha512).hexdigest()
        self.send_headers['Sign'] = mysign
        self.send_headers['Key'] = self.apikey
        #print('{:}'.format(self.send_headers))	
        req = urllib2.Request(self.trade_base_url,post_data, headers=self.send_headers)
        #ret = urllib2.urlopen(urllib2.Request('https://poloniex.com/tradingApi', post_data, headers))
            #elf.send_headers['Key'] = self.apikey
            #    'Sign': mysign,
            #    'Key': self.apikey
            #}
        try:
            res = urllib2.urlopen(req,timeout=5)
            page = res.read()
            json_obj = json.loads(page)
            #print(json_obj['SDC'])	
            #print('{:}'.format(json_obj))	
            for (k,v) in json_obj.items():
                if float(v)>0.000001:
                #    print (k,v)
                    self.cur_balances[k] = float(v)
        except Exception,e:
            err = 'Get poloniex balance error'
            print e
            logging.info(err)
            time.sleep(1)

        logging.info('get balances:'+'{:}'.format(self.cur_balances))

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
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)
    info = fetch_poloniex()
    try:
        #info.get_open_info()
        info.get_balance()
        #info.sell('LTC', 130.0, 0.01)
        #info.buy('XRP', 0.75, 1.5)
    except KeyboardInterrupt as e:
        info.stop()
    

    

