import tkinter as tk
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
from tkinter import Frame, ttk
from collections import defaultdict
from enum import Enum
import csv, settings

'''
Eventually collect probes_full_Wh and do linear regression to see how quickly battery degrades over time

Referencing plt will cause hanging
'''

class Window(Frame):
    def __init__(self, master = None):
        self.selected_sesh = 0
        self.lines = []
        self.stackplots = []
        self.color = ''

        try:
            if self.readCsv() == 0:
                tk.messagebox.showerror('Error', f'No data in csv file\nEnable tracking!')
                return
        except FileNotFoundError as e:
            tk.messagebox.showerror('Error', f'Cannot find csv file\n{e}')
            return

        self.avg_c_pph = self.avg_d_pph = 0
        
        self.init_graph(master)
        #self.add_toolbar()


    '''
        Initializes the figure and all UI elements
    '''
    def init_graph(self, master):
        tl = tk.Toplevel(master)
        Frame.__init__(self, tl)
        self.master = master
        
        self.internal_dpi = 65

        self.configure(bg='#2f2f2f')#, highlightbackground='blue', highlightthickness=3)

        topFrame = ttk.Frame(self)
        bottomFrame = ttk.Frame(self)

        self.session_times = []

        # Get starting times for each session
        for a in self.hdata:
            self.session_times.append(self.hdata[a][0][0].replace('|', ' - '))

        rst = ttk.Button(topFrame, text='Reset View', command=self.reset_view)

        self.sel = tk.StringVar(self)
        dd = ttk.OptionMenu(topFrame, self.sel, self.session_times[0], *self.session_times, command=self.change_sesh)
        
        self.sel2 = tk.StringVar(self)
        self.graphs = ['Power', 'Capacity', 'Extra', 'Charge Percent']
        dd2 = ttk.OptionMenu(topFrame, self.sel2, self.graphs[0], *self.graphs, command=self.change_info)
        
        # Pack elements
        ttk.Label(topFrame, text='Session: ').pack(side='left', padx=(0,5))
        dd.pack(side='left', padx=(0,10))
        ttk.Label(topFrame, text='Info: ').pack(side='left', padx=(10,5))
        dd2.pack(side='left')
        rst.pack(side='left', padx=(20,0))

        topFrame.pack()

        # Grid Frame to window
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        bottomFrame.pack(expand=True, fill='both')

        self.i_fig = plt.Figure(facecolor='#f0f0f0', figsize=(10,9), dpi=self.internal_dpi)
        self.i_fig.subplots_adjust(bottom=0.07, top=0.975, left=0.07, right=0.975)
        #self.i_fig.tight_layout()

        self.ax = self.i_fig.add_subplot(111)
        #self.ax.autoscale(enable=True)
        
        self.canvas = FigureCanvasTkAgg(self.i_fig, master=bottomFrame)
        self.canvas.get_tk_widget().pack(side='top', anchor='n', padx=10, expand=True, fill='both')

        self.setup_white()

        # Default to first graph
        self.change_info(self.graphs[0])

        # For clikcing, dragging, and zooming
        self.canvas.mpl_connect('scroll_event', self.zoom)
        self.canvas.mpl_connect('motion_notify_event', self.pan)
        self.canvas.mpl_connect('button_press_event', self.lclick)

        self.pack(expand=True, fill='both')


    '''
        Sets the graph x and y label, gridlines and text to white
    '''
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
        #print(self.hdata)
        return len(self.hdata)


    '''
        Runs on session dropdown click
    '''
    def change_sesh(self, e):
        self.selected_sesh = self.session_times.index(e)
        self.ax.cla()
        self.setup_white()
        self.lines.clear()

        self.change_info(self.graphs[self.graphs.index(self.sel2.get())])
        
        self.i_fig.canvas.draw()


    '''
        Runs on info dropdown click, changes data displayed in graph
    '''
    def change_info(self, e):
        self.ax.cla()
        self.setup_white()
        self.lines.clear()

        #print(mcolors.CSS4_COLORS)
        if e in self.graphs:
            if e == self.graphs[0]:
                self.fancy_line(self.get_session_el2(self.headers.index('voltage')), 'red')
                self.fancy_line(self.get_session_el2(self.headers.index('amps')), 'blue')
                self.fancy_line(self.get_session_el2(self.headers.index('watts')), 'gold')
                # Inlcude number in legend?
                self.ax.legend([self.lines[0][0], self.lines[1][0], self.lines[2][0]], [f'Volts ', 'Amps', 'Watts'], fontsize=18)
            elif e == self.graphs[1]:
                self.fancy_line(self.get_session_el2(self.headers.index('measured_Ah')), 'salmon')
                self.fancy_line(self.get_session_el2(self.headers.index('rem_Ah')), 'orange')
                self.fancy_line(self.get_session_el2(self.headers.index('measured_Wh')), 'yellowgreen')
                self.fancy_line(self.get_session_el2(self.headers.index('rem_Wh')), 'green')

                # Average watt-hour per minute, * 60 to get per hour
                avgwh_min = (float(self.hdata[str(self.selected_sesh)][-1][InfoOrder.Remain_Wh.value]) \
                    - float(self.hdata[str(self.selected_sesh)][0][InfoOrder.Remain_Wh.value])) / (len(self.hdata[str(self.selected_sesh)]) / 60)
                
                avgah_min = (float(self.hdata[str(self.selected_sesh)][-1][InfoOrder.Remain_Ah.value]) \
                    - float(self.hdata[str(self.selected_sesh)][0][InfoOrder.Remain_Ah.value])) / (len(self.hdata[str(self.selected_sesh)]) / 60)

                self.ax.legend([self.lines[0][0], self.lines[1][0], self.lines[2][0], self.lines[3][0]], 
                               ['Measured_Ah', f'Remaining_Ah {avgah_min:.2f}/m', 'Measured_Wh', f'Remaining_Wh {avgwh_min:.2f}/m'], fontsize=18)
            elif e == self.graphs[2]:
                
                self.ax.legend([self.lines[0][0], self.lines[1][0]], [f'Measured_Wh', 'Remaining_Wh'])
            elif e == self.graphs[3]:
                avgm = avgh = ''
                sesh = self.hdata[str(self.selected_sesh)]
                lminutes = len(sesh) / 60
                lhours = lminutes / 60
                # If session starts with charging, get the first and last reading and divide by length
                if self.hdata[str(self.selected_sesh)][0][InfoOrder.Charging.value] == 'True':
                    avgm = f'{(int(sesh[-1][InfoOrder.Charge.value]) - int(sesh[0][InfoOrder.Charge.value])) / lminutes:.2f}%'
                    avgh = f'{(int(sesh[-1][InfoOrder.Charge.value]) - int(sesh[0][InfoOrder.Charge.value])) / lhours:.2f}%'
                elif self.hdata[str(self.selected_sesh)][0][InfoOrder.Charging.value] == 'False':
                    avgm = f'{(int(sesh[0][InfoOrder.Charge.value]) - int(sesh[-1][InfoOrder.Charge.value])) / lminutes:.2f}%'
                    avgm = f'{(int(sesh[0][InfoOrder.Charge.value]) - int(sesh[-1][InfoOrder.Charge.value])) / lhours:.2f}%'
                
                # Plot linear regression line
                line = self.get_session_el2(self.headers.index('chrg_percent'))
                self.fancy_line(line, 'lightblue')
                self.add_lin_reg(line)
                self.ax.legend([self.lines[0][0]], [f'%/m {avgm}\n%/h {avgh}'], fontsize=18)


            self.ogx = self.ax.get_xlim()
            self.ogy = self.ax.get_ylim()

            self.i_fig.canvas.draw()
        else:
            tk.messagebox.showerror('Error', f'Selected graph is not in self.graphs')


    def add_lin_reg(self, xdata):
        x = np.arange(len(xdata))
        m, b = np.polyfit(x, xdata, 1)
        y = m*x+b
        self.lines.append(self.ax.plot(x, y, 'dodgerblue', linestyle='dashed'))




        



    '''
        Adds a line and stackplot to the graph
        x: array of elements to be graphed (should be int or float)
        c: color of the line3
    '''
    def fancy_line(self, x, c):
        #print(x)
        if len(self.lines) == 0:
            tmpx = np.arange(len(x))
            self.ax.xaxis.set_ticks(tmpx)
            self.ax.locator_params(axis='x', nbins=10)
            self.ax.set_xlim(0, tmpx[-1]-1)
            self.ax.xaxis.set_ticklabels([x.split('|')[1] for x in self.get_x_tick_labels()])
        self.lines.append(self.ax.plot(x, color=c, linewidth=1))
        self.stackplots.append(self.ax.stackplot(range(0, len(x)), x, color=c, alpha=0.2, labels=[]))
        

    def get_x_tick_labels(self):
        lst = []
        for v in self.hdata[str(self.selected_sesh)]:
                lst.append(v[InfoOrder.CurrentTime.value])
        return lst
    

    '''
        Returns a list of the given reading in history.csv
        i: index of the reading
    '''
    def get_session_el2(self, i: int):
        lst = []
        
        for v in self.hdata[str(self.selected_sesh)]:
            lst.append(float(v[i]))
        
        return lst


    '''
        Adds a toolbar on the bottom of the plot window
    '''
    def add_toolbar(self) -> None:
        # Optional toolbar
        self.toolbar = NavigationToolbar2Tk(self.canvas, self, pack_toolbar=False)
        self.toolbar.config(background='#2f2f2f', highlightbackground='#2f2f2f')
        self.toolbar._message_label.config(background='#2f2f2f')#, highlightbackground='#2f2f2f')
        self.toolbar.update()
        self.toolbar.pack(side='bottom', expand=False)


    def zoom(self, event):
        # get the current x and y limits
        cur_xlim = self.ax.get_xlim()
        cur_ylim = self.ax.get_ylim()
        cur_xrange = (cur_xlim[1] - cur_xlim[0])*.5
        cur_yrange = (cur_ylim[1] - cur_ylim[0])*.5
        xdata = event.xdata # get event x location
        ydata = event.ydata # get event y location
        if event.button == 'down':
            # deal with zoom in
            scale_factor = 1/0.5
        elif event.button == 'up':
            # deal with zoom out
            scale_factor = 0.5
        else:
            # deal with something that should never happen
            scale_factor = 1

        # set new limits
        self.ax.set_xlim([xdata - cur_xrange*scale_factor,
                     xdata + cur_xrange*scale_factor])
        self.ax.set_ylim([ydata - cur_yrange*scale_factor,
                     ydata + cur_yrange*scale_factor])

        self.canvas.draw()


    def lclick(self, event):
        self.startx, self.starty = event.xdata, event.ydata


    def pan(self, event):
        if event.button == 1:
            xd = event.xdata
            yd = event.ydata
            xl1, xl2 = self.ax.get_xlim()
            yl1, yl2 = self.ax.get_ylim()
            self.ax.set_xlim(xl1 + (self.startx - xd), xl2 + (self.startx - xd))
            self.ax.set_ylim(yl1 + (self.starty - yd), yl2 + (self.starty - yd))

            self.canvas.draw()
        

    def reset_view(self):
        self.ax.set_xlim(self.ogx)
        self.ax.set_ylim(self.ogy)
        self.canvas.draw_idle()

        

'''
    Small Enum class for indexing headers in history.csv
'''
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
    Charging = 12
