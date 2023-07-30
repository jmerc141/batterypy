# internal graph
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import tkinter as tk
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import probe
from tkinter import Frame,Label,Entry,Button
from multiprocessing import Process

'''
Referencing plt will cause hanging
'''

class Window(Frame):

    def __init__(self, master = None):
        Frame.__init__(self, master)
        self.master = master
        self.maxX = 60
        self.maxY = 10
        self.minY = 12
        self.tick = 0
        self.prop = None

        self.init_window()


    # Destroys graph element
    def Clear(self):
        self.destroy()


    def animate(self,i):
        try:
            self.line.remove()
        except:
            print('Probly doesnt exist')
        self.p.refresh()
        self.tick += 1
        self.x.append(self.tick)

        if self.prop == 'Amperage':
            tmp = self.p.amps
        if self.prop == 'Voltage':
            tmp = self.p.voltage
        if self.prop == 'Discharge Power':
            tmp = self.p.dischargerate
        if self.prop == 'Charge Power':
            tmp = self.p.chargerate
        self.y.append(tmp)

        # adds scrolling x axis after maxX seconds
        if len(self.x) > self.maxX:
            self.x.pop(0)
            self.y.pop(0)
            # + 1 to add space after line
            self.ax.set_xlim([self.x[0], self.x[-1]+1])

        self.ymax = max(self.y)
        self.ax.set_ylim(0, self.ymax+2)

        if self.prop == 'Amperage':
            self.line, = self.ax.stackplot(self.x, self.y, color='cyan', alpha=0.5)
        if self.prop == 'Voltage':
            self.line, = self.ax.stackplot(self.x, self.y, color='red', alpha=0.5)
        if self.prop == 'Discharge Power':
            self.line, = self.ax.stackplot(self.x, self.y, color='magenta', alpha=0.5)
        if self.prop == 'Charge Power':
            self.line, = self.ax.stackplot(self.x, self.y, color='yellow', alpha=0.5)


    def set_prop(self, batprop):
        self.x = [0]        
        self.maxY = 0
        self.minY = 100
        self.tick = 0
        self.ax.cla()

        self.ax.set_xlabel('Seconds', color='white')
        
        self.prop = batprop

        if self.prop == 'Amperage':
            tmp = self.p.amps
            self.ax.set_ylabel('Amperage (A)', color='white')
        if self.prop == 'Voltage':
            tmp = self.p.voltage
            self.ax.set_ylabel('Voltage (V)', color='white')
        if self.prop == 'Discharge Power':
            tmp = self.p.dischargerate
            self.ax.set_ylabel('Discharge Power (W)', color='white')
        if self.prop == 'Charge Power':
            tmp = self.p.chargerate
            self.ax.set_ylabel('Charge Power (W)', color='white')
        self.ax.set_ylim(0, tmp)
        self.y = [tmp]


    def init_window(self):
        # Initializes to Voltage for now
        self.grid(row=0, column=2)

        self.p = probe.Probe()
        self.v = 1.0
        self.A = 1.0

        self.fig = plt.Figure(facecolor='#2f2f2f', figsize=(7,7))
        self.fig.subplots_adjust(bottom=0.17, top=0.92)
        self.x = [0]
        self.prop = 'Discharge Power'
        self.y = [self.p.dischargerate]

        self.ax = self.fig.add_subplot(111, ylim=(0,20))
        
        self.ax.set_xlabel('Seconds', color='white')
        self.ax.set_ylabel('Discharge Power (W)', color='white')
        plt.xlabel('Seconds', color='white')
        plt.ylabel('Seconds', color='white')
        self.ax.set_title('Graph', color='white')
        self.ax.set_facecolor('#2f2f2f')
        self.ax.spines['bottom'].set_color('white')
        self.ax.spines['top'].set_color('white')
        self.ax.spines['right'].set_color('white')
        self.ax.spines['left'].set_color('white')
        self.ax.tick_params(axis='x', colors='white')
        self.ax.tick_params(axis='y', colors='white')
        self.ax.tick_params(grid_color='white')

        self.ax.plot(self.x, self.y)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack(side='top', anchor='n')

        # Optional toolbar
        #self.toolbar = NavigationToolbar2Tk(self.canvas, self, pack_toolbar=False)
        #self.toolbar.config(background='#2f2f2f', highlightbackground='#2f2f2f')
        #self.toolbar._message_label.config(background='#2f2f2f')#, highlightbackground='#2f2f2f')
        #self.toolbar.update()
        #self.toolbar.pack(side='bottom', expand=False)
        
        self.ani = animation.FuncAnimation(self.fig, self.animate, cache_frame_data=False, interval=1000, blit=False)

