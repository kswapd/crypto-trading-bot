# Crypto-trading-bot 
A crypto trading bot compatible with many main-stream exchanges.

## Supported Cryptocurrency Exchange Markets
The library currently supports the following main stream cryptocurrency exchange markets and trading APIs:

Current supported crypto currency exchange:
coinmarketcap, poloniex, binance, huobi, yobit, kraken


## Get binance market quotations list.
```
virtualenv -p python3 .
source ./bin/activate
pip install -r requirements.txt
python3 ./binance_bot.py
deactivate
```
If you don't need proxy to connect to binance, comment out the line in binance_trading.py file:
```.python
#session.proxies.update(proxyDict2)
```



## Get coinmarketcap quotations list.
```
virtualenv -p python3 .
source ./bin/activate
pip install -r requirements.txt
python3 ./coinmarket_bot.py
deactivate
```
If you don't need proxy to connect to coinmarketcap, comment out the line in binance_trading.py file:
```.python
#session.proxies.update(proxyDict2)
```

## RUN stock simulation
```
virtualenv -p python3 .
source ./bin/activate
pip install -r requirements.txt
python3 ./stock_simu.py
deactivate
```
* You could get stock simulation datas in stock.log files as follows:
  ```.log
2021-06-07 14:52:01,314 Stock simu started......
2021-06-07 14:52:01,315 Get configure file.
2021-06-07 14:52:01,315 {'stock': {'day-duration': 100, 'price-step-unit': 0.05, 'stock-trade-unit': 200, 'stock-open-price': 10, 'sellA-index': 1.02, 'buyB-index': 1.01, 'buyC-index': 1.03, 'buyA-index': 0.98, 'sellB-index': 0.99, 'sellC-index': 0.97, 'loop-days': 0}, 'log': {'level': 'INFO', 'file-name': 'stock2.log'}}
2021-06-07 14:52:01,315 Stock market times: 1.
2021-06-07 14:52:01,315 Max duration:100
2021-06-07 14:52:01,315 1-1 current price:9.95, down
2021-06-07 14:52:01,315 auto_trade_stock start.
2021-06-07 14:52:02,316 1-2 current price:9.90, down
  ```
  
* Generate executable file:
```
pip install pyinstaller
pyinstaller -F ./stock_simu.py
```





# Others
Stat all asset changed:
```
grep -n "asset changed" stock.log |awk -F ':' '{a=substr($5, 2, length($5)-4);print i ":"  a;sum+=a;i+=1} END{print "get all:" sum;}'
```
