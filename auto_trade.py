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
import monitor
#atrade = trade.auto_trade()
#atrade.start()
#auto_fetch = fetch_web.fetch_url()
#auto_fetch.start()
p_info = {}
k_info = {}
global infok
global infop
def start_coin_market(thrd_name, delay):
    coin_market = fetch_coinmarket.fetch_coinmarket()
    coin_market.start()
def start_yobit(thrd_name,delay):
    info = fetch_yobit.fetch_yobit()
    info.get_ticker()
def start_poloniex(thrd_name,delay):
    global infop
    infop = fetch_poloniex.fetch_poloniex()
    p_info = infop.monitor_info
    infop.get_ticker()
def start_kraken(thrd_name,delay):
    global infok
    infok = fetch_kraken.fetch_kraken()
    k_info = infok.monitor_info
    infok.get_ticker()
def start_monitor(thrd_name,delay):
    global infop
    global infok
    time.sleep(2)
    stdscr = curses.newwin(15, 80, 0, 0)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)

    while True:
        p_info = infop.monitor_info
        k_info = infok.monitor_info
        pos_x = 2
        pos_y = 2
        stdscr.box(curses.ACS_VLINE, curses.ACS_HLINE)
        stdscr.addstr(pos_x,pos_y,'Monitor', curses.color_pair(3))
        pos_x += 1
        stdscr.addstr(pos_x,pos_y,time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()) ), curses.color_pair(3))
        pos_x += 1
        print_head =  "Symbol \tPoloniex($) \tKraken \t\tSub \t\tPercent(%)"
        stdscr.addstr(pos_x,pos_y,print_head,curses.color_pair(3))
        pos_x += 1
        cur = 'BTC'
        stdscr.addstr(pos_x,pos_y,"BTC \t\t%7.2f \t%7.2f \t%7.2f, \t%7.2f"%(p_info[cur]['last']['price'], k_info[cur]['last']['price'],k_info[cur]['last']['price']-p_info[cur]['last']['price'], (k_info[cur]['last']['price']-p_info[cur]['last']['price'])*100/p_info[cur]['last']['price']),curses.color_pair(3))
        pos_x += 1
        cur = 'LTC'
        stdscr.addstr(pos_x,pos_y,"LTC \t\t%7.2f \t%7.2f \t%7.2f, \t%7.2f"%(p_info[cur]['last']['price'], k_info[cur]['last']['price'],k_info[cur]['last']['price']-p_info[cur]['last']['price'], (k_info[cur]['last']['price']-p_info[cur]['last']['price'])*100/p_info[cur]['last']['price']),curses.color_pair(3))
        pos_x += 1
        cur = 'ETH'
        stdscr.addstr(pos_x,pos_y,"ETH \t\t%7.2f \t%7.2f \t%7.2f, \t%7.2f"%(p_info[cur]['last']['price'], k_info[cur]['last']['price'],k_info[cur]['last']['price']-p_info[cur]['last']['price'], (k_info[cur]['last']['price']-p_info[cur]['last']['price'])*100/p_info[cur]['last']['price']),curses.color_pair(3))
        pos_x += 1
        cur = 'XRP'
        stdscr.addstr(pos_x,pos_y,"XRP \t\t%7.2f \t%7.2f \t%7.2f, \t%7.2f"%(p_info[cur]['last']['price'], k_info[cur]['last']['price'],k_info[cur]['last']['price']-p_info[cur]['last']['price'], (k_info[cur]['last']['price']-p_info[cur]['last']['price'])*100/p_info[cur]['last']['price']),curses.color_pair(3))
        pos_x += 1
        stdscr.refresh()
        time.sleep(2)

try:
    curses.initscr()
    #td1 = thread.start_new_thread( start_coin_market,('55',2) )
    #td2 = thread.start_new_thread( start_yobit,('5',2) )
    td3 = thread.start_new_thread( start_poloniex,('6',2) )
    td4 = thread.start_new_thread( start_kraken,('7',2) )
    td5 = thread.start_new_thread( start_monitor,('8',2) )
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
