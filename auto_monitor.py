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
import fetch_huobi
import _thread
import curses
import monitor
import logging
from logging.handlers import TimedRotatingFileHandler
from logging.handlers import RotatingFileHandler
import re
import console_view as cv
class auto_monitor(cv.console_view):
    def __init__(self, x = 0, y = 0, width = 130, height = 15, is_view = True):
        #cv.console_view.__init__(self, x, y, width, height, is_view)
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
        log_file_handler = TimedRotatingFileHandler(filename="monitor"+"_thread", when="D", interval=1, backupCount=7)
        log_file_handler.suffix = "%Y-%m-%d_%H-%M.log"
        log_file_handler.extMatch = re.compile(r"^\d{4}-\d{2}-\d{2}_\d{2}-\d{2}.log$")
        log_file_handler.setFormatter(formatter)
        log_file_handler.setLevel(logging.DEBUG)
        log = logging.getLogger()
        log.addHandler(log_file_handler)
        '''
        logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    #datefmt='%a, %d %b %Y %H:%M:%S',
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
    def start_huobi(self, thrd_name,delay):
        self.huobi = fetch_huobi.fetch_huobi(0,self.min_y,self.min_w,self.min_h)
        self.huobi_info = self.huobi.monitor_info
        self.huobi.get_open_info()
    def start_kraken(self, thrd_name,delay):
        self.kraken = fetch_kraken.fetch_kraken(self.min_w,self.min_y,self.min_w,self.min_h)
        self.k_info = self.kraken.monitor_info
        self.kraken.get_open_info()
    def start_monitor(self, thrd_name,delay):
        logging.info('start monitor...')
        print('start monitor...')
        time.sleep(2)
        #stdscr = curses.newwin(15, 140, 0, 0)
        #stdscr = curses.newwin(self.display_pos['height'], self.display_pos['width'], self.display_pos['y'], self.display_pos['x'])

        #curses.start_color()
        #curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
        #curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
        #curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        while True:
            self.p_info = self.poloniex.monitor_info
            self.k_info = self.kraken.monitor_info
            #self.y_info = self.yobit.monitor_info
            #self.binance_info = self.binance.monitor_info
            self.huobi_info = self.huobi.monitor_info
           
            pos_x = 2
            pos_y = 2
            #stdscr.box(curses.ACS_VLINE, curses.ACS_HLINE)
            #stdscr.addstr(pos_x,pos_y,'Cryptocurrency exchange Monitor', curses.color_pair(3))
            pos_x += 1
            nowtime = time.time()
            ptime =  time.strftime('%H:%M:%S', time.localtime(self.p_info['time']))
            ktime =  time.strftime('%H:%M:%S', time.localtime(self.k_info['time']))
            huobitime = time.strftime('%H:%M:%S', time.localtime(self.huobi_info['time']))
            sub_ptime = self.p_info['time'] - nowtime
            #sub_ytime = self.y_info['time'] - nowtime
            sub_ktime = self.k_info['time'] - nowtime
            #sub_binancetime = self.binance_info['time'] - nowtime
            sub_huobitime = self.huobi_info['time'] - nowtime

            #stdscr.addstr(pos_x,pos_y,time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(nowtime) ), curses.color_pair(3))
            pos_x += 1

            time_comp = ' P:%.2fs|huobi:%.2fs|K:%.2fs'%(sub_ptime, sub_huobitime, sub_ktime)
            alltime_info = 'P:'+ptime + '|huobi:' + huobitime  +'|K:'+ktime + time_comp
            #stdscr.addstr(pos_x, pos_y, alltime_info, curses.color_pair(3))
            pos_x += 1

            print_head =  "Symbol \tP \thuobi"
            #stdscr.addstr(pos_x,pos_y,print_head,curses.color_pair(3))
            pos_x += 1
            all_coin = [ 'LTC']
            for coin in all_coin:
                cur = coin
                #print('{:}'.format(self.k_info[cur]))

                pbp = self.p_info[cur]['bid']['price']
                pbn = self.p_info[cur]['bid']['num']

                pap = self.p_info[cur]['ask']['price']
                pan = self.p_info[cur]['ask']['num']

                hap = self.huobi_info[cur]['ask']['price']
                han = self.huobi_info[cur]['ask']['num']

                hbp = self.huobi_info[cur]['bid']['price']
                hbn = self.huobi_info[cur]['bid']['num']

                kbp = self.k_info[cur]['bid']['price']
                kbn = self.k_info[cur]['bid']['num']
                kap = self.k_info[cur]['ask']['price']
                kan = self.k_info[cur]['ask']['num']

                all_exchanges_info = {'poloniex':self.p_info[cur], 'huobi':self.huobi_info, 'kraken':self.k_info}
                max_bid = sorted(dict,key=lambda x:all_exchanges_info[x]['bid']['price'])[-1]

                min_ask = sorted(dict,key=lambda x:all_exchanges_info[x]['ask']['price'])[0]    

                print('maxbid:%s, minask:%s'%(max_bid, min_ask))
               #bid_price = [pbp, hbp, kbp]
                #ask_price = [pap, hap, kap]




                sub1 = pbp - hap
                percent1 = sub1*100/hap
                if percent1 < -100 or percent1 > 100:
                    percent1 = -1.00

                if percent1 > 1.0 and cur=='LTC':
                    
                    logging.info('get chance:%.2f,%.2f, %.2f,%.2f, %.2f'%(pbp, pbn,hap,han, percent1))
                    trade_num =  pbn if  pbn < han else han
                    self.poloniex.sell('LTC', pbp, trade_num)
                    self.huobi.buy('ltc', hap, trade_num)
                
                sub2 = hbp - pap
                percent2 = sub2*100/pap
                if percent2 < -100 or percent2 > 100:
                    percent2 = -1.00
                if percent2 > 1.0 and cur == 'LTC':
                    logging.info('get chance2:%.2f,%.2f, %.2f,%.2f, %.2f'%(hbp, hbn,pap,pan, percent2))

                    trade_num2 = hbn if hbn < pan else pan
                    self.huobi.sell('ltc', hbp, trade_num2)
                    self.poloniex.buy('LTC', pap, trade_num2)



                sub3 = hbp - kap
                percent3 = sub3*100/kap
                if percent3 < -100 or percent3 > 100:
                    percent3 = -1.00
                if percent3 > 1.0 and cur == 'LTC':
                    logging.info('get chance3:%.2f,%.2f, %.2f,%.2f, %.2f'%(hbp, hbn,kap,kan, percent3))

                    trade_num3 = hbn if hbn < kan else kan
                    self.huobi.sell('ltc', hbp, trade_num3)
                    self.kraken.buy('LTC', kap, trade_num3)






                sub4 = kbp - hap
                percent4 = sub4*100/hap
                if percent4 < -100 or percent4 > 100:
                    percent4 = -1.00

                if percent4 > 1.0 and cur=='LTC':
                    
                    logging.info('get chance4:%.2f,%.2f, %.2f,%.2f, %.2f'%(kbp, kbn,hap,han, percent4))
                    trade_num4 =  kbn if  kbn < han else han
                    self.kraken.sell('LTC', kbp, trade_num4)
                    self.huobi.buy('ltc', hap, trade_num4)




                sub5 = pbp - kap
                percent5 = sub5*100/kap
                if percent5 < -100 or percent5 > 100:
                    percent5 = -1.00

                if percent5 > 1.0 and cur=='LTC':
                    
                    logging.info('get chance5:%.2f,%.2f, %.2f,%.2f, %.2f'%(pbp, pbn,kap,kan, percent5))
                    trade_num5 =  pbn if  pbn < kan else kan
                    self.poloniex.sell('LTC', pbp, trade_num5)
                    self.kraken.buy('LTC', kap, trade_num5)




                sub6 = kbp - pap
                percent6 = sub6*100/pap
                if percent6 < -100 or percent6 > 100:
                    percent6 = -1.00

                if percent6 > 1.0 and cur=='LTC':
                    
                    logging.info('get chance6:%.2f,%.2f, %.2f,%.2f, %.2f'%(kbp, kbn,pap,pan, percent6))
                    trade_num6 =  kbn if  kbn < pan else pan
                    self.kraken.sell('LTC', kbp, trade_num6)
                    self.poloniex.buy('LTC', pap, trade_num6)








                prt_str = coin + " \t\t%7.2f \t%7.2f \t%7.2f"%(pbp, hbp, kbp)
                log_str_price = coin + ",%.2f,%.2f,%.2f,%.2f,%.2f,%.2f"%(percent1,percent2,percent3,percent4,percent5,percent6)
                #log_str_num = ",%.2f,%.2f,%.2f,%.2f"%(pbn, han, hbn, pan)
               
                #prt_str =  re.sub(r'(-1.00)','--\t', prt_str)   
        
                #stdscr.addstr(pos_x,pos_y,prt_str,curses.color_pair(3))
                pos_x += 1

                log_str = log_str_price
                #log_str =  re.sub(r'(-1.00)','--', log_str)   
                logging.info(log_str)
            #stdscr.refresh()
            time.sleep(2)

    def start(self):
        try:
            #curses.initscr()
	    #curses.noecho()
	    #curses.cbreak()
	    #curses.curs_set(0)
            #td1 = _thread.start_new_thread( start_coin_market,('55',2) )
            #td2 = _thread.start_new_thread( self.start_yobit,('5',2) )
            #td6 = _thread.start_new_thread( self.start_binance,('9',2) )
            #td3 = _thread.start_new_thread( self.start_poloniex,('6',2) )
            #td4 = _thread.start_new_thread( self.start_kraken,('7',2) )
            #td5 = _thread.start_new_thread( self.start_monitor,('8',2) )
            #td7 = _thread.start_new_thread( self.start_huobi,('9',2) )
            #time.sleep(0.5)
        except KeyboardInterrupt as e:
            #coin_market.stop()
            print('over')
        try:
            while 1:
                pass
        except KeyboardInterrupt as e:
            #coin_market.stop()
            #curses.endwin()
            print('over')
    def stop(self):
        print('over')
        #curses.endwin()

if __name__ == "__main__":
    #curses.initscr()
    #curses.noecho()
    info = auto_monitor()
    try:
        info.start()
    except KeyboardInterrupt as e:
        info.stop()
