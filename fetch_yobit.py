#! /usr/bin/python
#-*-coding:utf-8-*- 
import urllib2
import json
import sys, time
import curses
class fetch_yobit:
    def __init__(self):
        self.is_stop = False
        self.num = 50
        self.pos_y = 2
        self.target_symbol = ('BTC','ETH','XRP', 'BCH', 'LTC',  'DASH', 'USDT', 'DOGE')
        self.method = ('depth','ticker','trades', 'info')
        self.trade_list = ('ltc_usd', 'btc_usd', 'eth_usd', 'bcc_usd', 'dash_usd', 'doge_usd') 
        #self.coin_url = "https://api.coinmarketcap.com/v1/ticker/?limit=%d"%self.num
        self.base_url = 'https://yobit.net/api/3/'
        self.send_headers = {
 'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
 'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
 'Connection':'keep-alive',
 'Cookie':'__cfduid=dd5204b987cf59c58323bf14b8181e3121513921199; s1=eTGNGD%2BP%2Fo4UItAi5zuM8RJjc%2BKvcFCnth2l%2BqDeO8bDIYlVOXhES7blsIlQ7tkGb5cI5tyuBXgyj6IilvviEoT0jZpJB5R8wajPGQrBeRXToiQTKcsb6Wcw6aNTod3Y5sFwhJGI6UmFS9XhnJG1xj4JNQh4hIX4RNuT%2Bt7zX16iW%2FMFb32Up2oCvwCCmyU1mXkFQPkjXst%2B0ZNxDy%2BmdEEgvVDWrCh%2FaF9gcDPuGvcqTmOGS7UnCls7RyFiM5x7hxiJnvLC2WuqURYAEaDuh0IzMORSkTZv8vikmo4CIXnalPRnQ0koclBSEctOgKrBgAyChGe%2BnAwMN%2BrjlWB41ytsmQ29GsI%2F%2FPLzEdTLsROMblCIGZk80nXJm8aumz8%2FuR%2BwlMhTf5PwdOzT6xOQ43Ea2XefqJwlCVMOBabiYSo6VT2Lyg2O65Wo8MS4dcwCtVsrTSyP2tN9T4n4obnIKNdtN%2Bi7uBaYlykeqso2hn0mUZCIvObC9IVdgABEJjsess%2FLnZF85tMdNIXQ4fZ0KYz2YJeb2ImT64c3BLcvh6sEiCDMQjOr5KBKF5fW%2BgrDlBW8wME2TYR%2FRLPkojtPMjAwPrCIVEcxtp5QIu2TR%2BUl8jjqijoHiS7zZ6D9mfXEBzVUCcObO3cLXlWq34LStICfa9BysrAXy8qlQ7h6ek8%3D; s2=CfL6cJRtD7i41AjHzynWAlhL8C4bD53sz0Udn7zL%2BtitfFrpgPa%2FsQakq3YshcXe9AI4%2FkPokuK8GxKzT0shTHdc%2Fq0vOFpeSisRKaMViyRsvpy5EgLpGlYbafpuMe8%2Fe7l2MigkzMDqRrxP5fUsBA5sUueczutv9llJEdTaWWzB7vxtoiQ0evFSl0zUmOJlAk98UxkOACJi%2B3RUHfb8auERBRMPLMh62f02MTCBhVBUKBpdCR%2Bolz9XOJQ99a1gc%2Fy7YNeYjXzX%2BE6BjKsqarGu2l2xDZu88LRGFnjnE8BhTG7GVgws2xV64BfFlngOI57MYgbahRB%2FPMJmkQd4T5fEGkrQwbY49lTgJ98nyZgpAG2QqQM6JZh8LkUy%2Fv%2Fqc6LWd8b1npWjsKuiOx7ME2x4IFRTFNmCp9%2FuFDGTQdUMfx%2F76wqntdd3YxwsaJB16WVpRRSgncNjU02AB13eq5wskvSrQq7suy7fFrbjcbfU2tQ24AZuW7qQJ4xcJIT3AacVLcpfA37WESURJwR24ccFgUB%2BWTXkzaPrLpW%2BJk03B4v1DPWPeIYIf4JvxkRaI73mvl0ML1NFvyHD1t22bTG8ae%2BiNTLIkyKaYEmBxQ1lD7vdJp8oXR0TJW%2BTzxOMyKUsDAFEOKOKVmlR2Xzjq%2BgBW5ZzG5l3m8sKlgp0COo%3D; _ym_uid=1514186447680000922; Rfr=https%3A%2F%2Fyobit.net%2Fen%2F; locale=en; PHPSESSID=1d6podrq4h3733pj5032n31uh4; cf_clearance=e3b5006e91291b92cc7284d09f895e90334ca12e-1516590242-86400'
} 
    def stop(self):
        self.is_stop = True
        curses.endwin()
        print('stopped')

    def get_ticker(self):
        ticker_url = self.base_url+self.method[1]+'/'+'-'.join(self.trade_list)
        print(ticker_url)
        #self.stdscr = curses.initscr()
        #self.stdscr = curses.initscr()
        self.stdscr = curses.newwin(15, 80, 0, 80)
        #self.stdscr = curses.newpad(600, 800)
        curses.start_color()
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)

        while not self.is_stop:
            cur_pos_x = 2;
            req = urllib2.Request(ticker_url, headers=self.send_headers)
            try:
                res = urllib2.urlopen(req, timeout=5)
                page = res.read()
                json_obj = json.loads(page)
            except Exception,e:
                err =  'Get yobit data error, please set right cookies'
                self.stdscr.addstr(cur_pos_x,self.pos_y,err,curses.color_pair(3))
                self.stdscr.refresh()
                time.sleep(2)
                continue
            #print(page)
            self.stdscr.box(curses.ACS_VLINE, curses.ACS_HLINE)
            self.stdscr.addstr(cur_pos_x,self.pos_y,'Yobit', curses.color_pair(3))
            cur_pos_x += 1;
            self.stdscr.addstr(cur_pos_x,self.pos_y,time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()) ), curses.color_pair(3))
            cur_pos_x += 1;
            print_head =  "Symbol \tLast($) \tBuy \t\tSell"
            self.stdscr.addstr(cur_pos_x,self.pos_y,print_head,curses.color_pair(3))
            cur_pos_x += 1;
            for pair in self.trade_list:
                color_index = 1

                if pair in self.trade_list:
                    #print_content =  "sym:%7s \tprice:%10s \tper:%5s"%(json_obj[i]['symbol'], json_obj[i]['price_usd'], json_obj[i]['percent_change_24h']);
                    print_content =  "%7s \t%7.2f \t%7.2f \t%7.2f"%(pair, float(json_obj[pair]['last']), float(json_obj[pair]['buy']), float(json_obj[pair]['sell']));
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
    info = fetch_yobit()
    try:
        info.get_ticker()
    except KeyboardInterrupt as e:
        info.stop()
    

    

