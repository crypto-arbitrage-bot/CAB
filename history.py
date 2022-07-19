import pandas as pd
import os

class History:
    def __init__(self, filename="history"):
        self.history = pd.DataFrame(columns=["Time", "Exchange", "Path", "Profitability"])
        self.filename = filename
      
    def get_history(self):
        return self.history
    
    def append_history(self, data):
        self.history = pd.concat([self.history, data])
        
    def export_history(self):
        os.remove(self.filename + ".xlsx")
        self.history.to_excel(self.filename + ".xlsx", sheet_name='a', index = False)

# for testing

# obj = History()
# if(not obj.get_history().empty): print(str(obj.get_history()))

# data = {
#     "Time": 0.5,
#     "Exchange": "FTX",
#     "Path": [['a','b']],
#     "Profitability": 0.1
# }
# df = pd.DataFrame(data)
# obj.append_history(df)
# obj.append_history(df)
# print(str(obj.get_history()))
# obj.export_history()
# print("History exported")