#! /usr/bin/python
import configparser
import string, os, sys
class TradeKeys:
    def __init__(self):
        cf = configparser.ConfigParser()
        cf.read("keys.ini")
        kraken_public = cf.get("kraken", "public")
        kraken_secret = cf.get("kraken", "secret")
        poloniex_public = cf.get("poloniex", "public")
        poloniex_secret = cf.get("poloniex", "secret")
        huobi_public = cf.get("huobi", "public")
        huobi_secret = cf.get("huobi", "secret")
        self.keys_info = {
            'kraken':{'public':kraken_public,
                    'secret':kraken_secret
            },
            'poloniex':{'public':poloniex_public,
                    'secret':poloniex_secret
            },
            'huobi':{
                'public':huobi_public,
                'secret':huobi_secret
            },
            'binance':{
                'public':cf.get("binance", "public"),
                'secret':cf.get("binance", "secret")
            }
                        };
