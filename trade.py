#! /usr/bin/python
import ccxt as ct
import pprint
import trade 
import time
import conf
class auto_trade:
    def prt(self,info):
        pprint.pprint(info)
    def __init__(self):
         self.k = ct.kraken()
         self.y = ct.yobit()
         self.p = ct.poloniex()
         self.coinmarket = ct.coinmarketcap()
         self.liqui = ct.bitfinex()
         print(ct.exchanges)
         print(self.k.hasFetchOHLCV, self.k.rateLimit)
         print(self.y.hasFetchOHLCV, self.y.rateLimit)
         print(self.p.hasFetchOHLCV, self.p.rateLimit)
        # print(self.coinmarket.hasFetchOHLCV, self.coinmarket.rateLimit)
         keys_conf = conf.TradeKeys()
         #print(keys_conf.keys_info)
         self.k.apiKey = keys_conf.keys_info['kraken']['public']
         self.k.secret = keys_conf.keys_info['kraken']['secret']
         #self.k.load_markets()
         print(self.k.symbols)
         #print (self.k.fetch_balance ())
         #print (self.k.fetch_orders ())
         #self.k.create_market_buy_order ('BTC/USD', 0.1)
         #print(self.k.fetch_ohlcv('LTC/USD', '1d'))
    def start(self):
        symbol = 'BTC/USD'
        all_info = {'k':{}, 'y':{}, 'liqui':{}}
        for i in range(0,10):
            r = self.liqui
            start = time.time()
            ticker = r.fetch_ticker(symbol)
            #print(i, "open:%s, bid:%s, ask:%s,cost:%s"%(ticker['open'],ticker['bid'],ticker['ask'], time.time()-start))
            all_info['k']['bid'] = ticker['bid']


            r = self.y
            start = time.time()
            ticker = r.fetch_ticker(symbol)
            #print(i, "open:%s, bid:%s, ask:%s,cost:%s"%(ticker['open'],ticker['bid'],ticker['ask'], time.time()-start))
            all_info['y']['bid'] = ticker['bid']


            r = self.liqui
            start = time.time()
            ticker = r.fetch_ticker(symbol)
            #print(i, "open:%s, bid:%s, ask:%s,cost:%s"%(ticker['open'],ticker['bid'],ticker['ask'], time.time()-start))
            all_info['liqui']['bid'] = ticker['bid']

            print(i, "bid k:%s, y:%s, liqui:%s"%(all_info['k']['bid'],all_info['y']['bid'],all_info['liqui']['bid']))

            time.sleep(0.5)
            """
        for i in range(1,10):
            r = self.k
            start = time.time()
            orderbook = r.fetch_order_book('BTC/USD', {
                'depth': 5,
                 })
            bid = orderbook['bids'][0][0] if len (orderbook['bids']) > 0 else None
            ask = orderbook['asks'][0][0] if len (orderbook['asks']) > 0 else None
            spread = (ask - bid) if (bid and ask) else None
            print (i, r.id, 'market price', { 'bid': bid, 'ask': ask, 'spread': spread }, "cost: %s sec"%(time.time()-start))
            r = self.y
            start = time.time()
            orderbook = r.fetch_order_book('BTC/USD', {
                'depth': 5,
                 })
            bid = orderbook['bids'][0][0] if len (orderbook['bids']) > 0 else None
            ask = orderbook['asks'][0][0] if len (orderbook['asks']) > 0 else None
            spread = (ask - bid) if (bid and ask) else None
            print (i, r.id, 'market price', { 'bid': bid, 'ask': ask, 'spread': spread }, "cost: %s sec"%(time.time()-start))
            """
