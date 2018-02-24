#! /usr/bin/python
#-*-coding:utf-8-*- 
import urllib,urllib2
import json
import sys, time
import curses
import logging
import console_view as cv
import conf,hmac,hashlib,base64
import request
class fetch_kraken(cv.console_view):
    def __init__(self, x = 80, y = 16, width = 80, height = 15, is_view = True):
        cv.console_view.__init__(self, x, y, width, height, is_view)
        self.is_stop = False
        self.num = 50
        self.pos_y = 2
        self.target_symbol = ('BTC','ETH','XRP', 'BCH', 'LTC',  'DASH', 'USDT', 'DOGE')
        self.method = ('depth','ticker','trades', 'info')
        self.trade_list = ('XXBTZUSD', 'XLTCZUSD', 'BCHUSD', 'XETHZUSD', 'XXRPZUSD','DASHUSD') 
        #self.coin_url = "https://api.coinmarketcap.com/v1/ticker/?limit=%d"%self.num
        self.base_url = 'https://api.kraken.com/0/public/Ticker?pair='
        self.order_book_url = 'https://api.kraken.com/0/public/Depth?count=1&pair='
        self.api_url = 'https://api.kraken.com'
        self.api_version = '0'
        self.send_headers = {
 'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
 'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
 'Connection':'keep-alive'
} 
        self.monitor_info = {
                'time':time.time(),
                'BTC':{'last':{'price':-1, 'num':-1}, 'bid':{'price':-1, 'num':-1}, 'ask':{'price':-1, 'num':-1}},
                'LTC':{'last':{'price':-1, 'num':-1}, 'bid':{'price':-1, 'num':-1}, 'ask':{'price':-1, 'num':-1}},
                'ETH':{'last':{'price':-1, 'num':-1}, 'bid':{'price':-1, 'num':-1}, 'ask':{'price':-1, 'num':-1}},
                'XRP':{'last':{'price':-1, 'num':-1}, 'bid':{'price':-1, 'num':-1}, 'ask':{'price':-1, 'num':-1}},
                'DASH':{'last':{'price':-1, 'num':-1}, 'bid':{'price':-1, 'num':-1}, 'ask':{'price':-1, 'num':-1}},
                'DOGE':{'last':{'price':-1, 'num':-1}, 'bid':{'price':-1, 'num':-1}, 'ask':{'price':-1, 'num':-1}}
            }
        self.symbol_info_pair = {'XXBTZUSD':'BTC','XLTCZUSD':'LTC','XETHZUSD':'ETH','XXRPZUSD':'XRP', 'DASHUSD':'DASH'}
        self.symbol_info_pair_inv = {}
        for key,val in self.symbol_info_pair.items():
            self.symbol_info_pair_inv[val] = key   

        keys_conf = conf.TradeKeys()
        self.cur_balances = {}
        self.apikey = keys_conf.keys_info['kraken']['public']
        self.secret = keys_conf.keys_info['kraken']['secret']
    
    def stop(self):
        self.is_stop = True
        print('stopped')

    
    def get_balance(self):
        self.cur_balances = {}
        self.send_headers = {}
        url_path = '/' + self.api_version + '/private/'+'Balance'
        req_url = self.api_url + url_path

        myreq  = {}
        myreq['nonce'] = int(time.time()*1000)
        post_data = urllib.urlencode(myreq)
        
        message = url_path + hashlib.sha256(str(myreq['nonce']) +
                                           post_data).digest()
        signature = hmac.new(base64.b64decode(self.secret),
                             message, hashlib.sha512)
        self.send_headers['API-Key'] = self.apikey
        self.send_headers['API-Sign'] = base64.b64encode(signature.digest())
        
        #print('{:}'.format(self.send_headers)) 
        req = urllib2.Request(req_url,post_data, headers=self.send_headers)
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
            print('{:}'.format(json_obj))  
            for (k,v) in json_obj['result'].items():
                if float(v)>0.000001:
                    print (k,v)
                    self.cur_balances[k] = float(v)
        except Exception,e:
            err = 'Get kraken balance error'
            print e
            logging.info(err)
            time.sleep(1)

        logging.info('get balances:'+'{:}'.format(self.cur_balances))

    def buy(self, symbol, price, num):
        law_coin = {'USDT':'ZUSD'}
        url_path = '/' + self.api_version + '/private/'+'AddOrder'
        req_url = self.api_url + url_path
        logging.info('start buy:%s,%.2f,%.5f'%(symbol, price, num))
        self.get_balance()
        if(not self.cur_balances.has_key(law_coin['USDT'])):
            logging.info('not have money usdt, return')
            return
        to_buy_num = num
        #if self.cur_balances[law_coin['USDT']] <  to_buy_num*price:
         #   to_buy_num = self.cur_balances[law_coin['USDT']]/(price)
        #    logging.info('not have enough money:%.2f,change buy amount %.2f-->%.2f', self.cur_balances[law_coin['USDT']], num, to_buy_num)
        if to_buy_num*price < 1:
            logging.info('total must > 1, drop this order')
            return
        logging.info('buy amount:%.5f'%to_buy_num)

        self.send_headers = {}
        myreq  = {}
        myreq['pair'] = self.symbol_info_pair_inv[symbol]
        myreq['type'] = 'buy' 
        myreq['ordertype'] = 'limit' 
        myreq['price'] = price
        myreq['volume'] = to_buy_num
        
        myreq['nonce'] = int(time.time()*1000)

        post_data = urllib.urlencode(myreq)
        
        message = url_path + hashlib.sha256(str(myreq['nonce']) +
                                           post_data).digest()
        signature = hmac.new(base64.b64decode(self.secret),
                             message, hashlib.sha512)
        self.send_headers['API-Key'] = self.apikey
        self.send_headers['API-Sign'] = base64.b64encode(signature.digest())

        
        #req = urllib2.Request(self.trade_base_url,post_data, headers=self.send_headers)
        try:
            #res = urllib2.urlopen(req,timeout=5)
            #page = res.read()
            #json_obj = json.loads(page)

            ret = requests.post(req_url, data=myreq, headers=self.send_headers)
            json_obj = json.loads(ret.text)
            logging.info('buy success'+'{:}'.format(json_obj))
        except Exception,e:
            err = 'buy at kraken error'
            logging.info(err)
            logging.info(e)
            time.sleep(1)

    def sell(self, symbol, price, num):
        logging.info('start sell:%s,%.2f,%.5f'%(symbol, price, num))
   
        url_path = '/' + self.api_version + '/private/'+'AddOrder'
        req_url = self.api_url + url_path
        
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
        myreq['pair'] = self.symbol_info_pair_inv[symbol]
        myreq['type'] = 'sell' 
        myreq['ordertype'] = 'limit' 
        myreq['price'] = price
        myreq['volume'] = to_sell_num
        
        myreq['nonce'] = int(time.time()*1000)

        post_data = urllib.urlencode(myreq)
        
        message = url_path + hashlib.sha256(str(myreq['nonce']) +
                                           post_data).digest()
        signature = hmac.new(base64.b64decode(self.secret),
                             message, hashlib.sha512)
        self.send_headers['API-Key'] = self.apikey
        self.send_headers['API-Sign'] = base64.b64encode(signature.digest())

        
        #req = urllib2.Request(self.trade_base_url,post_data, headers=self.send_headers)
        try:
            #res = urllib2.urlopen(req,timeout=5)
            #page = res.read()
            #json_obj = json.loads(page)

            ret = requests.post(req_url, data=myreq, headers=self.send_headers)
            json_obj = json.loads(ret.text)
            logging.info('buy success'+'{:}'.format(json_obj))
        except Exception,e:
            err = 'buy at kraken error'
            logging.info(err)
            logging.info(e)
            time.sleep(1)
    def get_open_info(self):
        while not self.is_stop:
            #self.get_ticker()
            self.get_order_book()
            time.sleep(2)
    def get_ticker(self):
        ticker_url = self.base_url+','.join(self.trade_list)
        req = urllib2.Request(ticker_url, headers=self.send_headers)
        try:
            res = urllib2.urlopen(req,timeout=5)
            page = res.read()
            json_obj_all = json.loads(page)
            json_obj = json_obj_all['result']
            self.monitor_info['time'] = time.time()
            for pair in self.trade_list:
                if self.symbol_info_pair.has_key(pair):
                    self.monitor_info[self.symbol_info_pair[pair]]['last']['price'] = float(json_obj[pair]['c'][0])
                    self.monitor_info[self.symbol_info_pair[pair]]['bid']['price'] = float(json_obj[pair]['b'][0])
                    self.monitor_info[self.symbol_info_pair[pair]]['ask']['price'] = float(json_obj[pair]['a'][0])
        except Exception,e:
            err = 'Get kraken ticker error.' 
            logging.info(err)
            time.sleep(1)
    def get_order_book(self):
        for stock in self.trade_list:
            ticker_url = self.order_book_url+stock
            req = urllib2.Request(ticker_url, headers=self.send_headers)
            try:
                res = urllib2.urlopen(req,timeout=5)
                page = res.read()
                json_obj_all = json.loads(page)
                json_obj = json_obj_all['result']
                self.monitor_info['time'] = time.time()
                pair = stock
                if self.symbol_info_pair.has_key(pair):
                    self.monitor_info[self.symbol_info_pair[pair]]['bid']['price'] = float(json_obj[pair]['bids'][0][0])
                    self.monitor_info[self.symbol_info_pair[pair]]['ask']['price'] = float(json_obj[pair]['asks'][0][0])
                    self.monitor_info[self.symbol_info_pair[pair]]['bid']['num'] = float(json_obj[pair]['bids'][0][1])
                    self.monitor_info[self.symbol_info_pair[pair]]['ask']['num'] = float(json_obj[pair]['asks'][0][1])

            except Exception,e:
                err = 'Get kraken order book error.' 
                logging.info(err)
                time.sleep(1)
if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='test.log',
                    filemode='w')
    info = fetch_kraken()
    try:
        #info.get_open_info()
        #info.get_balance()
        info.sell('LTC', 530.0, 0.1)
        #info.buy('XRP', 0.75, 1.5)
    except KeyboardInterrupt as e:
        info.stop()
    

    

