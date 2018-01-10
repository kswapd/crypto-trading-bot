import ccxt as ct
import pprint as pp
import trade 
import time
atrade = trade.auto_trade()
atrade.start()
#t = ct.kraken()
#markets = t.load_markets()
#pp.pprint(t.id, markets)
#print(t.markets['ETH/USD'])
#print(t.symbols)
#print(t.markets.keys())
#print(t.currencies)
#print(t.fetch_ticker('LTC/USD'))
