import ccxt as ct
import pprint as pp
import trade 
import time
def time_me(fn):
    def _wrapper(*args, **kwargs):
            start = time.clock()
            fn(*args, **kwargs)
            print "%s cost %s second"%(fn.__name__, time.clock() - start)
    return _wrapper
atrade = trade.auto_trade()
atrade.start()
