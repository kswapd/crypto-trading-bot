#! /usr/bin/python
import ccxt as ct
import pprint as pp
import trade 
import time
import fetch_web
atrade = trade.auto_trade()
atrade.start()
#auto_fetch = fetch_web.fetch_url()
#auto_fetch.start()
