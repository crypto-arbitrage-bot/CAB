# pylint: disable=invalid-name
# pylint: disable=global-statement
"""
Handles the GUI part of the application and transfers data between the APIs, Computation, and
History parts of the application.
"""

from http import server
import json
from pyexpat import version_info
from tkinter import * # pylint: disable=wildcard-import, unused-wildcard-import
from tkinter import ttk
import pandas as pd
from api import API
from history import History
from computation import Computation
import requests

def api_click():
    """
    Handles API selection clicks.
    """
    selection = "You selected the option " + str(api_var.get())
    global selected_option
    selected_option = int(api_var.get())
    print(selection)

def export_history_click():
    """
    Handles export history clicks.
    """
    history_obj.export_history()

def print_msg(msg):
    """
    Prints a message to the user.
    """
    win = Toplevel(window)
    label = Label(win, text = msg)
    label.pack(anchor=CENTER)
    win.mainloop()
    
def check_version():
    """
    Handles check version clicks.
    """
    request = requests.get("https://cab-version.herokuapp.com/version")
    
    server_version = json.loads(request.text)
    print(server_version)
    if(server_version['version'] == version):
        print_msg("Version is up to date")
    else:
        print_msg("Version is outdated.Please update through our website")
        
def history_filter_click():
    """
    Handles history filter clicks.
    """
    global data
    if sort_type.get() == 1:
        print("Sort by time")
        data = history_obj.get_history().sort_values(by='Time', ascending=order_type.get())
    if sort_type.get() == 2:
        print("Sort by Exchange")
        data = history_obj.get_history().sort_values(by='Exchange',ascending=order_type.get())
    if sort_type.get() == 3:
        print("Sort by Profitability")
        data = history_obj.get_history().sort_values(by='Profitability', ascending=order_type.get())
    history_update_table(data)

def history_tab_clicked(event):
    """
    Handles history tab clicks.
    """
    global data
    tab = event.widget.tab('current')['text']
    if tab =='History':
        print("History clicked")
        data = history_obj.get_history()
        history_update_table(data)

def history_update_table(data_obj):
    """
    Updates the history table.
    """
    for i in table2.get_children():
        table2.delete(i)
    count_row = data_obj.shape[0]
    if(count_row > 500):
        count_row = 500
    for i in range(count_row):
        first_v = data_obj['Time'].values[i]
        second_v = data_obj['Exchange'].values[i]
        third_v = data_obj['Path'].values[i]
        fourth_v = data_obj['Profitability'].values[i]
        table2.insert(parent='', index='end', iid=i, text='',
        values=(first_v,second_v,third_v,fourth_v))

    table2.pack()
    table2.update()

def running_update_table(data_obj):
    """
    Updates the table on the Home tab.
    """

    for i in table1.get_children():
        table1.delete(i)
    count_row = data_obj.shape[0]
    for i in range(count_row):
        first_v = data_obj['Time'].values[i]
        second_v = data_obj['Exchange'].values[i]
        third_v = data_obj['Path'].values[i]
        fourth_v = data_obj['Profitability'].values[i]
        table1.insert(parent='', index='end', iid=i, text='',
        values=(first_v,second_v,third_v,fourth_v))

    table1.pack()
    table1.update()

def running_click():
    """
    Handles start running clicks.
    """
    print("Running clicked")
    global data, api_obj, computation_obj
    api_obj = API(selected_option)
    full_data = api_obj.get_data()
    time = full_data[0]
    data = full_data[1]
    print(data)
    computation_obj = Computation(crypto_data=data)
    computation_obj.generate_graph()
    exchange = "None"
    if selected_option == 1:
        exchange = "CoinGecko"
    if selected_option == 2:
        exchange = "Coinbase"
    if selected_option == 3:
        exchange = "FTX"
    if selected_option == 4:
        exchange = "Binance"
    data = computation_obj.scan_graph() #data hold link with profitibility
    complete_data = pd.DataFrame()
    if(len(data)==0):
       print_msg("No profitable trades found")
    else:
        for row in range(len(data)):
            full_data = {
                "Time": time,
                "Exchange": exchange,
                "Path": [data['Path'].values[row]],
                "Profitability": data['Result'].values[row]
            }
            full_data_df = pd.DataFrame(full_data)
            complete_data =pd.concat([complete_data, full_data_df])
        history_obj.append_history(complete_data)
    running_update_table(complete_data)

def update_theme():
    """
    Updates the GUI's current theme.
    - Switches to Dark Mode when current theme is Light Mode
    - Switches to Light Mode when current theme is Dark Mode
    """
    global bgColor, textColor, themeButtonImage, darkMode, themeButton # pylint: disable=global-variable-not-assigned

    # update global variables
    if darkMode is False:
        bgColor = '#292929'
        textColor = 'white'
        darkMode = True
    else:
        bgColor = 'white'
        textColor = 'black'
        darkMode = False

    # update TFrame style
    style.configure('TFrame', background=bgColor)

    # update TButton style
    style.configure('TButton', background=bgColor, foreground=textColor)
    if darkMode is False:
        style.map('TButton',
        background=[('pressed', '#e8e8e8'),
                    ('active', '#e8e8e8')],
        foreground=[('pressed', 'black'),
                    ('active', 'black')]
        )
    else:
        style.map('TButton',
        background=[('pressed', '#333333'),
                    ('active', '#333333')],
        foreground=[('pressed', 'white'),
                    ('active', 'white')]
        )

    # update TRadiobutton style
    style.configure('TRadiobutton', background=bgColor, foreground=textColor)
    if darkMode is False:
        style.map('TRadiobutton',
        background=[('pressed', '#e8e8e8'),
                    ('active', '#e8e8e8')],
        foreground=[('pressed', 'black'),
                    ('active', 'black')]
        )
    else:
        style.map('TRadiobutton',
        background=[('pressed', '#333333'),
                    ('active', '#333333')],
        foreground=[('pressed', 'white'),
                    ('active', 'white')]
        )

    # Update Treeview style
    style.configure('Treeview', background=bgColor,
    foreground=textColor, fieldbackground=bgColor)

    style.configure('Treeview.Heading', background=bgColor,
    foreground=textColor, fieldbackground=bgColor)

    if darkMode is False:
        style.map('Treeview.Heading',
        background=[('pressed', '#e8e8e8'),
                    ('active', '#e8e8e8')],
        foreground=[('pressed', 'black'),
                    ('active', 'black')]
        )
    else:
        style.map('Treeview.Heading',
        background=[('pressed', '#333333'),
                    ('active', '#333333')],
        foreground=[('pressed', 'white'),
                    ('active', 'white')]
        )

    # update TNotebook style
    style.configure('TNotebook', background=bgColor)
    style.configure('TNotebook.Tab', background=bgColor, foreground=textColor)
    if darkMode is False:
        style.map('TNotebook.Tab',
        background=[('pressed', '#e8e8e8'),
                    ('active', '#e8e8e8')],
        foreground=[('pressed', 'black'),
                    ('active', 'black')]
        )
    else:
        style.map('TNotebook.Tab',
        background=[('pressed', '#333333'),
                    ('active', '#333333')],
        foreground=[('pressed', 'white'),
                    ('active', 'white')]
        )

    # update ThemeButton style
    if darkMode is False:
        style.configure("ThemeButton.TButton", background="white")
        style.map('ThemeButton.TButton',
            background=[('pressed', 'white'),
                        ('active', 'white')])
        themeButtonImage = PhotoImage(file = "dark_mode.png")
        themeButton['image'] = themeButtonImage
    else:
        style.configure("ThemeButton.TButton", background='#333333')
        style.map('ThemeButton.TButton',
            background=[('pressed', '#333333'),
                        ('active', '#333333')])
        themeButtonImage = PhotoImage(file = "light_mode.png")
        themeButton['image'] = themeButtonImage

    # update window style
    window.configure(bg=bgColor)

data =[]
selected_option = 1
sort_option = 0
api_obj = API(selected_option)
history_obj = History()
computation_obj = Computation()
darkMode = True
bgColor = ''
textColor = ''
themeButtonImage = ''
version = 0.5
window = Tk()
window.title("The Crypto Arbitrage Bot")
window.configure(width=600, height=400)
window.geometry("600x400")
window.configure(bg=bgColor)

# move window center

tabControl = ttk.Notebook(window)

style = ttk.Style()
style.theme_use('default')

windowExists = True

topWindowFrame = ttk.Frame(window)
topWindowFrame.pack(side=TOP, anchor=W)

# theme button
themeButton = ttk.Button(topWindowFrame, command = update_theme,
style="ThemeButton.TButton", image=themeButtonImage)

themeButton['cursor'] = 'hand2'
themeButton.pack(side=LEFT, padx=10, pady=10)

update_theme()

# check version button
versionButton = ttk.Button(topWindowFrame, command = check_version,text="Check Version")
versionButton['cursor'] = 'hand2'
versionButton.pack(side=LEFT, pady=10)

tab1 = ttk.Frame(tabControl)
tab2 = ttk.Frame(tabControl)

tabControl.add(tab1, text ='Home')
tabControl.add(tab2, text ='History')
tabControl.pack(expand = 1, fill ="both")

api_var = IntVar()
R1 = ttk.Radiobutton(tab1, text="CoinGecko", variable=api_var, value=1,command=api_click)
R1.pack( anchor = W, padx=10, pady=(10,0) )
R1['cursor'] = 'hand2'
R2 = ttk.Radiobutton(tab1, text="Coinbase", variable=api_var, value=2,command=api_click)
R2.pack( anchor = W, padx=10)
R2['cursor'] = 'hand2'
R3 = ttk.Radiobutton(tab1, text="FTX", variable=api_var, value=3,command=api_click)
R3.pack( anchor = W, padx=10)
R3['cursor'] = 'hand2'
R4 = ttk.Radiobutton(tab1, text="Binance", variable=api_var, value=4,command=api_click)
R4.pack( anchor = W, padx=10)
R4['cursor'] = 'hand2'
game_frame = Frame(tab1)

#scrollbar
game_scroll = ttk.Scrollbar(game_frame)
game_scroll.pack(side=RIGHT, fill=Y)
table1 = ttk.Treeview(game_frame,yscrollcommand=game_scroll.set,height=5)
start_running_button = ttk.Button(tab1, text ="Retrieve Data", command = running_click)
start_running_button['cursor'] = 'hand2'
start_running_button.pack(anchor = CENTER, pady=(0,10))
table1.pack()
game_frame.pack()
game_scroll.config(command=table1.yview)
#define our column
table1['columns'] = ('Time', 'Exchange', 'Profit Link', 'Profitibility')
# format our column
table1.column("#0", width=0,  stretch=NO)
table1.column("Time",anchor=CENTER, width=160)
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
table1['cursor'] = 'hand2'

#HISTORY TAB STUFF
#FILTERS
filters_frame = ttk.Frame(tab2)
sort_frame = ttk.Frame(filters_frame)
sort_frame.pack(anchor = W,side='left')
sort_type = IntVar()
sort1 = ttk.Radiobutton(sort_frame, text="Time", variable=sort_type, value=1,command=history_filter_click)
sort1.pack( anchor = W, pady=(10,0) )
sort1['cursor'] = 'hand2'
sort2 = ttk.Radiobutton(sort_frame, text="Exchange", variable=sort_type, value=2,command=history_filter_click)
sort2.pack( anchor = W )
sort2['cursor'] = 'hand2'
sort3 = ttk.Radiobutton(sort_frame, text="Profitibility", variable=sort_type, value=3,command=history_filter_click)
sort3.pack( anchor = W, pady=(0,10))
sort3['cursor'] = 'hand2'
#Dates Within
dates_frame = ttk.Frame(filters_frame)
dates_frame.pack(anchor = W,side='left')
#ORDER
order_frame = ttk.Frame(filters_frame)
order_frame.pack(anchor = W,side='right')
order_type = BooleanVar()
order1 = ttk.Radiobutton(order_frame, text="Ascending",
variable=order_type, value=True,command=history_filter_click)

order1.pack( anchor = W )
order1['cursor'] = 'hand2'
order2 = ttk.Radiobutton(order_frame, text="Descending",
variable=order_type, value=False,command=history_filter_click)

order2.pack( anchor = W )
order2['cursor'] = 'hand2'
filters_frame.pack()
#TABLE FRAME
table_frame2 = ttk.Frame(tab2)
table_frame2.pack()
#scrollbar
game_scroll = ttk.Scrollbar(table_frame2)
game_scroll.pack(side=RIGHT, fill=Y)
table2 = ttk.Treeview(table_frame2,yscrollcommand=game_scroll.set,height=5)
table2.pack()
table2['cursor'] = 'hand2'
game_scroll.config(command=table2.yview)
#define our column
table2['columns'] = ('Time', 'Exchange', 'Profit Link', 'Profitibility')
# format our column
table2.column("#0", width=0,  stretch=NO)
table2.column("Time",anchor=CENTER, width=160)
table2.column("Exchange",anchor=CENTER,width=80)
table2.column("Profit Link",anchor=CENTER,width=160)
table2.column("Profitibility",anchor=CENTER,width=120)
#Create Headings
table2.heading("#0",text="",anchor=CENTER)
table2.heading("Time",text="Time",anchor=CENTER)
table2.heading("Exchange",text="Exchange",anchor=CENTER)
table2.heading("Profit Link",text="Profit Link",anchor=CENTER)
table2.heading("Profitibility",text="Profitibility",anchor=CENTER)
table2.pack()
export_history = ttk.Button(tab2, text ="Export History", command = export_history_click)
export_history['cursor'] = 'hand2'
export_history.pack(pady=10)
print("2 Tables created")
tabControl.bind('<<NotebookTabChanged>>', history_tab_clicked)

window.mainloop()
