# Crypto-trading-bot 
a crypto trading bot compatible with many main-stream exchanges. 

## Supported Cryptocurrency Exchange Markets
The library currently supports the following 98 cryptocurrency exchange markets and trading APIs:

Current supported crypto currency exchange:
coinmarketcap, poloniex, binance, huobi, yobit, kraken

#Environment
python 3+
# RUN
```
virtualenv -p python3 .
source ./bin/activate
pip install -r requirements.txt
python ./fetch_coinmarket_new.py
python3 ./stock_simu.py
deactivate
```

# Others
Stat all aset changed:
```
grep -n "asset changed" stock.log |awk -F ':' '{a=substr($5, 2, length($5)-4);print i ":"  a;sum+=a;i+=1} END{print "get all:" sum;}'
```
