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

    
    
    def coinbase(self):
        # https://api.coinbase.com/v2/prices/BTC-USD/spot
        # {"data":{"base":"BTC","currency":"USD","amount":"23128.76"}}
        
        symbol = ['BCH','ETH','BTC','LTC', 'EOS']
        
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
        
        print(return_dict)
        return return_dict

    
api = API()
api.coinbase()

#api.coinbase()



#def kucoin(self):
        # https://api.kucoin.com/api/v1/market/histories?symbol=ETH-USDT
    #return 0
#def kraken(self):
        # https://api.kraken.com/0/public/Trades?pair=BTCUSDT

    #return 0  

"""
def binance(self):
    # https://api.binance.com/api/v3/avgPrice?symbol=BTCUSDT
    symbol = ['BCH','ETH','BTC','LTC', 'EOS']
    full_symbol = ['bitcoin-cash', 'ethereum', 'bitcoin','litecoin', 'eos']
    
    price = []
    return_dict = {}
    
    for coin in full_symbol:
        return_dict[coin] = {}
    
    
    for coin in symbol:
        base = 'https://api.binance.com/api/v3/avgPrice?symbol='

        base = base + coin + 'USDT'
        request = requests.get(base) 
        tmp = json.loads(request.text)
        price.append(tmp['price'])

    print(tmp)
    print(price)
    print(return_dict)
    return 0
"""