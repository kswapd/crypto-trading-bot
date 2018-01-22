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
import logging
from logging.handlers import TimedRotatingFileHandler
from logging.handlers import RotatingFileHandler
import re
import console_view as cv
class auto_trade(cv.console_view):
    def __init__(self, x = 0, y = 0, width = 140, height = 15, is_view = True):
        cv.console_view.__init__(self, x, y, width, height, is_view)
        self.p_info = {}
        self.k_info = {}
        self.log_init()
    def log_init(self):
        '''
        log_fmt = '%(asctime)s\tFile \"%(filename)s\",line %(lineno)s\t%(levelname)s: %(message)s'
        formatter = logging.Formatter(log_fmt)
        log_file_handler = TimedRotatingFileHandler(filename="monitor"+"thread_", when="D", interval=1, backupCount=7)
        log_file_handler.suffix = "%Y-%m-%d_%H-%M.log"
        log_file_handler.extMatch = re.compile(r"^\d{4}-\d{2}-\d{2}_\d{2}-\d{2}.log$")
        log_file_handler.setFormatter(formatter)
        log_file_handler.setLevel(logging.DEBUG)
        log = logging.getLogger()
        log.addHandler(log_file_handler)
        '''
        logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='monitor.log',
                    filemode='w')
        
    def start_coin_market(self, thrd_name, delay):
        coin_market = fetch_coinmarket.fetch_coinmarket()
        coin_market.start()
    def start_yobit(self, thrd_name,delay):
        self.yobit = fetch_yobit.fetch_yobit(90, 16, 45, 15)
        self.y_info = self.yobit.monitor_info
        self.yobit.get_ticker()
    def start_poloniex(self, thrd_name,delay):
        self.poloniex = fetch_poloniex.fetch_poloniex(0,16,45,15)
        self.p_info = self.poloniex.monitor_info
        self.poloniex.get_ticker()
    def start_kraken(self, thrd_name,delay):
        self.kraken = fetch_kraken.fetch_kraken(45,16,45,15)
        self.k_info = self.kraken.monitor_info
        self.kraken.get_ticker()
    def start_monitor(self, thrd_name,delay):
        time.sleep(2)
        #stdscr = curses.newwin(15, 140, 0, 0)
        stdscr = curses.newwin(self.display_pos['height'], self.display_pos['width'], self.display_pos['y'], self.display_pos['x'])

        curses.start_color()
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        while True:
            self.p_info = self.poloniex.monitor_info
            self.k_info = self.kraken.monitor_info
            self.y_info = self.yobit.monitor_info
            pos_x = 2
            pos_y = 2
            stdscr.box(curses.ACS_VLINE, curses.ACS_HLINE)
            stdscr.addstr(pos_x,pos_y,'Monitor', curses.color_pair(3))
            pos_x += 1
            ptime =  time.strftime('%H:%M:%S', time.localtime(self.k_info['time']))
            ktime =  time.strftime('%H:%M:%S', time.localtime(self.p_info['time']))
            ytime =  time.strftime('%H:%M:%S', time.localtime(self.y_info['time']))
            subtime = self.k_info['time'] - self.p_info['time']
            suby_ptime = self.y_info['time'] - self.p_info['time']
            stdscr.addstr(pos_x,pos_y,time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()) ), curses.color_pair(3))
            pos_x += 1
            time_comp = '|Cur-P:%.2fs|K-P:%.2fs|Y-P:%.2f'%(time.time()-self.p_info['time'], subtime, suby_ptime)
            stdscr.addstr(pos_x, pos_y, 'P:'+ptime + '|K:' + ktime + '|Y:'+ytime+ time_comp, curses.color_pair(3))
            pos_x += 1
            print_head =  "Symbol \tPoloniex($) \tKraken \t\tSub(K-P) \tPercent(K-P) \tYobit\t\tSub(Y-P) \tPercent(Y-P)"
            stdscr.addstr(pos_x,pos_y,print_head,curses.color_pair(3))
            pos_x += 1


            '''
            cur = 'BTC'
            stdscr.addstr(pos_x,pos_y,"BTC \t\t%7.2f \t%7.2f \t%7.2f, \t%7.2f "%(self.p_info[cur]['last']['price'], self.k_info[cur]['last']['price'],self.k_info[cur]['last']['price']-self.p_info[cur]['last']['price'], (self.k_info[cur]['last']['price']-self.p_info[cur]['last']['price'])*100/self.p_info[cur]['last']['price']),curses.color_pair(3))
            pos_x += 1
            cur = 'LTC'
            stdscr.addstr(pos_x,pos_y,"LTC \t\t%7.2f \t%7.2f \t%7.2f, \t%7.2f"%(self.p_info[cur]['last']['price'], self.k_info[cur]['last']['price'],self.k_info[cur]['last']['price']-self.p_info[cur]['last']['price'], (self.k_info[cur]['last']['price']-self.p_info[cur]['last']['price'])*100/self.p_info[cur]['last']['price']),curses.color_pair(3))
            pos_x += 1
            cur = 'ETH'
            stdscr.addstr(pos_x,pos_y,"ETH \t\t%7.2f \t%7.2f \t%7.2f, \t%7.2f"%(self.p_info[cur]['last']['price'], self.k_info[cur]['last']['price'],self.k_info[cur]['last']['price']-self.p_info[cur]['last']['price'], (self.k_info[cur]['last']['price']-self.p_info[cur]['last']['price'])*100/self.p_info[cur]['last']['price']),curses.color_pair(3))
            pos_x += 1
            cur = 'XRP'
            prt_str = "XRP \t\t%7.2f \t%7.2f \t%7.2f, \t%7.2f"%(self.p_info[cur]['last']['price'], self.k_info[cur]['last']['price'],self.k_info[cur]['last']['price']-self.p_info[cur]['last']['price'], (self.k_info[cur]['last']['price']-self.p_info[cur]['last']['price'])*100/self.p_info[cur]['last']['price'])
            stdscr.addstr(pos_x,pos_y,prt_str,curses.color_pair(3))
            pos_x += 1



            cur = 'DASH'
            prt_str = "DASH \t\t%7.2f \t%7.2f \t%7.2f, \t%7.2f"%(self.p_info[cur]['last']['price'], self.k_info[cur]['last']['price'],self.k_info[cur]['last']['price']-self.p_info[cur]['last']['price'], (self.k_info[cur]['last']['price']-self.p_info[cur]['last']['price'])*100/self.p_info[cur]['last']['price'])
            stdscr.addstr(pos_x,pos_y,prt_str,curses.color_pair(3))
            pos_x += 1
            

            cur = 'DOGE'
            prt_str = "DOGE \t\t%7.2f \t%7.2f \t%7.2f, \t%7.2f"%(self.p_info[cur]['last']['price'], self.k_info[cur]['last']['price'],self.k_info[cur]['last']['price']-self.p_info[cur]['last']['price'], (self.k_info[cur]['last']['price']-self.p_info[cur]['last']['price'])*100/self.p_info[cur]['last']['price'])
            stdscr.addstr(pos_x,pos_y,prt_str,curses.color_pair(3))
            pos_x += 1
            '''


            all_coin = ('BTC', 'LTC', 'ETH', 'XRP', 'DASH', 'DOGE')
            for coin in all_coin:
                cur = coin
                prt_str = coin + " \t\t%7.2f \t%7.2f \t%7.2f \t%7.2f \t%7.2f \t%7.2f \t%7.2f"%(self.p_info[cur]['last']['price'], self.k_info[cur]['last']['price'],self.k_info[cur]['last']['price']-self.p_info[cur]['last']['price'], (self.k_info[cur]['last']['price']-self.p_info[cur]['last']['price'])*100/self.p_info[cur]['last']['price'], self.y_info[cur]['last']['price'],self.y_info[cur]['last']['price']-self.p_info[cur]['last']['price'], (self.y_info[cur]['last']['price']-self.p_info[cur]['last']['price'])*100/self.p_info[cur]['last']['price'])
                
                prt_str =  re.sub(r'(-[\d+\.\d]+)','--\t', prt_str)   
                stdscr.addstr(pos_x,pos_y,prt_str,curses.color_pair(3))
                pos_x += 1



            stdscr.refresh()
    	    logging.info(prt_str+time_comp)
            time.sleep(2)

    def start(self):
        try:
            curses.initscr()
            #td1 = thread.start_new_thread( start_coin_market,('55',2) )
            td2 = thread.start_new_thread( self.start_yobit,('5',2) )
            td3 = thread.start_new_thread( self.start_poloniex,('6',2) )
            td4 = thread.start_new_thread( self.start_kraken,('7',2) )
            td5 = thread.start_new_thread( self.start_monitor,('8',2) )
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
    info = auto_trade()
    try:
        info.start()
    except KeyboardInterrupt as e:
        info.stop()
