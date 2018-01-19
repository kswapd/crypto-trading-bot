#! /usr/bin/python
#-*-coding:utf-8-*- 
import urllib,urllib2
import json
import sys, time
import curses
import hmac,hashlib
import conf
class fetch_poloniex:
    def __init__(self):
        self.is_stop = False
        self.num = 50
        self.pos_y = 2
        self.target_symbol = ('USDT_BTC','USDT_LTC','USDT_BCH','USDT_ETH','USDT_XRP', 'USDT_DASH',  'BTC_DOGE')
        self.method = ('depth','ticker','trades', 'info')
        self.trade_list = ('ltc_usd', 'btc_usd', 'eth_usd', 'bcc_usd', 'dash_usd', 'doge_usd') 
        #self.coin_url = "https://api.coinmarketcap.com/v1/ticker/?limit=%d"%self.num
        self.base_url = 'https://poloniex.com/public?command=returnTicker'
        self.send_headers = {
 'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
 'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:55.0) Gecko/20100101 Firefox/55.0',
 'Cookie':'__cfduid=d92eb21c1dd0e150a8e730ef1e8780fd61516264900; cf_clearance=6cfee2bba5c3195454b486744acb78e68f37e101-1516330664-1800'
} 
        #keys_conf = conf.TradeKeys()
        #self.apikey = keys_conf.keys_info['poloniex']['public']
        #self.secret = keys_conf.keys_info['poloniex']['secret']
        self.apikey = 'aaa'
        self.secret = 'bbb'
	#print(self.secret)
	#print(self.apikey)
        self.monitor_info = {
                'BTC':{'last':{'price':-1, 'num':-1}, 'bid':{'price':-1, 'num':-1}, 'ask':{'price':-1, 'num':-1}},
                'LTC':{'last':{'price':-1, 'num':-1}, 'bid':{'price':-1, 'num':-1}, 'ask':{'price':-1, 'num':-1}},
                'ETH':{'last':{'price':-1, 'num':-1}, 'bid':{'price':-1, 'num':-1}, 'ask':{'price':-1, 'num':-1}},
                'XRP':{'last':{'price':-1, 'num':-1}, 'bid':{'price':-1, 'num':-1}, 'ask':{'price':-1, 'num':-1}}
            }
        self.symbol_info_pair = {'USDT_BTC':'BTC','USDT_LTC':'LTC','USDT_ETH':'ETH','USDT_XRP':'XRP'}
	
    def stop(self):
        self.is_stop = True
        curses.endwin()
        print('stopped')

    def get_ticker(self):
        ticker_url = self.base_url
        print(ticker_url)
        #self.stdscr = curses.initscr()
        #self.stdscr = curses.initscr()
        self.stdscr = curses.newwin(15, 80, 16, 0)
        #self.stdscr = curses.newpad(600, 800)
        curses.start_color()
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)

        while not self.is_stop:
            cur_pos_x = 2;
            myreq  = {}
            myreq['command'] = 'returnTicker' 
            myreq['nonce'] = int(time.time()*1000)
            post_data = urllib.urlencode(myreq)

            mysign = hmac.new(self.secret, post_data, hashlib.sha512).hexdigest()
            self.send_headers['Sign'] = mysign
            self.send_headers['Key'] = self.apikey
            #    'Sign': mysign,
            #    'Key': self.apikey
            #}
            req = urllib2.Request(ticker_url, headers=self.send_headers)
            res = urllib2.urlopen(req)
            page = res.read()
            json_obj = json.loads(page)
            #print(page)
            self.stdscr.box(curses.ACS_VLINE, curses.ACS_HLINE)
            self.stdscr.addstr(cur_pos_x,self.pos_y,'Poloniex', curses.color_pair(3))
            cur_pos_x += 1;
            self.stdscr.addstr(cur_pos_x,self.pos_y,time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()) ), curses.color_pair(3))
            cur_pos_x += 1;
            print_head =  "Symbol \tLast($) \tBuy \t\tSell \t\tPer"
            self.stdscr.addstr(cur_pos_x,self.pos_y,print_head,curses.color_pair(3))
            cur_pos_x += 1;
            for pair in self.target_symbol:
                color_index = 1
                if self.symbol_info_pair.has_key(pair):
                    self.monitor_info[self.symbol_info_pair[pair]]['last']['price'] = float(json_obj[pair]['last'])
                    self.monitor_info[self.symbol_info_pair[pair]]['bid']['price'] = float(json_obj[pair]['highestBid'])
                    self.monitor_info[self.symbol_info_pair[pair]]['ask']['price'] = float(json_obj[pair]['lowestAsk'])


                if pair in self.target_symbol:
                    #print_content =  "sym:%7s \tprice:%10s \tper:%5s"%(json_obj[i]['symbol'], json_obj[i]['price_usd'], json_obj[i]['percent_change_24h']);
                    print_content =  "%7s \t%7.2f \t%7.2f \t%7.2f \t%7.2f"%(pair, float(json_obj[pair]['last']), float(json_obj[pair]['highestBid']), float(json_obj[pair]['lowestAsk']), float(json_obj[pair]['percentChange']));
                    if json_obj[pair]['percentChange'][0] is '-':
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
    info = fetch_poloniex()
    try:
        info.get_ticker()
    except KeyboardInterrupt as e:
        info.stop()
    

    

