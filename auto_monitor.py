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
import fetch_binance
import thread
import curses
import monitor
import logging
from logging.handlers import TimedRotatingFileHandler
from logging.handlers import RotatingFileHandler
import re
import console_view as cv
class auto_monitor(cv.console_view):
    def __init__(self, x = 0, y = 0, width = 130, height = 15, is_view = True):
        cv.console_view.__init__(self, x, y, width, height, is_view)
        self.p_info = {}
        self.k_info = {}
        self.log_init()
	self.min_w = 30	
	self.min_h = 15
	self.min_y = 16
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
        self.yobit = fetch_yobit.fetch_yobit(self.min_w*2,self.min_y,self.min_w,self.min_h)
        self.y_info = self.yobit.monitor_info
        self.yobit.get_ticker()

    def start_binance(self, thrd_name,delay):
        self.binance = fetch_binance.fetch_binance(self.min_w*3,self.min_y,self.min_w,self.min_h)
        self.binance_info = self.binance.monitor_info
        self.binance.get_ticker()

    def start_poloniex(self, thrd_name,delay):
        self.poloniex = fetch_poloniex.fetch_poloniex(0,self.min_y,self.min_w,self.min_h)
        self.p_info = self.poloniex.monitor_info
        self.poloniex.get_open_info()
    def start_kraken(self, thrd_name,delay):
        self.kraken = fetch_kraken.fetch_kraken(self.min_w,self.min_y,self.min_w,self.min_h)
        self.k_info = self.kraken.monitor_info
        self.kraken.get_open_info()
    def start_monitor(self, thrd_name,delay):
        logging.info('start monitor...')
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
            self.binance_info = self.binance.monitor_info
           
            pos_x = 2
            pos_y = 2
            stdscr.box(curses.ACS_VLINE, curses.ACS_HLINE)
            stdscr.addstr(pos_x,pos_y,'Cryptocurrency exchange Monitor', curses.color_pair(3))
            pos_x += 1
            nowtime = time.time()
            ptime =  time.strftime('%H:%M:%S', time.localtime(self.k_info['time']))
            ktime =  time.strftime('%H:%M:%S', time.localtime(self.p_info['time']))
            ytime =  time.strftime('%H:%M:%S', time.localtime(self.y_info['time']))
            binancetime =  time.strftime('%H:%M:%S', time.localtime(self.binance_info['time']))
            
            sub_ptime = self.p_info['time'] - nowtime
            sub_ytime = self.y_info['time'] - nowtime
            sub_ktime = self.k_info['time'] - nowtime
            sub_binancetime = self.binance_info['time'] - nowtime


            stdscr.addstr(pos_x,pos_y,time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(nowtime) ), curses.color_pair(3))
            pos_x += 1

            time_comp = ' P:%.2fs|K:%.2f|Y:%.2f|Binance:%.2f'%(sub_ptime, sub_ktime, sub_ytime, sub_binancetime)
            alltime_info = 'P:'+ptime + '|K:' + ktime + '|Y:'+ytime + '|Binance:'+binancetime + time_comp
            stdscr.addstr(pos_x, pos_y, alltime_info, curses.color_pair(3))
            pos_x += 1

            print_head =  "Symbol \tSub(K-P) \tPercent(K-P) \tSub(Y-P) \tPercent(Y-P) \tSub(Binance-P) \tPercent(Binance-P)"
            stdscr.addstr(pos_x,pos_y,print_head,curses.color_pair(3))
            pos_x += 1
            
            all_coin = ('BTC', 'LTC', 'ETH', 'XRP', 'DASH', 'DOGE')
    	    #logging.info(alltime_info)
            for coin in all_coin:
                cur = coin
                #prt_str = coin + " \t\t%7.2f \t%7.2f \t%7.2f \t%7.2f \t%7.2f \t%7.2f \t%7.2f"%(self.p_info[cur]['last']['price'], self.k_info[cur]['last']['price'],self.k_info[cur]['last']['price']-self.p_info[cur]['last']['price'], (self.k_info[cur]['last']['price']-self.p_info[cur]['last']['price'])*100/self.p_info[cur]['last']['price'], self.y_info[cur]['last']['price'],self.y_info[cur]['last']['price']-self.p_info[cur]['last']['price'], (self.y_info[cur]['last']['price']-self.p_info[cur]['last']['price'])*100/self.p_info[cur]['last']['price'])
                sub1 = self.p_info[cur]['bid']['price']-self.k_info[cur]['ask']['price']
                percent1 = sub1*100/self.k_info[cur]['ask']['price']
                if percent1 < -100 or percent1 > 100:
                    percent1 = -1.00

                if percent1 > 4.0 and cur=='LTC':
                    logging.info('get sell chance:%.2f,%.2f, %.2f,%.2f'%(self.p_info[cur]['bid']['price'], self.p_info[cur]['bid']['num'],self.k_info[cur]['ask']['price'], percent1))
                    self.poloniex.sell('LTC', self.p_info[cur]['bid']['price'], self.p_info[cur]['bid']['num'])
                

                sub2 = self.k_info[cur]['bid']['price']-self.p_info[cur]['ask']['price']
                percent2 = sub2*100/self.p_info[cur]['ask']['price']
                if percent2 < -100 or percent2 > 100:
                    percent2 = -1.00
                #sub2 = self.y_info[cur]['last']['price']-self.p_info[cur]['last']['price']
                #percent2 =  sub2*100/self.p_info[cur]['last']['price']
                #if percent2 < -100 or percent2 > 100:
                #    percent2 = -1.00

                sub3 = self.binance_info[cur]['last']['price']-self.p_info[cur]['last']['price']
                percent3 =  sub3*100/self.p_info[cur]['last']['price']
                if percent3 < -100 or percent3 > 100:
                    percent3 = -1.00

                prt_str = coin + " \t\t%7.2f \t%7.2f \t%7.2f \t%7.2f \t%7.2f \t%7.2f"%(sub1, percent1, sub2,percent2, sub3, percent3)
                num_str = "\t%7.2f \t%7.2f \t%7.2f \t%7.2f"%(self.p_info[cur]['bid']['num'], self.p_info[cur]['ask']['num'], self.k_info[cur]['bid']['num'], self.k_info[cur]['ask']['num'])
                prt_str =  re.sub(r'(-1.00)','--\t', prt_str)   
                #prt_str =  re.sub(r'(-[\d+\.\d]+)','--\t', prt_str)   
                stdscr.addstr(pos_x,pos_y,prt_str,curses.color_pair(3))
                pos_x += 1

                #log_str = prt_str + num_str
                #log_str =  re.sub(r'(-1.00)','--', log_str)   
    	    	#logging.info(log_str)
            stdscr.refresh()
            time.sleep(2)

    def start(self):
        try:
            curses.initscr()
	    curses.noecho()
	    #curses.cbreak()
	    curses.curs_set(0)
            #td1 = thread.start_new_thread( start_coin_market,('55',2) )
            td2 = thread.start_new_thread( self.start_yobit,('5',2) )
            td6 = thread.start_new_thread( self.start_binance,('9',2) )
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
    curses.noecho()
    info = auto_monitor()
    try:
        info.start()
    except KeyboardInterrupt as e:
        info.stop()
