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
         print(self.coinmarket.hasFetchOHLCV, self.coinmarket.rateLimit)
         keys_conf = conf.TradeKeys()
         print(keys_conf.keys_info)
         self.k.apiKey = keys_conf.keys_info['kraken']['public']
         self.k.secret = keys_conf.keys_info['kraken']['secret']
         print (self.k.fetch_balance ())
         print (self.k.fetch_orders ())
         #print(self.k.fetch_ohlcv('LTC/USD', '1d'))
    def start(self):
        for i in range(0,10):
            r = self.k
            start = time.time()
            ticker = r.fetch_ticker('LTC/USD')
            print(i, "open:%s, bid:%s, ask:%s,cost:%s"%(ticker['open'],ticker['bid'],ticker['ask'], time.time()-start))
            r = self.y
            start = time.time()
            ticker = r.fetch_ticker('LTC/USD')
            print(i, "open:%s, bid:%s, ask:%s,cost:%s"%(ticker['open'],ticker['bid'],ticker['ask'], time.time()-start))
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
