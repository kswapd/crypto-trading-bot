#! /usr/bin/python3
#-*-coding:utf-8-*- 
import urllib2
import json
import sys, time
import curses
class fetch_coinmarket:
    def start(self):
        self.num = 50
        self.targetSymbol = ('BTC','ETH','XRP', 'BCH', 'LTC', 'XLM', 'DASH', 'USDT', 'DOGE')
        coin_url = "https://api.coinmarketcap.com/v1/ticker/?limit=%d"%self.num
        print coin_url
        stdscr = curses.initscr()
        curses.start_color()
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)

        while True:
            req = urllib2.Request(coin_url)
            res = urllib2.urlopen(req)
            page = res.read()
            json_obj = json.loads(page)
            stdscr.addstr(0,0,time.asctime( time.localtime(time.time()) ), curses.color_pair(1))
            cur_pos_x = 1;
            for i in range(self.num):
                color_index = 1

                if json_obj[i]['symbol'] in self.targetSymbol:
                    print_content =  "sym:%7s \tprice:%10s \tper:%5s"%(json_obj[i]['symbol'], json_obj[i]['price_usd'], json_obj[i]['percent_change_24h']);
                    if json_obj[i]['percent_change_24h'][0] == '-':
                        color_index = 2
                    stdscr.addstr(cur_pos_x,0,print_content,curses.color_pair(color_index))
                    cur_pos_x += 1

                #print "hi:%d\r"%i
                #stdscr.addstr(i, 0,  "hi:%d"%i)
                #sys.stdout.flush()
                stdscr.refresh()
            time.sleep(10)
        print 'finished'

    

