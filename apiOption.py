from abc import ABC, abstractmethod

class APIOption(ABC):
  @abstractmethod
  def retrieve_data(self):
    pass

class CoinGecko(APIOption):
  # override abstract method retrieve_data()
  def retrieve_data(self):
    print("CoinGecko retrieve_data()")

class Coinbase(APIOption):
  # override abstract method retrieve_data()
  def retrieve_data(self):
    print("Coinbase retrieve_data()")

class FTX(APIOption):
  # override abstract method retrieve_data()
  def retrieve_data(self):
    print("FTX retrieve_data()")

class Binance(APIOption):
  # override abstract method retrieve_data()
  def retrieve_data(self):
    print("Binance retrieve_data()")

# driver code
# selected_option = 3
# apiOption = CoinGecko()
# if selected_option == 0: apiOption = CoinGecko()
# if selected_option == 1: apiOption = Coinbase()
# if selected_option == 2: apiOption = FTX()
# if selected_option == 3: apiOption = Binance()
# apiOption.retrieve_data()