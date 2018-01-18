#! /usr/bin/python
import ccxt as ct
import pprint as pp
import trade 
import time
import fetch_web
import fetch_info
#atrade = trade.auto_trade()
#atrade.start()
#auto_fetch = fetch_web.fetch_url()
#auto_fetch.start()
coin_market = fetch_info.fetch_coinmarket()
try:
    coin_market.start()
except KeyboardInterrupt as e:
    coin_market.stop()
