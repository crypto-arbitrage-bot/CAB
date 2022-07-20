import json
import pandas as pd
import requests
import re
class API:
    def __init__(self):#include age as arguement
        print("API Constructor")
        #self.age = age Sets to global variable
      
    def get_time(self):
        return self.time
    def coingecko(self):
        id_list = ['bitcoin-cash', 'ethereum', 'bitcoin','litecoin', 'eos']
        vs_currencies_list = ['bch','eth','btc','ltc', 'eos']
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
        self.time = result[0]
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
        print(results_dict)
        
        return(results_dict)
    
    def binance(self):
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

api = API()
#api.coingecko()

api.binance()
