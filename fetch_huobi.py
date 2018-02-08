#! /usr/bin/python
#-*-coding:utf-8-*- 
import urllib,urllib2
import json
import sys, time
import curses
import hmac,hashlib,base64
import conf
import console_view as cv
import logging
import requests
import datetime
import collections
class fetch_huobi(cv.console_view):
    def __init__(self, x = 0, y = 16, width = 80, height = 15, is_view = True):
        cv.console_view.__init__(self, x, y, width, height, is_view)
        self.is_stop = False
        self.num = 50
        self.pos_y = 2
        self.target_symbol = ['ltcusdt']
        #self.coin_url = "https://api.coinmarketcap.com/v1/ticker/?limit=%d"%self.num
        self.base_url_inner = 'https://api.huobipro.com'
        self.base_url_outer = 'https://api.huobi.pro'
        self.base_url = self.base_url_inner
        self.trade_base_url ='https://poloniex.com/tradingApi'
        self.order_book_url = 'https://poloniex.com/public?command=returnOrderBook&&currencyPair=all&depth=1'
        self.send_headers = {
'Content-Type':'application/x-www-form-urlencoded',
 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36',
 'Cookie':'__cfduid=d92eb21c1dd0e150a8e730ef1e8780fd61516264900; cf_clearance=e61fba35a2c2bdc9cd35af99cb5ca9112244f353-1516613184-1800'
} 
        keys_conf = conf.TradeKeys()
        self.cur_balances = {}
        self.apikey = keys_conf.keys_info['huobi']['public']
        self.secret = keys_conf.keys_info['huobi']['secret']
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
        self.symbol_info_pair = {'btcusdt':'BTC','ltcusdt':'LTC','USDT_ETH':'ETH','USDT_XRP':'XRP', 'BTC_DOGE':'DOGE', 'USDT_DASH':'DASH'}
        self.trade_info_pair = {'btcusdt':'btc','ltcusdt':'ltc','xrpusdt':'xrp'}

        self.trade_info_pair_inv = {}
        for key,val in self.trade_info_pair.items():
            self.trade_info_pair_inv[val] = key
    

    def stop(self):
        self.is_stop = True
        print('stopped')


    def sell(self, symbol, price, num):
        logging.info('start sell:%s,%.2f,%.5f'%(symbol, price, num))
        self.get_balance()
        sub_path = '/v1/order/orders/place'
        self.send_headers = {
        'Accept': 'application/json',
        'Content-Type':'application/json',
        'User-Agent': 'Chrome/39.0.2171.71',
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0'
}
        msg = collections.OrderedDict()

        msg['AccessKeyId'] = self.apikey
        msg['SignatureMethod'] = 'HmacSHA256'
        msg['SignatureVersion'] = '2'
        msg['Timestamp'] = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")

        msg_Method = 'POST\n'
        msg_Url = self.base_url[8:]+'\n'
        msg_Path = sub_path + '\n'
        message_head = msg_Method+msg_Url+msg_Path


        message_param = urllib.urlencode(msg)

        message_all = message_head + message_param
        print(message_all)
        self.sell_url = self.base_url  +  sub_path
        #self.send_headers = {}
        self.send_headers = {
        'Accept': 'application/json'
        
        }
        signature = base64.b64encode(hmac.new(self.secret, message_all, digestmod=hashlib.sha256).digest())
        signature = signature.decode()
        
        req_url = self.sell_url + '?' + 'AccessKeyId='+msg['AccessKeyId']+'&SignatureMethod='+msg['SignatureMethod']+'&SignatureVersion='+ \
        msg['SignatureVersion']+'&Timestamp='+urllib.quote(msg['Timestamp'])+'&Signature='+urllib.quote(signature)
        #req_url = self.balance_url + '?' + 'Signature='+urllib.quote(signature)
        print(req_url)

        if(not self.cur_balances.has_key(symbol)):
            logging.info('not get this symbol:%s, return'%symbol)
            return
        to_sell_num = num
        if self.cur_balances[symbol] <  to_sell_num:
            to_sell_num = self.cur_balances[symbol]
        
        #if to_sell_num*price < 1:
         #   logging.info('total must > 1, drop this order')
         #   return
        logging.info('selling num:%.5f'%to_sell_num)


        post_data  = {}
        post_data['account-id'] = '991115'
        post_data['amount'] = to_sell_num
        post_data['price'] = price
        post_data['source'] = 'api' 
        post_data['symbol'] = self.trade_info_pair_inv[symbol] #ltcusdt
        post_data['type'] = 'sell-limit'

        post_data_enc = urllib.urlencode(post_data)

        #req = urllib2.Request(req_url, post_data_enc)

        try:
            ret = requests.post(req_url, data=post_data, headers=self.send_headers)
            json_obj = json.loads(ret.text)
            #res = urllib2.urlopen(req, timeout=5)
            #page = res.read()
            #json_obj = json.loads(page)
            logging.info('sell success'+'{:}'.format(json_obj))
         
        except Exception,e:
            err = 'sell at huobi error'
            logging.info(err)
            logging.info(e)
            time.sleep(1)
    def sell2(self, symbol, price, num):
        logging.info('start sell:%s,%.2f,%.5f'%(symbol, price, num))
        self.get_balance()
        if(not self.cur_balances.has_key(symbol)):
            logging.info('not get this symbol:%s, return'%symbol)
            return
        to_sell_num = num
        if self.cur_balances[symbol] <  to_sell_num:
            to_sell_num = self.cur_balances[symbol]
        if to_sell_num > 0.12:
            to_sell_num = 0.12
        if to_sell_num < 0.01:
            to_sell_num = 0.01
        logging.info('selling num:%.5f'%to_sell_num)

        self.send_headers = {}

        myreq  = {}
        myreq['currencyPair'] = 'USDT_LTC'
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
            res = urllib2.urlopen(req,timeout=5)
            page = res.read()
            json_obj = json.loads(page)

            #ret = requests.post(self.trade_base_url, data=myreq, headers=self.send_headers)
            #json_obj = json.loads(ret.text)
            logging.info('sell success'+'{:}'.format(json_obj))
        except Exception,e:
            err = 'sell at poloniex error'
            logging.info(err)
            logging.info(e)
            time.sleep(1)
    def get_balance(self):
        sub_path = '/v1/account/accounts/991115/balance'
        msg = collections.OrderedDict()
        msg['AccessKeyId'] = self.apikey
        msg['SignatureMethod'] = 'HmacSHA256'
        msg['SignatureVersion'] = '2'
        utc_datetime = datetime.datetime.utcnow()
        utcmsg = utc_datetime.strftime("%Y-%m-%dT%H:%M:%S")
        msg['Timestamp'] = utcmsg#time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime())
       
        #msg['Timestamp'] = msg['Timestamp'][0:-2]+'13'
        #print(msg['Timestamp'])
        msg_Method = 'GET\n'
        msg_Url = self.base_url[8:]+'\n'
        msg_Path = sub_path + '\n'
        message_head = msg_Method+msg_Url+msg_Path
        message_param = urllib.urlencode(msg)
        #print(message_param)
        message_all = message_head + message_param

        print(message_all)
        self.balance_url = self.base_url  +  sub_path
        self.cur_balances = {}
        self.send_headers = {}
        signature = base64.b64encode(hmac.new(self.secret, message_all, digestmod=hashlib.sha256).digest())
        req_url = self.balance_url + '?' + 'AccessKeyId='+msg['AccessKeyId']+'&SignatureMethod='+msg['SignatureMethod']+'&SignatureVersion='+ \
        msg['SignatureVersion']+'&Timestamp='+urllib.quote(msg['Timestamp'])+'&Signature='+urllib.quote(signature)
        print(req_url)
        #print('{:}'.format(self.send_headers))	
        req = urllib2.Request(req_url, headers=self.send_headers)
        #ret = urllib2.urlopen(urllib2.Request('https://poloniex.com/tradingApi', post_data, headers))
            #elf.send_headers['Key'] = self.apikey
            #    'Sign': mysign,
            #    'Key': self.apikey
            #}
        try:
            res = urllib2.urlopen(req,timeout=5)
            page = res.read()
            json_obj = json.loads(page)
            #print('{:}'.format(json_obj))
            if json_obj['data'] is not None:	
                for item in json_obj['data']['list']:
                    if float(item['balance'])>0.000001 and item['type'] != 'frozen':
                        self.cur_balances[item['currency']] = float(item['balance'])
                print('{:}'.format(self.cur_balances))
            else:
                print(json_obj) 
        except Exception,e:
            err = 'Get huobi balance error'
            print err
            print e
            logging.info(err)
            logging.info(e)
            time.sleep(1)

        logging.info('get balances:'+'{:}'.format(self.cur_balances))
    def get_accounts(self):
        msg = collections.OrderedDict()
        msg['AccessKeyId'] = self.apikey
        msg['SignatureMethod'] = 'HmacSHA256'
        msg['SignatureVersion'] = '2'
        utc_datetime = datetime.datetime.utcnow()
        utcmsg = utc_datetime.strftime("%Y-%m-%dT%H:%M:%S")
        msg['Timestamp'] = utcmsg#time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime())
        print(msg['Timestamp'])
        msg_Method = 'GET\n'
        msg_Url = self.base_url[8:-1]+'\n'
        msg_Path = '/v1/account/accounts\n'
        message_head = msg_Method+msg_Url+msg_Path
        message_param = urllib.urlencode(msg)
        #print(message_param)
        message_all = message_head + message_param

        #print(message_all)
        self.balance_url = self.base_url  +  'v1/account/accounts'
        self.cur_balances = {}
        self.send_headers = {}
        signature = base64.b64encode(hmac.new(self.secret, message_all, digestmod=hashlib.sha256).digest())
        req_url = self.balance_url + '?' + 'AccessKeyId='+msg['AccessKeyId']+'&SignatureMethod='+msg['SignatureMethod']+'&SignatureVersion='+ \
        msg['SignatureVersion']+'&Timestamp='+urllib.quote(msg['Timestamp'])+'&Signature='+signature
        print(req_url)
        #print('{:}'.format(self.send_headers)) 
        req = urllib2.Request(req_url, headers=self.send_headers)
        #ret = urllib2.urlopen(urllib2.Request('https://poloniex.com/tradingApi', post_data, headers))
            #elf.send_headers['Key'] = self.apikey
            #    'Sign': mysign,
            #    'Key': self.apikey
            #}
        try:
            res = urllib2.urlopen(req,timeout=5)
            page = res.read()
            json_obj = json.loads(page)
            #print(json_obj)    
            print('{:}'.format(json_obj))  
           
        except Exception,e:
            err = 'Get huobi balance error'
            print e
            logging.info(err)
            time.sleep(1)

    def get_ticker(self):
        ticker_url = self.base_url_outer +'market/detail/merged?symbol=ltcusdt'
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
                #print pair
                if self.symbol_info_pair.has_key(pair):
                    #self.monitor_info[self.symbol_info_pair[pair]]['last']['price'] = float(json_obj[pair]['last'])
                    self.monitor_info[self.symbol_info_pair[pair]]['bid']['price'] = float(json_obj['tick']['bid'][0])
                    self.monitor_info[self.symbol_info_pair[pair]]['bid']['num'] = float(json_obj['tick']['bid'][1])
                    self.monitor_info[self.symbol_info_pair[pair]]['ask']['price'] = float(json_obj['tick']['ask'][0])
                    self.monitor_info[self.symbol_info_pair[pair]]['ask']['num'] = float(json_obj['tick']['ask'][1])
                    #self.monitor_info[self.symbol_info_pair[pair]]['change'] = float(json_obj[pair]['percentChange'])
        except Exception,e:
            err = 'Get huobi ticker error'
            logging.info(err)
            logging.info(e)
            time.sleep(1)
        
    def get_open_info(self):
        while not self.is_stop:
            self.get_ticker()
            #self.get_order_book()
            #print '{:}'.format(self.monitor_info)
            time.sleep(2)

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='test.log',
                    filemode='w')
    info = fetch_huobi()
    try:
        #info.get_open_info()
        #info.get_accounts()
        #info.get_balance()
        info.sell('xrp', 0.5, 3)
    except KeyboardInterrupt as e:
        info.stop()
    

    

