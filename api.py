"""
Holds the API class.
"""

from apiOption import CoinGecko, Coinbase, FTX, Binance, KuCoin, Kraken

class API:
    """
    Manages the various APIs used for the program.
    """
    def __init__(self, selected_option = 0):
        """
        Initializes the class using a selected API option.
        """
        self.selected_option = selected_option

    def create_api_option(self):
        """
        Creates and stores a concrete implementation of the abstract APIOption class, using the
        selected option passed through the initializer.
        """
        api_option = CoinGecko()
        if self.selected_option == 1:
            api_option = CoinGecko()
        if self.selected_option == 2:
            api_option = Coinbase()
        if self.selected_option == 3:
            api_option = FTX()
        if self.selected_option == 4:
            api_option = Binance()
        if self.selected_option == 5:
            api_option = KuCoin()
        if self.selected_option == 6:
            api_option = Kraken()

        return api_option

    def get_data(self):
        """
        Calls the retrieve_data() function on the created concrete implemention of the abstract
        APIOption class and returns the data returned by that function.
        """
        api_option = self.create_api_option()
        return api_option.retrieve_data()

# driver code
# obj = API(3)
# obj.get_data()
