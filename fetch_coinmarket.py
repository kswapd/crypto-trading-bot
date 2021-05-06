#! /usr/bin/python
#-*-coding:utf-8-*- 
import urllib.request
import json
import sys, time
import curses
import console_view as cv
class fetch_coinmarket(cv.console_view):
    def __init__(self, x = 0, y = 0, width = 80, height = 15, is_view = True):
        cv.console_view.__init__(self, x, y, width, height, is_view)
        self.is_stop = False
        self.num = 50
        self.pos_y = 2 
        self.targetSymbol = ('BTC','ETH','XRP', 'BCH', 'LTC',  'DASH', 'USDT', 'DOGE')
        #self.coin_url = "https://pro-api.coinmarketcap.com/v1/ticker/?limit=%d"%self.num
        self.coin_url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
    def stop(self):
        self.is_stop = True
        curses.endwin()
        print('stopped')

    def start(self):
        print(self.coin_url)
        #self.stdscr = curses.initscr()
        #self.stdscr = curses.initscr()
        #self.stdscr = curses.newwin(15, 80, 0, 0)
        self.stdscr = curses.newwin(self.display_pos['height'], self.display_pos['width'], self.display_pos['y'], self.display_pos['x'])

        #self.stdscr = curses.newpad(600, 800)
        curses.start_color()
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)

        while not self.is_stop:
            cur_pos_x = 2;
            headers = {
                'Accepts': 'application/json',
                'X-CMC_PRO_API_KEY': 'b22f9e6d-6c09-431d-ac9a-fd87131fc9a5',
                }
            req = urllib.request.Request(url=self.coin_url, headers=headers)
            res = urllib.request.urlopen(req)
            page = res.read()
            json_obj = json.loads(page)
            print(json_obj)
            self.stdscr.box(curses.ACS_VLINE, curses.ACS_HLINE)
            self.stdscr.addstr(cur_pos_x,self.pos_y,'Coin market cap', curses.color_pair(3))
            cur_pos_x += 1;
            self.stdscr.addstr(cur_pos_x,self.pos_y,time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()) ), curses.color_pair(3))
            cur_pos_x += 1;
            print_head =  "Symbol \tPrice($) \tPercent(24h)"
            self.stdscr.addstr(cur_pos_x,self.pos_y,print_head,curses.color_pair(3))
            cur_pos_x += 1;
            for i in range(self.num):
                color_index = 1

                if json_obj[i]['symbol'] in self.targetSymbol:
                    #print_content =  "sym:%7s \tprice:%10s \tper:%5s"%(json_obj[i]['symbol'], json_obj[i]['price_usd'], json_obj[i]['percent_change_24h']);
                    print_content =  "%7s \t%7s \t%7s"%(json_obj[i]['symbol'], json_obj[i]['price_usd'], json_obj[i]['percent_change_24h']);
                    if json_obj[i]['percent_change_24h'][0] == '-':
                        color_index = 2
                    self.stdscr.addstr(cur_pos_x,self.pos_y,print_content,curses.color_pair(color_index))
                    cur_pos_x += 1

                #stdscr.addstr(i, 0,  "hi:%d"%i)
                #sys.stdout.flush()
                self.stdscr.refresh()
            time.sleep(10)
if __name__ == "__main__":
    curses.initscr()
    coin_market = fetch_coinmarket()
    try:
        coin_market.start()
    except KeyboardInterrupt as e:
        coin_market.stop()
    

    

