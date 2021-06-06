#! /usr/bin/python
#-*-coding:utf-8-*- 
import urllib.request
import json
import sys, time
import curses
import console_view as cv
import requests
import _thread
import logging
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import sched, time
import random
from datetime import datetime
session = requests.Session()
retry = Retry(connect=3, backoff_factor=0.5)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)

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

        #self.event_func()
    def event_func(self):
        #logging.info("ddddd:", self.param)
        self.end_time = time.time()
        self.func(self.param)
        #logging.info("time:%.2f,%d", self.end_time - self.start_time, self.duration)
        if self.end_time - self.start_time > self.duration and self.schedule and self.event:
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
    def sched_start(self):
        self.schedule.run()
    #td1 = _thread.start_new_thread( start_coin_market,('55',2) )
class stock_market():
    def __init__(self, duration=5, cur_price=10.00, hold=100):
        self.is_stop = False
        self.num = 50
        self.pos_y = 2 
        self.coin_url = "https://coinmarketcap.com/"
        self.duration = duration
        self.cur_price = cur_price
        self.stock_hold = hold
        self.cur_money = 0.0
        self.change_stock_unit = 100
        self.change_price_unit = 0.05
        #卖出价A
        self.sellA = round(self.cur_price*1.02,2)
        #赚钱买入价B
        self.buyB = round(self.cur_price*1.01,2)
        #补仓买入价C
        self.buyC = round(self.cur_price*1.03,2)
        #补仓买入价D
        self.buyD = round(self.cur_price,2)
        #买入价A
        self.buyA = round(self.cur_price*0.98,2)
        #赚钱卖出价B
        self.sellB = round(self.cur_price*0.99,2)
        #补仓卖出价C
        self.sellC = round(self.cur_price*0.97,2)
        #补仓卖出价D
        self.sellD = round(self.cur_price,2)

        self.status = 'init'

        

        self.changeList = []

        logging.info("duration:%d", self.duration)
        
        #b = timer_loop(3, self.duration, self.print_time3)
        #b.start()
    def auto_trade_stock(self):
        self.thread2 = _thread.start_new_thread(self.auto_trade_stock_thrd,())
    def auto_trade_stock_thrd(self):
        logging.info("auto_trade_stock start. %s",self.is_stop)
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
                #elif self.cur_price <= self.buyA:
                elif self.cur_price == self.buyA:
                    self.status = 'buyA'
                    changed_money = -1*round(self.cur_price * self.change_stock_unit,2)
                    self.changeList.append((curStr, 'buy', self.status, self.cur_price, self.change_stock_unit, changed_money))
                    self.stock_hold += self.change_stock_unit
                    self.cur_money += changed_money
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
                    logging.info("Trade finished today, asset changed: %.2f .", assetChanged)
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
                    logging.info("Trade finished today, asset changed: %.2f .", assetChanged)
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
                    logging.info("Trade finished today, asset changed: %.2f .", assetChanged)
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
                    logging.info("Trade finished today, asset changed: %.2f .", assetChanged)
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
                    logging.info("Trade finished today, asset changed: %.2f .", assetChanged)
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
                    logging.info("Trade finished today, asset changed: %.2f .", assetChanged)
                    for i in self.changeList:
                        logging.info(i)

            elif self.status == 'finish':
                #logging.info("Trading finished..")  
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
        logging.info("current price:%.2f, %s", self.cur_price, flag)
    def stop(self):
        self.is_stop = True
        logging.info('stopped')  
    def start(self):
        self.start_time = time.time()  
        a = timer_loop(1, self.duration, self.change_stock_price)
        a.start()
        
        self.auto_trade_stock()

        while not self.is_stop:
            if time.time() - self.start_time > self.duration:
                self.stop()
            else:
                pass    
            time.sleep(1)
        time.sleep(3)
if __name__ == "__main__":
    #logging.basicConfig(format='%(asctime)s %(message)s')
    #logging.basicConfig(format='%(asctime)s %(message)s', filename='./stock.log', level=logging.INFO)
    logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)
    #logging.basicConfig(filename='./stock.log')
    logging.warning('Started')
    stock_simu = stock_market(duration=100)

    try:
        stock_simu.start()
    except KeyboardInterrupt as e:
        stock_simu.stop()
    

    

