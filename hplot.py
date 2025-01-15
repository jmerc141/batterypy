# internal graph
import tkinter as tk
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.colors as mcolors
from tkinter import Frame, ttk
from collections import defaultdict
from enum import Enum
import sys, os, csv, json, settings

'''
Referencing plt will cause hanging


'''

class Window(Frame):
    def __init__(self, master = None):
        if sys.platform == 'win32':
            import s_probe
            self.sp = s_probe
        elif sys.platform == 'linux':
            import s_probe_l
            self.sp = s_probe_l

        self.current_sesh = 0
        self.lines = []
        self.stackplots = []
        self.color = ''

        #try:
        self.readCsv()
        #except FileNotFoundError as e:
        #    print('Error reading csv file', e)
        #    return

        #try:
        self.init_graph(master)
        #except Exception as e:
        #    print('Error with hplot', e)


    def init_graph(self, master):
        tl = tk.Toplevel(master)
        Frame.__init__(self, tl)
        self.master = master
        
        self.internal_dpi = 65

        self.configure(bg='#2f2f2f', highlightbackground='blue', highlightthickness=3)

        topFrame = ttk.Frame(self)
        bottomFrame = ttk.Frame(self)

        session_times = []

        self.sel = tk.StringVar(self)

        # Get starting times for each session
        for a in self.hdata:
            session_times.append(self.hdata[a][0][0])    
        
        dd = ttk.OptionMenu(topFrame, self.sel, session_times[0], *session_times, command=self.change_sesh)
        
        self.sel2 = tk.StringVar(self)
        self.graphs = ['Graph1', 'Graph2', 'Graph3']
        dd2 = ttk.OptionMenu(topFrame, self.sel2, self.graphs[0], *self.graphs, command=self.change_info)
        
        # Pack elements
        ttk.Label(topFrame, text='Session: ').pack(side='left', padx=(0,5))
        dd.pack(side='left', padx=(0,10))
        ttk.Label(topFrame, text='Info: ').pack(side='left', padx=(10,5))
        dd2.pack(side='left')

        topFrame.pack()

        # Grid Frame to window
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        #self.grid(row=0, column=0, sticky='nesw')
        bottomFrame.pack(expand=True, fill='both')

        self.i_fig = plt.Figure(facecolor='#f0f0f0', figsize=(9,8), dpi=self.internal_dpi)
        self.i_fig.subplots_adjust(bottom=0.07, top=0.975, left=0.07, right=0.975)
        #self.i_fig.tight_layout()

        self.ax = self.i_fig.add_subplot(111)
        self.ax.autoscale(enable=True)

        self.setup_white()

        self.change_info('Graph1')

        self.canvas = FigureCanvasTkAgg(self.i_fig, master=bottomFrame)
        self.canvas.get_tk_widget().pack(side='top', anchor='n', padx=10, expand=True, fill='both')

        self.pack(expand=True, fill='both')



    def setup_white(self):
        self.ax.set_xlabel('Time', color='black', fontsize=16)
        self.ax.set_ylabel('Voltage (V)', color='black', fontsize=16)
        self.ax.grid(color='black')
        self.ax.set_xlabel('Seconds', color='white')
        self.ax.set_ylabel('Power', color='white')
        self.ax.set_facecolor('#2f2f2f')
        self.ax.spines['bottom'].set_color('white')
        self.ax.spines['top'].set_color('white')
        self.ax.spines['right'].set_color('white')
        self.ax.spines['left'].set_color('white')
        self.ax.tick_params(axis='x', colors='white')
        self.ax.tick_params(axis='y', colors='white')
        self.ax.grid(color='white')
        self.i_fig.set_facecolor('#2f2f2f')


    '''
        Read csv file into memory
        key = session number, value = array of readings
    '''
    def readCsv(self):
        self.hdata = defaultdict(list)
        with open(settings.s['filename'], 'r') as f:
            csvFile = csv.reader(f)
            #csvDict = csv.DictReader(f)

            # Skip header, dont include session_num column
            self.headers = next(csvFile, None)[1:]

            # Each line is x chunks of readings
            for l in csvFile:
                self.hdata[l[0]].append(l[1:])
                
        #print(self.hdata, len(self.hdata))


    def change_sesh(self, e):
        #self.current_sesh = e-1
        self.ax.cla()
        self.lined()
        #self.canvas.draw()


    def change_info(self, e):
        self.ax.cla()
        self.setup_white()
        self.lines.clear()

        #print(mcolors.CSS4_COLORS)
        match e:
            case 'Graph1':
                self.fancy_line(self.get_session_el2(self.headers.index('voltage')), 'red')
                self.fancy_line(self.get_session_el2(self.headers.index('amps')), 'blue')
                self.fancy_line(self.get_session_el2(self.headers.index('watts')), 'gold')
                # Inlcude number in legend?
                self.ax.legend([self.lines[0][0], self.lines[1][0], self.lines[2][0]], [f'Volts ', 'Amps', 'Watts'])
            case 'Graph2':
                self.fancy_line(self.get_session_el2(self.headers.index('measured_Ah')), 'salmon')
                self.fancy_line(self.get_session_el2(self.headers.index('rem_Ah')), 'orange')
                print(self.lines)
                self.ax.legend([self.lines[0][0], self.lines[1][0]], [f'Measured_Ah', 'Remaining_Ah'])
            case 'Graph3':
                self.fancy_line(self.get_session_el2(self.headers.index('measured_Wh')), 'yellowgreen')
                self.fancy_line(self.get_session_el2(self.headers.index('rem_Wh')), 'green')
                print(self.lines)
                self.ax.legend([self.lines[0][0], self.lines[1][0]], [f'Measured_Wh', 'Remaining_Wh'])
                
        
        self.i_fig.canvas.draw()


    def fancy_line(self, x, c):
        if len(self.lines) == 0:
            y = [*range(len(x))]
            #self.ax.xaxis.set_ticks(y)
            self.ax.xaxis.set_ticklabels([x.split('|')[1] for x in self.get_session_el2(InfoOrder.CurrentTime.value)])
        self.lines.append(self.ax.plot(x, color=c, linewidth=2, marker='o'))
        self.stackplots.append(self.ax.stackplot(range(0, len(x)), x, color=c, alpha=0.2, labels=[]))
        

    def get_session_el2(self, i: int):
        lst = []
        if i == InfoOrder.CurrentTime.value:
            for v in self.hdata[str(self.current_sesh)]:
                lst.append(v[i])
        else:
            for v in self.hdata[str(self.current_sesh)]:
                lst.append(float(v[i]))
        return lst



    # Destroys graph element
    def Clear(self):
        self.destroy()



    def add_toolbar(self) -> None:
        # Optional toolbar
        self.toolbar = NavigationToolbar2Tk(self.canvas, self, pack_toolbar=False)
        self.toolbar.config(background='#2f2f2f', highlightbackground='#2f2f2f')
        self.toolbar._message_label.config(background='#2f2f2f')#, highlightbackground='#2f2f2f')
        self.toolbar.update()
        self.toolbar.pack(side='bottom', expand=False)
        

class InfoOrder(Enum):
    CurrentTime = 0
    Health = 1
    Full_Wh = 2
    Measured_Ah = 3
    Measured_Wh = 4
    Remain_Ah = 5
    Remain_Wh = 6
    Capacity_Diff = 7
    Voltage = 8
    Amps = 9
    Watts = 10
    Charge = 11
