#! /usr/bin/python
#-*-coding:utf-8-*- 
import ccxt as ct
import pprint as pp
import trade 
import time
import fetch_web
import fetch_coinmarket
import fetch_yobit
import thread
import curses
#atrade = trade.auto_trade()
#atrade.start()
#auto_fetch = fetch_web.fetch_url()
#auto_fetch.start()

def start_coin_market(thrd_name, delay):
    coin_market = fetch_coinmarket.fetch_coinmarket()
    coin_market.start()
def start_yobit(thrd_name,delay):
    info = fetch_yobit.fetch_yobit()
    info.get_ticker()
try:
    curses.initscr()
    td1 = thread.start_new_thread( start_coin_market,('55',2) )
    td2 = thread.start_new_thread( start_yobit,('5',2) )
except KeyboardInterrupt as e:
    #coin_market.stop()
    print 'over'
try:
    while 1:
        pass
except KeyboardInterrupt as e:
    #coin_market.stop()
    curses.endwin()
    print 'over'
