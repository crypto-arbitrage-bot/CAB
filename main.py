from select import select
import sys
import tkinter
from api import API
from history import History
from computation import Computation
from tkinter import *
from tkinter import ttk
import pandas as pd
        
def sel(num):
    selection = "You selected the option " + str(num)
    global selected_option 
    selected_option= num
    print(selection)
    
def hel(num):
    selection = "You selected the option " + str(num)
    global sort_option
    sort_option = num
    print(selection)
    
def history_tab_clicked(event):
    tab = event.widget.tab('current')['text']
    if tab =='History':
        print("History clicked")
        data = history_obj.get_history()
        update_table(table2,data)
    return
    
def update_table(table,data):
    # code for updating table
    #delete old data
    for i in table.get_children():
        table.delete(i)
    count_row = data.shape[0]
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
    global data
    data = api_obj.coingecko()    
    time = api_obj.get_time()        
    computation_obj = Computation(crypto_data=data)
    computation_obj.generate_graph()
    exchange = "TEST"
    if(selected_option == 1):
        exchange = "CoinGecko"
    if(selected_option == 2):
        exchange = "Coinbase"
    if(selected_option == 3):
        exchange = "FTX"
    if(selected_option == 4):
        exchange = "Binance"
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
    history_obj.append_history(complete_data)
    update_table(table,complete_data)
    return
    
    
    
data =[]
selected_option = 0
sort_option =0
api_obj = API()        
history_obj = History()
computation_obj = Computation()
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

var = IntVar()
R1 = Radiobutton(tab1, text="CoinGecko", variable=var, value=1,command=sel(1))
R1.pack( anchor = W )
R2 = Radiobutton(tab1, text="Coinbase", variable=var, value=2,command=sel(2))
R2.pack( anchor = W )
R3 = Radiobutton(tab1, text="FTX", variable=var, value=3,command=sel(3))
R3.pack( anchor = W)
R4 = Radiobutton(tab1, text="Binance", variable=var, value=4,command=sel(4))
R4.pack( anchor = W)
game_frame = Frame(tab1)

#scrollbar
game_scroll = Scrollbar(game_frame)
game_scroll.pack(side=RIGHT, fill=Y)
table1 = ttk.Treeview(game_frame,yscrollcommand=game_scroll.set,height=5)
start_running_button = Button(tab1, text ="Start Running", command = running_click(table1))
start_running_button.pack(anchor = E)
table1.pack()
game_frame.pack()
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
table1.pack()

#HISTORY TAB STUFF
#FILTERS
filters_frame = Frame(tab2)
sort_frame = Frame(filters_frame)    
sort_frame.pack(anchor = W,side='left')
var = IntVar()
sort1 = Radiobutton(sort_frame, text="Time", variable=var, value=1,command=hel(1))
sort1.pack( anchor = W )
sort2 = Radiobutton(sort_frame, text="Exchange", variable=var, value=2,command=hel(2))
sort2.pack( anchor = W )
sort3 = Radiobutton(sort_frame, text="Profitibility", variable=var, value=3,command=hel(3))
sort3.pack( anchor = W)
#Dates Within
dates_frame = Frame(filters_frame)    
dates_frame.pack(anchor = W,side='left')
date_type = IntVar()
date1 = Radiobutton(dates_frame, text="None", variable=date_type, value=1)
date1.pack( anchor = W )
date2 = Radiobutton(dates_frame, text="From Date To Date", variable=date_type, value=2)
date2.pack( anchor = W )
#ORDER
order_frame = Frame(filters_frame)    
order_frame.pack(anchor = W,side='left')
order_type = IntVar()
order1 = Radiobutton(order_frame, text="Ascending", variable=order_type, value=1)
order1.pack( anchor = W )
order2 = Radiobutton(order_frame, text="Descending", variable=order_type, value=2)
order2.pack( anchor = W )
filters_frame.pack()
#TABLE FRAME
table_frame2 = Frame(tab2)        
table_frame2.pack()
#scrollbar
game_scroll = Scrollbar(table_frame2)
game_scroll.pack(side=RIGHT, fill=Y)
table2 = ttk.Treeview(table_frame2,yscrollcommand=game_scroll.set,height=5)
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
export_history = Button(tab2, text ="Export History", command = history_obj.export_history())
export_history.pack()
print("2 Tables created")
tabControl.bind('<<NotebookTabChanged>>', history_tab_clicked)

window.mainloop()