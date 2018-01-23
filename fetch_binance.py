#! /usr/bin/python
#-*-coding:utf-8-*- 
import urllib2
import json
import sys, time
import curses
import logging
import console_view as cv
class fetch_binance(cv.console_view):
    def __init__(self, x = 80, y = 16, width = 80, height = 15, is_view = True):
        cv.console_view.__init__(self, x, y, width, height, is_view)
        self.is_stop = False
        self.num = 50
        self.pos_y = 2
        self.target_symbol = ('BTC','ETH','XRP', 'BCH', 'LTC',  'DASH', 'USDT', 'DOGE')
        self.method = ('depth','ticker','trades', 'info')
        self.trade_list = ('BTCUSDT', 'LTCUSDT', 'ETHUSDT', 'XRPUSDT', 'DASHUSDT') 
        #self.coin_url = "https://api.coinmarketcap.com/v1/ticker/?limit=%d"%self.num
	self.base_url = 'https://api.binance.com/api/v3/ticker/price'
        self.send_headers = {
 'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
 'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
 'Connection':'keep-alive',
 'Cookie':'_ga=GA1.2.244936084.1515551927; _gid=GA1.2.711168496.1516671748; sajssdk_2015_cross_new_user=1; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2223985229%22%2C%22%24device_id%22%3A%2216120ae638968b-04a0897647b113-32607402-1296000-16120ae638ab0a%22%2C%22props%22%3A%7B%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%7D%2C%22first_id%22%3A%2216120ae638968b-04a0897647b113-32607402-1296000-16120ae638ab0a%22%7D'
} 
        self.monitor_info = {
                'time':time.time(),
                'BTC':{'last':{'price':-1, 'num':-1}, 'bid':{'price':-1, 'num':-1}, 'ask':{'price':-1, 'num':-1}},
                'LTC':{'last':{'price':-1, 'num':-1}, 'bid':{'price':-1, 'num':-1}, 'ask':{'price':-1, 'num':-1}},
                'ETH':{'last':{'price':-1, 'num':-1}, 'bid':{'price':-1, 'num':-1}, 'ask':{'price':-1, 'num':-1}},
                'XRP':{'last':{'price':-1, 'num':-1}, 'bid':{'price':-1, 'num':-1}, 'ask':{'price':-1, 'num':-1}},
                'DASH':{'last':{'price':-1, 'num':-1}, 'bid':{'price':-1, 'num':-1}, 'ask':{'price':-1, 'num':-1}},
                'DOGE':{'last':{'price':-1, 'num':-1}, 'bid':{'price':-1, 'num':-1}, 'ask':{'price':-1, 'num':-1}}
            }
        self.symbol_info_pair = {'BTCUSDT':'BTC','LTCUSDT':'LTC','ETHUSDT':'ETH','XRPUSDT':'XRP', 'DASHUSDT':'DASH'}
    def stop(self):
        self.is_stop = True
        curses.endwin()
        print('stopped')

    def get_ticker(self):
        ticker_url = self.base_url
        print(ticker_url)
        #self.stdscr = curses.initscr()
        #self.stdscr = curses.initscr()
        #self.stdscr = curses.newwin(15, 80, 16, 80)
        self.stdscr = curses.newwin(self.display_pos['height'], self.display_pos['width'], self.display_pos['y'], self.display_pos['x'])

        #self.stdscr = curses.newpad(600, 800)
        curses.start_color()
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)

        while not self.is_stop:
            cur_pos_x = 2;
            req = urllib2.Request(ticker_url, headers=self.send_headers)
            try:
                res = urllib2.urlopen(req,timeout=5)
                page = res.read()
                json_obj_all = json.loads(page)
                json_obj = json_obj_all
            except Exception,e:
                err = 'Get binance data error, please set right cookies'
                self.stdscr.addstr(cur_pos_x,self.pos_y,err,curses.color_pair(3))
                self.stdscr.refresh()
                time.sleep(2)
                continue
            #print(page)
            self.stdscr.box(curses.ACS_VLINE, curses.ACS_HLINE)
            self.stdscr.addstr(cur_pos_x,self.pos_y,'Binance', curses.color_pair(3))
            cur_pos_x += 1;
            self.stdscr.addstr(cur_pos_x,self.pos_y,time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()) ), curses.color_pair(3))
            cur_pos_x += 1;
            if self.view_mode == 'simp':
                print_head =  "Symbol \tLast($)"
            elif self.view_mode == 'complete':
                print_head =  "Symbol \tLast($) \tBuy \t\tSell \t\tPer"
            #print_head =  "Symbol \tLast($) \tBuy \t\tSell"
            self.stdscr.addstr(cur_pos_x,self.pos_y,print_head,curses.color_pair(3))
            cur_pos_x += 1;
            for coin in json_obj:
                if coin['symbol'] in self.trade_list:
                    pair = coin['symbol']
                #for pair in self.trade_list:
                    color_index = 1
                    self.monitor_info['time'] = time.time()
                    if self.symbol_info_pair.has_key(coin['symbol']):
                        self.monitor_info[self.symbol_info_pair[pair]]['last']['price'] = float(coin['price'])
                        self.monitor_info[self.symbol_info_pair[pair]]['bid']['price'] = float(coin['price'])
                        self.monitor_info[self.symbol_info_pair[pair]]['ask']['price'] = float(coin['price'])

                    if pair in self.trade_list:
                        #print_content =  "sym:%7s \tprice:%10s \tper:%5s"%(json_obj[i]['symbol'], json_obj[i]['price_usd'], json_obj[i]['percent_change_24h']);
                        if self.view_mode == 'simp':
                            print_content =  "%7s \t%7.2f"%(pair, float(coin['price']))
                        elif self.view_mode == 'complete':   
                            print_content =  "%7s \t%7.2f \t%7.2f \t%7.2f"%(pair, float(coin['price']), float(coin['price']), float(coin['price']))
                        
                        if not True:
                            color_index = 2
                        self.stdscr.addstr(cur_pos_x,self.pos_y,print_content,curses.color_pair(color_index))
                        cur_pos_x += 1

                    #print "hi:%d\r"%i
                    #stdscr.addstr(i, 0,  "hi:%d"%i)
                    #sys.stdout.flush()
                    self.stdscr.refresh()
            time.sleep(2)
if __name__ == "__main__":
    curses.initscr()
    info = fetch_binance()
    try:
        info.get_ticker()
    except KeyboardInterrupt as e:
        info.stop()
    

    

