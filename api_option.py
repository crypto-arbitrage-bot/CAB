"""
Holds the abstract APIOption class and its concrete implementations.
"""

import json
import re
from abc import ABC, abstractmethod
from datetime import datetime
import requests

class APIOption(ABC): # pylint: disable=too-few-public-methods
    """
    Abstract class for an API Option object.
    """
    @abstractmethod
    def retrieve_data(self):
        """
        The concrete implementation of this function returns a JSON object.
        """

class CoinGecko(APIOption): # pylint: disable=too-few-public-methods
    """
    A concrete implementation of the abstract APIOption class involving the CoinGecko API.
    """
    # override abstract method retrieve_data()
    def retrieve_data(self):
        """
        Retrieves market data from the CoinGecko API.
        """
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
        for vs_currency in vs_currencies_list:
            base += vs_currency
            vs_remaining -= 1
            if vs_remaining > 0:
                base += ','
        request = requests.get(base)
        value = request.headers['Date']
        result = re.findall(r"\w\w\:\w\w\:\w\w", value)
        time = result[0]
        results_dict = json.loads(request.text)
        for coin in id_list:
            if coin == 'bitcoin-cash':
                results_dict[coin]= results_dict['bitcoin-cash']
                del results_dict[coin]
            if coin == 'ethereum':
                results_dict['eth'] = results_dict['ethereum']
                del results_dict[coin]
            if coin == 'bitcoin':
                results_dict['btc'] = results_dict['bitcoin']
                del results_dict[coin]
            if coin == 'litecoin':
                results_dict['ltc'] = results_dict['litecoin']
                del results_dict[coin]
            if coin == 'ripple':
                results_dict['xrp'] = results_dict['ripple']
                del results_dict[coin]
            if coin == 'polkadot':
                results_dict['dot'] = results_dict['polkadot']
                del results_dict[coin]

        return((time,results_dict))

class Coinbase(APIOption): # pylint: disable=too-few-public-methods
    """
    A concrete implementation of the abstract APIOption class involving the Coinbase API.
    """
    # override abstract method retrieve_data()
    def retrieve_data(self):
        """
        Retrieves market data from the Coinbase API.
        """
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
        time_string = ""
        if time.hour < 10:
            time_string += "0"
        time_string += str(time.hour)
        time_string += ":"
        if time.minute < 10:
            time_string += "0"
        time_string += str(time.minute)
        time_string += ":"
        if time.second < 10:
            time_string += "0"
        time_string += str(time.second)

        return ((time_string, results_dict))

class FTX(APIOption): # pylint: disable=too-few-public-methods
    """
    A concrete implementation of the abstract APIOption class involving the FTX API.
    """
    # override abstract method retrieve_data()
    def retrieve_data(self): # pylint: disable=too-many-locals
        """
        Retrieves market data from the FTX API.
        """
        results_dict = {"eth":{"bch":99999,"eth":1.0,"btc":99999,"ltc":99999,"usd":99999},
        "usd":{"bch":99999,"eth":99999,"btc":99999,"ltc":99999,"usd":1.0},
        "ltc":{"bch":99999,"eth":99999,"btc":99999,"ltc":1.0,"usd":99999},
        "btc":{"bch":99999,"eth":99999,"btc":1.0,"ltc":99999,"usd":99999},
        "bch":{"bch":1.0,"eth":99999,"btc":99999,"ltc":99999,"usd":99999}}

        currencies_list = ['bch','eth','btc','ltc', 'usd']
        url = 'https://ftx.com/api/markets'
        markets = requests.get(url)
        value = markets.headers['Date']
        result = re.findall(r"\w\w\:\w\w\:\w\w", value)
        time = result[0]
        print(value)
        response = json.loads(markets.text)
        for i in range(0,len(response['result'])):
            for curr_index1, currency1 in enumerate(currencies_list):
                curr = currency1
                for curr_index2, currency2 in enumerate(currencies_list):
                    curr_ = curr + '/' + currency2
                    if response['result'][i]['name'] == (curr_.upper()):
                        result = response['result'][i]['price']
                        results_index1 = currencies_list[curr_index1]
                        results_index2 = currencies_list[curr_index2]
                        results_dict[results_index1][results_index2] = result
        for currency1 in currencies_list:
            for currency2 in currencies_list:
                if results_dict[currency1][currency2] == 99999:
                    usd1 = results_dict[currency1]['usd']
                    usd2 = results_dict[currency2]['usd']
                    result = usd1 / usd2
                    results_dict[currency1][currency2] = result

        print(results_dict)
        return ((time, results_dict))


class Binance(APIOption): # pylint: disable=too-few-public-methods
    """
    A concrete implementation of the abstract APIOption class involving the Binance API.
    """
    # override abstract method retrieve_data()
    def retrieve_data(self):
        """
        Retrieves market data from the Binance API.
        """
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
                if currency2 == currency:
                    continue
                base = "https://api.binance.com/api/v3/ticker/price?symbol="
                base += currency.upper()
                base += currency2.upper()
                request = requests.get(base)
                request_data = json.loads(request.text)
                if not 'code' in request_data:
                    exchange_rates[currency2] = float(request_data['price'])
                else:
                    exchange_rates[currency2] = 0.0
            results_dict[currency] = exchange_rates
        for currency in currencies_list:
            for currency2 in currencies_list:
                if results_dict[currency][currency2] == 0.0:
                    usd1 = usdt_prices[currency]
                    usd2 = usdt_prices[currency2]
                    results_dict[currency][currency2] = usd1 / usd2

        print(results_dict)

        request = requests.get("https://api.binance.com/api/v3/time")
        tmp = json.loads(request.text)
        time = float(str(tmp['serverTime'])[:-3])
        time = datetime.utcfromtimestamp(time)
        time_string = ""
        if time.hour < 10:
            time_string += "0"
        time_string += str(time.hour)
        time_string += ":"
        if time.minute < 10:
            time_string += "0"
        time_string += str(time.minute)
        time_string += ":"
        if time.second < 10:
            time_string += "0"
        time_string += str(time.second)

        return ((time_string, results_dict))

class KuCoin(APIOption): # pylint: disable=too-few-public-methods
    """
    A concrete implementation of the abstract APIOption class involving the KuCoin API.
    """
    # https://api.kucoin.com/api/v1/market/histories?symbol=ETH-USDT
    # override abstract method retrieve_data()
    def retrieve_data(self):
        """
        Retrieves market data from the KuCoin API.
        """
        print("KuCoin retrieve_data()")

class Kraken(APIOption): # pylint: disable=too-few-public-methods
    """
    A concrete implementation of the abstract APIOption class involving the Kraken API.
    """
    # https://api.kraken.com/0/public/Trades?pair=BTCUSDT
    # override abstract method retrieve_data()
    def retrieve_data(self):
        """
        Retrieves market data from the Kraken API.
        """
        print("Kraken retrieve_data()")

# driver code
# apiOption = CoinGecko()
# apiOption.retrieve_data()
# print()
# apiOption = Binance()
# apiOption.retrieve_data()
# apiOption = FTX()
# apiOption.retrieve_data()
