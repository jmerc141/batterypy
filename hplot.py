# internal graph
import tkinter as tk
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from tkinter import Frame, ttk
from collections import defaultdict
from enum import Enum
import sys, os, csv, json, settings

'''
Referencing plt will cause hanging,

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



    '''
        Read csv file into memory
        key = session number, value = array of readings
    '''
    def readCsv(self):
        self.hdata = defaultdict(list)
        with open(settings.s['filename'], 'r') as f:
            csvFile = csv.reader(f)
            #csvDict = csv.DictReader(f)

            # Skip header
            self.headers = next(csvFile, None)[2:]

            # Each line is x chunks of readings
            for l in csvFile:
                self.hdata[l[0]].append(l[1:])
                
        #print(self.hdata, len(self.hdata))


    def change_sesh(self, e):
        self.current_sesh = e-1
        self.ax.cla()
        self.lined()
        #self.canvas.draw()

    def change_info(self, e):
        print(e)


    def lined(self, enum: Enum, color: str):
        self.lines.append(self.ax.plot(self.get_session_element(enum), label=enum, color=color, linewidth=2))


    def init_graph(self, master):
        tl = tk.Toplevel(master)
        Frame.__init__(self, tl)
        self.master = master

        self.internal_dpi = 65

        self.configure(bg='#2f2f2f')

        topFrame = ttk.Frame(self)

        self.sel = tk.StringVar(self)
        sesh_options = [*range(len(self.hdata))]
        dd = ttk.OptionMenu(topFrame, self.sel, sesh_options[0], *sesh_options, command=self.change_sesh)
        
        self.headers.insert(0, 'power')
        self.sel2 = tk.StringVar(self)
        dd2 = ttk.OptionMenu(topFrame, self.sel2, self.headers[0], *self.headers, command=self.change_info)
        

        ttk.Label(topFrame, text='Session: ').pack(side='left')
        dd.pack(side='left')
        ttk.Label(topFrame, text='Info: ').pack(side='left')
        dd2.pack(side='left')

        topFrame.pack()

        # Grid Frame to window
        self.grid(row=0, column=2)

        self.i_fig = plt.Figure(facecolor='#f0f0f0', figsize=(8,8), dpi=self.internal_dpi)
        self.i_fig.subplots_adjust(bottom=0.07, top=0.975, left=0.09, right=0.975)

        self.prop = 'Power'
        self.x = [0]
        self.y = [0]

        self.ax = self.i_fig.add_subplot(111)

        self.ax.set_xlabel('Seconds', color='black', fontsize=16)
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

        # Define graph title
        self.title = self.ax.text(0.5, 0.95, 'Title', bbox={'facecolor': 'w', 'alpha': 0.5, 'pad': 5}, 
                                transform=self.ax.transAxes, ha='center', fontsize=16, color='white')

        self.title.set_text('Power')

        self.x = self.get_session_element(InfoOrder.Voltage)
        self.y = [*range(len(self.x))]
        self.ax.xaxis.set_ticks(self.y)
        self.ax.xaxis.set_ticklabels([x.split('|')[1] for x in self.get_session_element(InfoOrder.CurrentTime)])

        self.ax.set_xlim(0, len(self.x))
        self.ax.set_ylim(-1, max(self.x)+2)

        self.l1 = self.ax.plot(self.x, self.y, color='red', linewidth=7)
        self.s1 = self.ax.stackplot(range(0, len(self.x)), self.x, color='red', alpha=0.2)

        self.canvas = FigureCanvasTkAgg(self.i_fig, master=self)
        self.canvas.get_tk_widget().pack(side='top', anchor='n', padx=10, expand=True, fill='both')


    '''
    
    '''
    def get_session_element(self, enum: Enum):
        lst = []
        if enum == InfoOrder.CurrentTime:
            for t in self.hdata[str(self.current_sesh)]:
                lst.append(t[enum.value])
        else:
            for v in self.hdata[str(self.current_sesh)]:
                lst.append(float(v[enum.value]))
            
        return lst


    # Destroys graph element
    def Clear(self):
        self.destroy()


    def set_prop(self, batprop):
        self.ax.cla()
        self.x = [0]
        self.y = [0]
        self.maxY = 0
        self.minY = 100
        self.tick = 0
        
        self.prop = batprop
        self.yl = ''

        if self.prop == 'Amperage':
            tmp = self.amps
            self.l1, = self.ax.plot(self.x, self.y, color='c')
            self.yl = 'Amperage (A)'
        if self.prop == 'Voltage':
            tmp = self.volts
            self.l1, = self.ax.plot(self.x, self.y, color='red')
            self.yl = 'Voltage (V)'
        if self.prop == 'Discharge Power':
            tmp = self.disch
            self.l1, = self.ax.plot(self.x, self.y, color='m')
            self.yl = 'Discharge Power (W)'
        if self.prop == 'Charge Power':
            tmp = self.charg
            self.l1, = self.ax.plot(self.x, self.y, color='orange')
            self.yl = 'Charge Power (W)'
        if self.prop == 'All':
            pass
        
        
        self.ax.set_ylabel(self.yl, color='white')
        self.ax.grid(color='white')
        self.title = self.ax.text(0.5, 0.95, '', bbox={'facecolor': 'w', 'alpha': 0.5, 'pad': 5}, 
                                transform=self.ax.transAxes, ha='center', fontsize=20, color='white')
        

        self.ax.set_xlim(0, 60)
        self.ax.set_ylim(0, tmp + 1)
        self.y = [tmp]
        self.canvas.draw()


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
