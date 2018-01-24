#! /usr/bin/python
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
import auto_monitor
if __name__ == "__main__":
    monitor = auto_monitor.auto_monitor()
    try:
        monitor.start()
    except KeyboardInterrupt as e:
        monitor.stop()
