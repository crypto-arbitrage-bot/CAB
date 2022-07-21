import json
import pandas as pd
import requests
import re
from apiOption import *

class API:
    def __init__(self, selected_option = 0):
        self.selected_option = selected_option
      
    def get_time(self):
        return self.time
    def coingecko(self):
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
            if(coin == 'ripple'):
                results_dict['xrp'] = results_dict['ripple']
                del results_dict[coin]
            if(coin == 'polkadot'):
                results_dict['dot'] = results_dict['polkadot']
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

    def coinbase(self):
        # https://api.coinbase.com/v2/prices/BTC-USD/spot
        # {"data":{"base":"BTC","currency":"USD","amount":"23128.76"}}
        list1 = ['BCH','ETH','BTC','LTC', 'EOS']
        for coin in list1:
            base = 'https://api.coinbase.com/v2/prices/'
            base += coin + '-USD/spot'
            request = requests.get(base) 
            results_dict = json.loads(request.text)
        # price_list = [xxx, xxx, xxx, xxx, xxx]


        print(results_dict)


        return 0

    #def kucoin(self):
            # https://api.kucoin.com/api/v1/market/histories?symbol=ETH-USDT
        #return 0
    #def kraken(self):
            # https://api.kraken.com/0/public/Trades?pair=BTCUSDT

        #return 0    

    def get_data(self):
        apiOption = self.create_api_option()
        return apiOption.retrieve_data()

    def create_api_option(self):
        apiOption = CoinGecko()
        if self.selected_option == 0: apiOption = CoinGecko()
        if self.selected_option == 1: apiOption = Coinbase()
        if self.selected_option == 2: apiOption = FTX()
        if self.selected_option == 3: apiOption = Binance()

        return apiOption

# driver code
# obj = API(3)
# obj.get_data()
