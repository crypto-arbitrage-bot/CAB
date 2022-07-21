import json
import pandas as pd
import requests
import re
from abc import ABC, abstractmethod
from datetime import datetime

class APIOption(ABC):
  @abstractmethod
  def retrieve_data(self):
    pass

class CoinGecko(APIOption):
  # override abstract method retrieve_data()
  def retrieve_data(self):
    id_list = ['bitcoin-cash', 'ethereum', 'bitcoin','litecoin', 'eos','ripple','polkadot']
    vs_currencies_list = ['bch','eth','btc','ltc', 'eos','xrp','dot']
    base = 'https://api.coingecko.com/api/v3/simple/price?ids='       
    id_remaining = len(id_list)
    for coin in id_list:
        base += coin
        id_remaining -= 1
        if id_remaining > 0:
            base += ','
    base += '&vs_currencies='
    vs_remaining = len(vs_currencies_list)
    for vs in vs_currencies_list:
        base += vs
        vs_remaining -= 1
        if vs_remaining > 0:
            base += ','
    request = requests.get(base)  
    value = request.headers['Date']
    print(value)
    result = re.findall("\w\w\:\w\w\:\w\w", value)
    time = result[0]
    results_dict = json.loads(request.text)
    for coin in id_list:
        if(coin == 'bitcoin-cash'):
            results_dict[coin]= results_dict['bitcoin-cash']
            del results_dict[coin]
        if(coin == 'ethereum'):
            results_dict['eth'] = results_dict['ethereum']
            del results_dict[coin]
        if(coin == 'bitcoin'):
            results_dict['btc'] = results_dict['bitcoin']
            del results_dict[coin]
        if(coin == 'litecoin'):
            results_dict['ltc'] = results_dict['litecoin']
            del results_dict[coin]
        if(coin == 'ripple'):
            results_dict['xrp'] = results_dict['ripple']
            del results_dict[coin]
        if(coin == 'polkadot'):
            results_dict['dot'] = results_dict['polkadot']
            del results_dict[coin]
    #print(results_dict)
    
    return((time,results_dict))

class Coinbase(APIOption):
  # override abstract method retrieve_data()
  def retrieve_data(self):
    # https://api.coinbase.com/v2/prices/BTC-USD/spot
    # {"data":{"base":"BTC","currency":"USD","amount":"23128.76"}}
    
    symbol = ['BCH','ETH','BTC','LTC','EOS']
    
    price = []
    return_dict = {}
    
    for coin in symbol:
        return_dict[coin.lower()] = {}
        
    for coin in symbol:
        base = 'https://api.coinbase.com/v2/prices/'
        base += coin + '-USD/spot'
        # print(base)
        request = requests.get(base) 
        tmp = json.loads(request.text)
        price.append(float(tmp['data']['amount']))
    
    for coin in return_dict:
        for sub_coin in symbol:
            (return_dict[coin])[sub_coin.lower()] = price[symbol.index(coin.upper())] / price[symbol.index(sub_coin.upper())]
    
    request = requests.get("https://api.coinbase.com/v2/time")
    tmp = json.loads(request.text)
    time = float(tmp['data']['epoch'])
    time = datetime.utcfromtimestamp(time)
    timeString = ""
    if time.hour < 10: timeString += "0"
    timeString += str(time.hour)
    timeString += ":"
    if time.minute < 10: timeString += "0"
    timeString += str(time.minute)
    timeString += ":"
    if time.second < 10: timeString += "0"
    timeString += str(time.second)

    #print(return_dict)
    return ((timeString, return_dict))

class FTX(APIOption):
  # override abstract method retrieve_data()
  def retrieve_data(self):
    print("FTX retrieve_data()")

class Binance(APIOption):
  # override abstract method retrieve_data()
  def retrieve_data(self):
    # https://api.binance.com/api/v3/avgPrice?symbol=BTCUSDT
    list1 = ['BCH','ETH','BTC','LTC', 'EOS']
    for coin in list1:
        base = 'https://api.binance.com/api/v3/avgPrice?symbol='
        for coin1 in list1:
            if coin != coin1:
                base = base + coin + coin1
                request = requests.get(base) 
                results_dict = json.loads(request.text)
                print(results_dict)
    return 0

class KuCoin(APIOption):
  # https://api.kucoin.com/api/v1/market/histories?symbol=ETH-USDT
  # override abstract method retrieve_data()
  def retrieve_data(self):
    print("KuCoin retrieve_data()")

class Kraken(APIOption):
  # https://api.kraken.com/0/public/Trades?pair=BTCUSDT
  # override abstract method retrieve_data()
  def retrieve_data(self):
    print("Kraken retrieve_data()")

# driver code
apiOption = CoinGecko()
apiOption.retrieve_data()
apiOption = Coinbase()
apiOption.retrieve_data()