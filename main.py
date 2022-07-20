from select import select
import sys
import tkinter
from api import API
from history import History
from computation import Computation
from tkinter import *
from tkinter import ttk
import pandas as pd

class Main:
    def __init__(self):
        self.selected_option = 0
        self.api_obj = API()        
        self.history_obj = History()
        self.computation_obj = Computation()
        self.generate_gui()
        
    def sel(self,num):
        selection = "You selected the option " + str(num)
        self.selected_option = num
        print(selection)
        
    def hel(self,num):
        selection = "You selected the option " + str(num)
        self.sort_option = num
        print(selection)
    def update_table(self,table,data):
        # code for creating table
        count_row = data.shape[0]
        for i in range(count_row):
            first_v =data['Time'].values[i]
            second_v = data['Exchange'].values[i]
            third_v = data['Path'].values[i]
            fourth_v = data['Profitability'].values[i]
            table.insert(parent='',index='end',iid=i,text='',values=(first_v,second_v,third_v,fourth_v))
            
        table.pack()
        table.update()
        
    def running_click(self,table):
        print("Running clicked")       
        time = "03:30:23" #get from api
        self.computation_obj.generate_graph()
        exchange = "TEST EXCHANGE"
        data = self.computation_obj.scan_graph() #data hold link with profitibility
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
        self.history_obj.append_history(complete_data)
        self.update_table(table,complete_data)
        
    def generate_gui(self):
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
    
        self.var = IntVar()
        R1 = Radiobutton(tab1, text="API OPTION 1", variable=self.var, value=1,command=self.sel(1))
        R1.pack( anchor = W )
        R2 = Radiobutton(tab1, text="API OPTION 2", variable=self.var, value=2,command=self.sel(2))
        R2.pack( anchor = W )
        R3 = Radiobutton(tab1, text="API OPTION 3", variable=self.var, value=3,command=self.sel(3))
        R3.pack( anchor = W)
        R4 = Radiobutton(tab1, text="API OPTION 4", variable=self.var, value=4,command=self.sel(4))
        R4.pack( anchor = W)
        game_frame = Frame(tab1)
        
        #scrollbar
        game_scroll = Scrollbar(game_frame)
        game_scroll.pack(side=RIGHT, fill=Y)
        table1 = ttk.Treeview(game_frame,yscrollcommand=game_scroll.set,height=5)
        start_running_button = Button(tab1, text ="Start Running", command = self.running_click(table1))
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
        self.var = IntVar()
        sort1 = Radiobutton(sort_frame, text="Time", variable=self.var, value=1,command=self.hel(1))
        sort1.pack( anchor = W )
        sort2 = Radiobutton(sort_frame, text="Exchange", variable=self.var, value=2,command=self.hel(2))
        sort2.pack( anchor = W )
        sort3 = Radiobutton(sort_frame, text="Profitibility", variable=self.var, value=3,command=self.hel(3))
        sort3.pack( anchor = W)
        #Dates Within
        dates_frame = Frame(filters_frame)    
        dates_frame.pack(anchor = W,side='left')
        self.date_type = IntVar()
        date1 = Radiobutton(dates_frame, text="None", variable=self.date_type, value=1)
        date1.pack( anchor = W )
        date2 = Radiobutton(dates_frame, text="From Date To Date", variable=self.date_type, value=2)
        date2.pack( anchor = W )
        #ORDER
        order_frame = Frame(filters_frame)    
        order_frame.pack(anchor = W,side='left')
        self.order_type = IntVar()
        order1 = Radiobutton(order_frame, text="Ascending", variable=self.order_type, value=1)
        order1.pack( anchor = W )
        order2 = Radiobutton(order_frame, text="Descending", variable=self.order_type, value=2)
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
        export_history = Button(tab2, text ="Export History", command = self.history_obj.export_history())
        export_history.pack()
        print("2 Tables created")
        
        window.mainloop()

Main()