import ccxt as ct
import pprint as pp

#polo   = ccxt.poloniex({
#        'apiKey': 'JDPP5LLW-JT0S02DE-PSQX7TX8-UXREDFLM',
#            'secret': '9a0718c859f5331663731566198f7ec802907c994935955493108fe26b40f1a0ffcbb8ec8aebc989c2dcb3249ead57a1025ca62d92c8ab78b4b877a953569194',
#            })
#polo = ct.poloniex()
k = ct.kraken()
#polo = ct.huobi()
print(ct.exchanges)
pp.pprint(k.id, k.load_markets())
#print(k.id, k.load_markets())
#print(polo.fetch_trades('BTC/CNY'))
#print(polo.fetch_balance())
