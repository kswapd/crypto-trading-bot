import ccxt as ct
import pprint
import trade 
import time
class auto_trade:
    def prt(self,info):
        pprint.pprint(info)
    def __init__(self):
         self.k = ct.kraken()
         self.y = ct.yobit()
         self.p = ct.poloniex()
         self.coinmarket = ct.coinmarketcap()
         print(ct.exchanges)
    def start(self):
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
