#! /usr/bin/python
#-*-coding:utf-8-*- 
import urllib.request
import json
import sys, time
import _thread
import logging
import sched, time
import random
from datetime import datetime
import yaml

def print_time(sc, a='default'):
    logging.info("From print_time", time.time(), a)
    sc.enter(2, 1, print_time, (sc,a))
def print_time2(a='default'):
    logging.info("From print_time2", time.time(), a)
#def cur_random_price(delta_value=1):

class timer_loop():
    
    def __init__(self, interval, duration, func, *args):
        self.interval = interval
        self.duration = duration
        self.func = func
        self.param = args
        self.run = False
        
        self.schedule = sched.scheduler(time.time, time.sleep)
        #self.schedule.enter(self.interval, 1, self.event_func,())
        #self.schedule.run()
        self.start_time = time.time()
        self.end_time = time.time()
        self.is_stop = False
        #self.event_func()
    def event_func(self):
        #logging.info("ddddd:", self.param)
        self.end_time = time.time()
        self.func(self.param)
        #logging.info("time:%.2f,%d", self.end_time - self.start_time, self.duration)
        if self.end_time - self.start_time > self.duration or self.is_stop:
            #self.schedule.cancel(self.event)
            return
        self.event = self.schedule.enter(self.interval, 1, self.event_func,())
        #if not self.run:
        #    self.schedule.run()
        #    self.run = True
    def start(self):
        self.event_func()
        #self.thread = _thread.start_new_thread(self.event_func,())
        self.thread = _thread.start_new_thread(self.sched_start,())
        #self.schedule.run()
    def stop(self):
        self.is_stop = True
    def sched_start(self):
        self.schedule.run()
    #td1 = _thread.start_new_thread( start_coin_market,('55',2) )
class stock_market():
    def __init__(self, cfg):
        self.is_stop = False
        self.coin_url = "https://coinmarketcap.com/"
        self.duration = cfg['stock']['day-duration']
        self.cur_price = cfg['stock']['stock-open-price']
        self.base_price = cfg['stock']['stock-open-price']
        self.stock_hold =  cfg['stock']['stock-trade-unit']
        self.cur_money = 0.0
        self.price_change_count = 1
        self.change_stock_unit = cfg['stock']['stock-trade-unit']
        self.change_price_unit = cfg['stock']['price-step-unit']
        self.max_change_price_percent = cfg['stock']['max-change-percent']
        sellAIndex = cfg['stock']['sellA-index']
        buyBIndex = cfg['stock']['buyB-index']
        buyCIndex = cfg['stock']['buyC-index']

        buyAIndex = cfg['stock']['buyA-index']
        sellBIndex = cfg['stock']['sellB-index']
        sellCIndex = cfg['stock']['sellC-index']
        #卖出价A
        self.sellA = round(self.cur_price*sellAIndex,2)
        #赚钱买入价B
        self.buyB = round(self.cur_price*buyBIndex,2)
        #补仓买入价C
        self.buyC = round(self.cur_price*buyCIndex,2)
        #补仓买入价D
        self.buyD = round(self.cur_price,2)
        #买入价A
        self.buyA = round(self.cur_price*buyAIndex,2)
        #赚钱卖出价B
        self.sellB = round(self.cur_price*sellBIndex,2)
        #补仓卖出价C
        self.sellC = round(self.cur_price*sellCIndex,2)
        #补仓卖出价D
        self.sellD = round(self.cur_price,2)

        self.status = 'init'

        

        self.changeList = []
        logging.info("Max duration:%d", self.duration)
    def auto_trade_stock(self):
        self.thread2 = _thread.start_new_thread(self.auto_trade_stock_thrd,())
    def auto_trade_stock_thrd(self):
        logging.info("auto_trade_stock start.")
        global g_market_cur_time
        global g_all_changed_asset
        while not self.is_stop:
            cur = time.time()
            curStr = datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
            #logging.info("auto_trade_stock start loop. %s",self.status)
            if self.status == 'init':
                #if self.cur_price >= self.sellA:
                if self.cur_price == self.sellA:
                    self.status = 'sellA'
                    changed_money = round(self.cur_price * self.change_stock_unit,2)
                    self.changeList.append((curStr, 'sell', self.status, self.cur_price, -1*self.change_stock_unit, changed_money))
                    self.stock_hold -= self.change_stock_unit
                    self.cur_money += changed_money
                    logging.info("%d-%d Sell by sellA price %.2f .", g_market_cur_time, self.price_change_count, self.sellA)

                #elif self.cur_price <= self.buyA:
                elif self.cur_price == self.buyA:
                    self.status = 'buyA'
                    changed_money = -1*round(self.cur_price * self.change_stock_unit,2)
                    self.changeList.append((curStr, 'buy', self.status, self.cur_price, self.change_stock_unit, changed_money))
                    self.stock_hold += self.change_stock_unit
                    self.cur_money += changed_money
                    logging.info("%d-%d Buy by buyA price %.2f .", g_market_cur_time, self.price_change_count, self.buyA)

            elif self.status == 'sellA':
                #if self.cur_price <= self.buyB:
                if self.cur_price == self.buyB:
                    self.status = 'buyB'
                    changed_money = -1*round(self.cur_price * self.change_stock_unit,2)
                    self.changeList.append((curStr, 'buy', self.status, self.cur_price, self.change_stock_unit, changed_money))
                    self.stock_hold += self.change_stock_unit
                    self.cur_money += changed_money
                    self.status = 'finish'
                    assetChanged = round(self.changeList[0][-1]  + self.changeList[1][-1],2)
                    g_all_changed_asset += assetChanged
                    logging.info("%d-%d Trade finished today, asset changed: %.2f, all changed: %.2f", g_market_cur_time, self.price_change_count, assetChanged,g_all_changed_asset)
                    logging.info("%d-%d Trading flow:", g_market_cur_time, self.price_change_count)
                    for i in self.changeList:
                        logging.info(i)
                #elif self.cur_price <= self.buyC:
                elif self.cur_price == self.buyC:
                    self.status = 'buyC'
                    changed_money = -1*round(self.cur_price * self.change_stock_unit,2)
                    self.changeList.append((curStr, 'buy', self.status, self.cur_price, self.change_stock_unit, changed_money))
                    self.stock_hold += self.change_stock_unit
                    self.cur_money += changed_money
                    self.status = 'finish'
                    assetChanged = round(self.changeList[0][-1]  + self.changeList[1][-1],2)
                    g_all_changed_asset += assetChanged
                    logging.info("%d-%d Trade finished today, asset changed: %.2f, all changed: %.2f", g_market_cur_time, self.price_change_count, assetChanged,g_all_changed_asset)
                    logging.info("%d-%d Trading flow:", g_market_cur_time, self.price_change_count)
                    for i in self.changeList:
                        logging.info(i)
                # Closing market in 2 seconds:
                elif cur - self.start_time >= self.duration - 2:
                    self.status = 'buyD'
                    changed_money = -1*round(self.cur_price * self.change_stock_unit,2)
                    self.changeList.append((curStr, 'buy', self.status, self.cur_price, self.change_stock_unit, changed_money))
                    self.stock_hold += self.change_stock_unit
                    self.cur_money += changed_money
                    self.status = 'finish'
                    assetChanged = round(self.changeList[0][-1]  + self.changeList[1][-1],2)
                    g_all_changed_asset += assetChanged
                    logging.info("%d-%d Trade finished today, asset changed: %.2f, all changed: %.2f", g_market_cur_time, self.price_change_count, assetChanged,g_all_changed_asset)
                    logging.info("%d-%d Trading flow:", g_market_cur_time, self.price_change_count)
                    for i in self.changeList:
                        logging.info(i)
            
            
            elif self.status == 'buyA':
                #if self.cur_price >= self.sellB:
                if self.cur_price == self.sellB:
                    self.status = 'sellB'
                    changed_money = round(self.cur_price * self.change_stock_unit,2)
                    self.changeList.append((curStr, 'sell', self.status, self.cur_price, -1*self.change_stock_unit, changed_money))
                    self.stock_hold -= self.change_stock_unit
                    self.cur_money += changed_money
                    self.status = 'finish'
                    assetChanged = round(self.changeList[0][-1]  + self.changeList[1][-1],2)
                    g_all_changed_asset += assetChanged
                    logging.info("%d-%d Trade finished today, asset changed: %.2f, all changed: %.2f", g_market_cur_time, self.price_change_count, assetChanged,g_all_changed_asset)
                    logging.info("%d-%d Trading flow:", g_market_cur_time, self.price_change_count)
                    for i in self.changeList:
                        logging.info(i)
                #elif self.cur_price >= self.sellC:
                elif self.cur_price == self.sellC:
                    self.status = 'sellC'
                    changed_money = round(self.cur_price * self.change_stock_unit,2)
                    self.changeList.append((curStr, 'sell', self.status, self.cur_price, -1*self.change_stock_unit, changed_money))
                    self.stock_hold -= self.change_stock_unit
                    self.cur_money += changed_money
                    self.status = 'finish'
                    assetChanged = round(self.changeList[0][-1]  + self.changeList[1][-1],2)
                    g_all_changed_asset += assetChanged
                    logging.info("%d-%d Trade finished today, asset changed: %.2f, all changed: %.2f", g_market_cur_time, self.price_change_count, assetChanged,g_all_changed_asset)
                    logging.info("%d-%d Trading flow:", g_market_cur_time, self.price_change_count)
                    for i in self.changeList:
                        logging.info(i)
                # Closing market in 2 seconds:
                elif cur - self.start_time >= self.duration - 2:
                    self.status = 'sellD'
                    changed_money = round(self.cur_price * self.change_stock_unit,2)
                    self.changeList.append((curStr, 'sell', self.status, self.cur_price, -1*self.change_stock_unit, changed_money))
                    self.stock_hold -= self.change_stock_unit
                    self.cur_money += changed_money
                    self.status = 'finish'
                    assetChanged = round(self.changeList[0](-1)  + self.changeList[1](-1),2)
                    g_all_changed_asset += assetChanged
                    logging.info("%d-%d Trade finished today, asset changed: %.2f, all changed: %.2f", g_market_cur_time, self.price_change_count, assetChanged,g_all_changed_asset)
                    logging.info("%d-%d Trading flow:", g_market_cur_time, self.price_change_count)
                    for i in self.changeList:
                        logging.info(i)

            elif self.status == 'finish':
                #logging.info("Trading finished..") 
                self.stop()
                pass  
            else:
                logging.info("No trading here..")      
            time.sleep(0.1)
        logging.info("auto_trade_stock finished.")
    def print_time3(self, a='default'):
        logging.info("From print_time3,%s,%s", time.time(), a)
    def change_stock_price(self, delta_value=1):
        flag = 'up'
        if bool(random.getrandbits(1)):
            self.cur_price += self.change_price_unit
        else:
            flag = 'down'
            self.cur_price -= self.change_price_unit
        self.cur_price = round(self.cur_price,2)
        logging.info("%d-%d current price:%.2f, %s", g_market_cur_time, self.price_change_count, self.cur_price, flag)
        self.price_change_count += 1

    def change_stock_price_by_percent(self, delta_value=1):
        flag = 'up'
        ref_price = self.cur_price
        cur_delta = (self.cur_price - self.base_price) / self.base_price
        probability_delta = cur_delta/self.max_change_price_percent*0.5
        cur_random = 0.5 + probability_delta
        cur_random = 0 if cur_random<0 else 1 if cur_random>1 else cur_random
        if random.random() > cur_random:
            self.cur_price += self.change_price_unit
        else:
            flag = 'down'
            self.cur_price -= self.change_price_unit
        self.cur_price = round(self.cur_price,2)
        #logging.info("%d-%d current probability:%.2f,%.2f,%s", g_market_cur_time, self.price_change_count,self.cur_price, 1-cur_random, flag)
        logging.info("%d-%d current price:(%.2f->%.2f, %s), up pb:%.2f", g_market_cur_time, self.price_change_count, ref_price, self.cur_price, flag, 1-cur_random)
        self.price_change_count += 1
    def stop(self):
        self.is_stop = True
        self.stock_market.stop()
        logging.info('stopped')  
    def start(self):
        self.start_time = time.time()  
        self.stock_market = timer_loop(1, self.duration, self.change_stock_price_by_percent)
        self.stock_market.start()
        
        self.auto_trade_stock()

        while not self.is_stop:
            if time.time() - self.start_time > self.duration:
                self.stop()
            else:
                pass    
            time.sleep(1)
        time.sleep(1)

g_market_cur_time = 1
g_all_changed_asset = 0

if __name__ == "__main__":
    #logging.basicConfig(format='%(asctime)s %(message)s')
    with open("stock.yml", "r") as ymlfile:
        cfg = yaml.load(ymlfile)
    print('Get configure file.', cfg)
    if cfg['log']['level'] == 'INFO':
        logLevel = logging.INFO
    elif cfg['log']['level'] == 'WARN':
        logLevel = logging.WARN
    elif cfg['log']['level'] == 'ERROR':
        logLevel = logging.ERROR
    elif cfg['log']['level'] == 'DEBUG':
        logLevel = logging.DEBUG  
    else:
        logLevel = logging.INFO       
    logging.basicConfig(format='%(asctime)s %(message)s', filename=cfg['log']['file-name'], level=logLevel)
    logging.info('Stock simu started......')
    logging.info('Get configure file.')
    logging.info(cfg)
    #logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)
    #logging.basicConfig(filename='./stock.log')
    #stock_simu = stock_market(duration=10)
    if cfg['stock']['loop-days'] < 1: 
        while True:
            logging.info('Stock market times: %d.', g_market_cur_time)
            stock_simu = stock_market(cfg)
            try:
                stock_simu.start()
            except KeyboardInterrupt as e:
                stock_simu.stop()
                logging.info('Stock simu loop finished by key......')
            g_market_cur_time += 1
    else:
        loop_days = cfg['stock']['loop-days']
        while loop_days > 0:
            logging.info('Stock market times: %d.', g_market_cur_time)
            stock_simu = stock_market(cfg)
            try:
                stock_simu.start()
            except KeyboardInterrupt as e:
                stock_simu.stop()
                logging.info('Stock simu finished by key......')
            g_market_cur_time += 1
            loop_days -= 1
        logging.info('Stock simu finished......')
    
    
    

    

