from apiOption import *

class API:
    def __init__(self, selected_option = 0):
        self.selected_option = selected_option
      
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