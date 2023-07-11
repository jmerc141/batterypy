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
        print("clear")     
        self.destroy()


    def Plot(self):
        self.v = float(self.textSpeed.get())
        self.A = float(self.textAmplitude.get())


    def animate(self,i):
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

        # set min and max for y-axis
        if tmp+.25 > self.maxY:
            self.maxY = tmp+.25
        if tmp-.25 < self.minY:
            self.minY = tmp-.25

        self.ax.set_ylim([self.minY, self.maxY])
        if self.prop == 'Amperage':
            self.ax.plot(self.x, self.y, 'c-')
        if self.prop == 'Voltage':
            self.ax.plot(self.x, self.y, 'r-')
        if self.prop == 'Discharge Power':
            self.ax.plot(self.x, self.y, 'm-')
        if self.prop == 'Charge Power':
            self.ax.plot(self.x, self.y, 'y-')


    def set_prop(self, batprop):
        # change y range, reset self.x self.y, min max
        self.x = [0]
        self.y = [0]
        self.maxY = 0
        self.tick = 0
        self.ax.set_xlim(0, 1)
        self.minY = 100
        self.ax.cla()
        
        self.prop = batprop


    def init_window(self):
        self.master.title("Plot")
        self.grid(row=0, column=2)

        self.p = probe.Probe()
        self.v = 1.0
        self.A = 1.0

        self.fig = plt.Figure(facecolor='#2f2f2f', figsize=(7,7))
        self.x = [0]
        self.prop = 'Voltage'
        self.y = [0]

        self.ax = self.fig.add_subplot(111, ylim=(0,20))
        self.ax.plot(self.x, self.y)
        self.ax.set_xlabel('Seconds', color='white')
        self.ax.set_ylabel('', color='white')
        self.ax.set_title('Graph', color='white')
        self.ax.set_facecolor('#2f2f2f')
        self.ax.spines['bottom'].set_color('white')
        self.ax.spines['top'].set_color('white')
        self.ax.spines['right'].set_color('white')
        self.ax.spines['left'].set_color('white')
        self.ax.tick_params(axis='x', colors='white')
        self.ax.tick_params(axis='y', colors='white')

        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().grid(column=0,row=0)

        toolbar = NavigationToolbar2Tk(self.canvas, self.master, pack_toolbar=False)
        toolbar.update()
        toolbar.grid(column=2, row=0, sticky='n')

        self.ani = animation.FuncAnimation(self.fig, self.animate, cache_frame_data=False, interval=1000, blit=False)

