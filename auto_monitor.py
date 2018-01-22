#! /usr/bin/python
#-*-coding:utf-8-*- 
#import ccxt as ct
import pprint as pp
#import trade 
import time
import fetch_web
import fetch_coinmarket
import fetch_yobit
import fetch_poloniex
import fetch_kraken
import thread
import curses

class auto_monitor:    
    def start_coin_market(self,thrd_name, delay):
        coin_market = fetch_coinmarket.fetch_coinmarket()
        coin_market.start()
    def start_yobit(self,thrd_name,delay):
        info = fetch_yobit.fetch_yobit()
        info.get_ticker()
    def start_poloniex(self,thrd_name,delay):
        info = fetch_poloniex.fetch_poloniex()
        info.get_ticker()
    def start_kraken(self,thrd_name,delay):
        info = fetch_kraken.fetch_kraken()
        info.get_ticker()
    def start(self):
        try:
            curses.initscr()
            td1 = thread.start_new_thread(self.start_coin_market,('55',2) )
            #time.sleep(0.5)
            td2 = thread.start_new_thread( self.start_yobit,('5',2) )
            #time.sleep(0.5)
            td3 = thread.start_new_thread( self.start_poloniex,('6',2) )
            #time.sleep(0.5)
            td4 = thread.start_new_thread( self.start_kraken('7',2) )
            #time.sleep(0.5)
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
    def stop(self):
        curses.endwin()

if __name__ == "__main__":
    curses.initscr()
    info = auto_monitor()
    try:
        info.start()
    except KeyboardInterrupt as e:
        info.stop()

