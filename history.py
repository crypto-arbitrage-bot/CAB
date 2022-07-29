"""
Holds the History class.
"""
from os.path import exists
import pandas as pd
from pathlib import Path
import os


class History:
    """
    Manages the computation history of the application. Keeps a running track of all profitable
    links.
    """
    def __init__(self, filename = "history"):
        """
        Initializes the History class with a filename (that the history will export to).
        """
        self.history = pd.DataFrame(columns=["Time", "Exchange", "Path", "Profitability"])
        self.filename = filename

    def get_history(self):
        """
        Gets the history from the history file, along with the current data.
        """
        file_exists = exists(self.filename + ".xlsx")
        print("Get history")
        if file_exists:
            data= pd.read_excel(self.filename + ".xlsx", sheet_name='a')
            self.history = pd.concat([self.history, data])
        return self.history

    def append_history(self, data):
        """
        Adds new data to the history.
        """
        self.history = pd.concat([self.history, data])
        self.history.to_excel(self.filename + ".xlsx", sheet_name='a', index = False)
        print("Append history")

    def export_history(self):
        """
        Saves the current history to a file in the downloads folder.
        """
        print("Export history")
        print(self.history)
        path_to_download_folder = str(os.path.join(Path.home(), "Downloads"))
        self.history.to_excel(path_to_download_folder + "/" + self.filename + ".xlsx", sheet_name='a', index = False)
        

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
