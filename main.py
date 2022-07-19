import sys
from api import API
from history import History
from computation import Computation
from tkinter import *
from tkinter import ttk
import pandas as pd

def update_table(table,data):
    # code for creating table
    count_row = data.shape[0]
    count_col = data.shape[1]
    for i in range(count_row):
        first_v =data['Time'].values[i]
        second_v = data['Exchange'].values[i]
        third_v = data['Path'].values[i]
        fourth_v = data['Profitability'].values[i]
        table.insert(parent='',index='end',iid=i,text='',values=(first_v,second_v,third_v,fourth_v))
        
    table.pack()
    table.update()
    
def running_click(table):
    print("Running clicked")
    api_obj = API()
    time = api_obj.myfunc() #get time from API
    history_obj = History()
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
        #print(complete_data)
    #history_obj.append_history(complete_data)
    update_table(table,complete_data)
    
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
    game_frame = Frame(tab1)
    game_frame.pack()
    #scrollbar
    game_scroll = Scrollbar(game_frame)
    game_scroll.pack(side=RIGHT, fill=Y)
    table1 = ttk.Treeview(game_frame,yscrollcommand=game_scroll.set)
    table1.pack()
    game_scroll.config(command=table1.yview)
    #define our column
    table1['columns'] = ('Time', 'Exchange', 'Profit Link', 'Profitibility')
    # format our column
    table1.column("#0", width=0,  stretch=NO)
    table1.column("Time",anchor=CENTER, width=80)
    table1.column("Exchange",anchor=CENTER,width=80)
    table1.column("Profit Link",anchor=CENTER,width=160)
    table1.column("Profitibility",anchor=CENTER,width=100)
    #Create Headings 
    table1.heading("#0",text="",anchor=CENTER)
    table1.heading("Time",text="Time",anchor=CENTER)
    table1.heading("Exchange",text="Exchange",anchor=CENTER)
    table1.heading("Profit Link",text="Profit Link",anchor=CENTER)
    table1.heading("Profitibility",text="Profitibility",anchor=CENTER)
    start_running_button = Button(tab1, text ="Start Running", command = running_click(table1))
    start_running_button.pack()
    table1.pack()
    
    table_frame2 = Frame(tab2)
    table_frame2.pack()
    #scrollbar
    game_scroll = Scrollbar(table_frame2)
    game_scroll.pack(side=RIGHT, fill=Y)
    table2 = ttk.Treeview(table_frame2,yscrollcommand=game_scroll.set)
    table2.pack()
    game_scroll.config(command=table2.yview)
    #define our column
    table2['columns'] = ('Time', 'Exchange', 'Profit Link', 'Profitibility')
    # format our column
    table2.column("#0", width=0,  stretch=NO)
    table2.column("Time",anchor=CENTER, width=80)
    table2.column("Exchange",anchor=CENTER,width=80)
    table2.column("Profit Link",anchor=CENTER,width=160)
    table2.column("Profitibility",anchor=CENTER,width=100)
    #Create Headings 
    table2.heading("#0",text="",anchor=CENTER)
    table2.heading("Time",text="Time",anchor=CENTER)
    table2.heading("Exchange",text="Exchange",anchor=CENTER)
    table2.heading("Profit Link",text="Profit Link",anchor=CENTER)
    table2.heading("Profitibility",text="Profitibility",anchor=CENTER)
    table2.pack()
    print("2 Tables created")
    
    window.mainloop()
    
def main():
    generate_gui()
    return 0

main()