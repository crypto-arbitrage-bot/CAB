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
    
    return((time,results_dict))

class Coinbase(APIOption):
  # override abstract method retrieve_data()
    def retrieve_data(self):
        currencies_list = ['bch','eth','btc','ltc','eos','xrp','dot']

        results_dict = {}

        for currency in currencies_list:
            base = 'https://api.coinbase.com/v2/exchange-rates?currency='
            base += currency
            request = requests.get(base)
            request_data = json.loads(request.text)
            exchange_rates = {}
            for currency2 in currencies_list:
                currency2 = currency2.upper()
                exchange_rates[currency2.lower()] = float(request_data['data']['rates'][currency2])

            results_dict[currency] = exchange_rates

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

        return ((timeString, results_dict))

class FTX(APIOption):
  # override abstract method retrieve_data()
  def retrieve_data(self):
    results_dict = {"eth":{"bch":99999,"eth":1.0,"btc":99999,"ltc":99999,"usd":99999},"usd":{"bch":99999,"eth":99999,"btc":99999,"ltc":99999,"usd":1.0},"ltc":{"bch":99999,"eth":99999,"btc":99999,"ltc":1.0,"usd":99999},"btc":{"bch":99999,"eth":99999,"btc":1.0,"ltc":99999,"usd":99999},"bch":{"bch":1.0,"eth":99999,"btc":99999,"ltc":99999,"usd":99999}}
    currencies_list = ['bch','eth','btc','ltc', 'usd']
    url = 'https://ftx.com/api/markets'
    markets = requests.get(url)
    value = markets.headers['Date']
    result = re.findall("\w\w\:\w\w\:\w\w", value)
    time = result[0]
    print(value)
    response = json.loads(markets.text)
    for i in range(0,len(response['result'])):
        for x in range(0,len(currencies_list)):
            curr = currencies_list[x]
            for y in range(0,len(currencies_list)):
                curr_ = curr + '/' + currencies_list[y]
                if(response['result'][i]['name'] == (curr_.upper())):
                    results_dict[currencies_list[x]][currencies_list[y]] = response['result'][i]['price']
    for j in range(0,len(currencies_list)):
        for r in range(0,len(currencies_list)):
            if(results_dict[currencies_list[j]][currencies_list[r]] == 99999):
                results_dict[currencies_list[j]][currencies_list[r]] = results_dict[currencies_list[j]]['usd']/results_dict[currencies_list[r]]['usd']

    print(results_dict)
    return ((time, results_dict))

class Binance(APIOption):
  # override abstract method retrieve_data()
    def retrieve_data(self):
        currencies_list = ['bch','eth','ltc','eos','xrp','dot']
        results_dict = {}
        usdt_prices = {}
        for currency in currencies_list:
            exchange_rates = {}
            exchange_rates[currency] = 1.0
            base = "https://api.binance.com/api/v3/ticker/price?symbol=" + currency.upper() + "USDT"
            request = requests.get(base)
            request_data = json.loads(request.text)
            usdt_prices[currency] = float(request_data["price"])
            for currency2 in currencies_list:
                if currency2 == currency: continue
                base = "https://api.binance.com/api/v3/ticker/price?symbol="
                base += currency.upper()
                base += currency2.upper()
                request = requests.get(base)
                request_data = json.loads(request.text)
                if not 'code' in request_data: exchange_rates[currency2] = float(request_data['price'])
                else: exchange_rates[currency2] = 0.0
            results_dict[currency] = exchange_rates
        for currency in currencies_list:
            for currency2 in currencies_list:
                if results_dict[currency][currency2] == 0.0:
                    results_dict[currency][currency2] = usdt_prices[currency] / usdt_prices[currency2]

        print(results_dict)

        request = requests.get("https://api.binance.com/api/v3/time")
        tmp = json.loads(request.text)
        time = float(str(tmp['serverTime'])[:-3])
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

        return ((timeString, results_dict))

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
# apiOption = CoinGecko()
# apiOption.retrieve_data()
# print()
# apiOption = Binance()
# apiOption.retrieve_data()
# apiOption = FTX()
# apiOption.retrieve_data()