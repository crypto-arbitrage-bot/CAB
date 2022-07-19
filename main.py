import sys
import tkinter
from api import API
from history import History
from computation import Computation
from tkinter import *
from tkinter import ttk
import pandas as pd

def update_table(window,data):
    # code for creating table
    for i in range(len(data)):
        for j in range(data):                
            e = Entry(window, width=20, fg='blue',
                            font=('Arial',16,'bold'))                
            e.grid(row=i, column=j)
            e.insert(END, data[i][j])
    e.pack()
    window.update()
    
def running_click(window):
    api_obj = API()
    time = api_obj.myfunc() #get time from API
    history_obj = History()
    history_obj.myfunc()
    computation_obj = Computation()
    computation_obj.generate_graph()
    exchange = "TEST EXCHANGE"
    data = computation_obj.scan_graph() #data hold link with profitibility
    complete_data = pd.DataFrame()
    for row in range(len(data)):
        full_data = {
            "Time": time,
            "Exchange": exchange,
            "Path": [data['Path'].values[row]],
            "Profitability": data['Result'].values[row]
        }
        full_data_df = pd.DataFrame(full_data)
        complete_data =pd.concat([complete_data, full_data_df])
        print(complete_data)
    #history_obj.append_history(complete_data)
    update_table(window,complete_data)
    
def generate_gui():
    window = Tk()
    window.title("CAB APPLICATION")
    window.configure(width=500, height=500)
    window.geometry("500x300")
    window.configure(bg='lightgray')

    # move window center
    
    tabControl = ttk.Notebook(window)
  
    tab1 = ttk.Frame(tabControl)
    tab2 = ttk.Frame(tabControl)
  
    tabControl.add(tab1, text ='Home')
    tabControl.add(tab2, text ='History')
    tabControl.pack(expand = 1, fill ="both")
  
   # ttk.Label(tab1, text ="HOME Content Here").grid(column = 0, row = 0,padx = 30,pady = 30)  
   # ttk.Label(tab2,text ="HISTORY Content Here").grid(column = 0,row = 0, padx = 30,pady = 30)
    start_running_button = tkinter.Button(tab1, text ="Start Running", command = running_click(window))
    start_running_button.pack()
    window.mainloop()
    
def main():
    generate_gui()
    return 0

main()