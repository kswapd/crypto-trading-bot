import pprint as pp
#import trade 
import time
import fetch_web
import fetch_coinmarket
import fetch_yobit
import fetch_poloniex
import fetch_kraken
import _thread
import curses
class trade_monitor:
    def __init__(self):
        a = 1
    def start2(self):
        print('aaaa')
    def start(self):
        time.sleep(5)
        self.stdscr = curses.newwin(15, 80, 0, 0)
        curses.start_color()
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        while True:
            pos_x = 2
            pos_y = 2
            self.stdscr.box(curses.ACS_VLINE, curses.ACS_HLINE)
            self.stdscr.addstr(pos_x,pos_y,'Monitor', curses.color_pair(3))
            pos_x += 1
            self.stdscr.addstr(pos_x,pos_y,time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()) ), curses.color_pair(3))
            pos_x += 1
            print_head =  "Symbol \tLast($) \tBuy \t\tSell"
            self.stdscr.addstr(pos_x,pos_y,print_head,curses.color_pair(3))
            pos_x += 1
            self.stdscr.addstr(pos_x,pos_y,print_head,curses.color_pair(3))
            pos_x += 1

            self.stdscr.refresh()
            time.sleep(2)
