import pandas as pd
import os
from os.path import exists

class History:
    def __init__(self, filename="history"):
        self.history = pd.DataFrame(columns=["Time", "Exchange", "Path", "Profitability"])
        self.filename = filename
      
    def get_history(self):
        file_exists = exists(self.filename + ".xlsx")
        if(file_exists):
            data= pd.read_excel(self.filename + ".xlsx", sheet_name='a')
            self.history = pd.concat([self.history, data])
        return self.history
    
    def append_history(self, data):
        self.history = pd.concat([self.history, data])
        
    def export_history(self):
        file_exists = exists(self.filename + ".xlsx")
        if file_exists: os.remove(self.filename + ".xlsx")
        self.history.to_excel(self.filename + ".xlsx", sheet_name='a', index = False)

# for testing

#obj = History("history2")
#if(not obj.get_history().empty): print(str(obj.get_history()))

#data = {
#    "Time": 0.5,
#    "Exchange": "FTX",
#    "Path": [['a','b']],
#    "Profitability": 0.1
#}
#df = pd.DataFrame(data)
#obj.append_history(df)
#obj.append_history(df)
#print(str(obj.get_history()))
#obj.export_history()
#print("History exported")