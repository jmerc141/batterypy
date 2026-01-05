# internal graph
import tkinter as tk
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from tkinter import Frame, ttk
from threading import Thread
import sys, s_probe

'''
Referencing plt will cause hanging,
Plot resizes after opening external plot (open external then internal and its resized)
TODO: remove self.sp, replace with s_probe static calls
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

        self.internal_dpi = 65

        self.configure(bg='#2f2f2f')
            
        self.grid(row=0, column=2)

        self.v = 1.0
        self.A = 1.0

        self.i_fig = plt.Figure(facecolor='#f0f0f0', figsize=(7,6.5), dpi=self.internal_dpi)
        self.i_fig.subplots_adjust(bottom=0.05, top=0.975, left=0.1, right=0.975)
        self.x = [0]
        self.prop = 'Voltage'
        self.y = [0]

        self.ax = self.i_fig.add_subplot(111, ylim=(0,20))
        self.ax.set_ylabel('Voltage (V)', color='black', fontsize=16)
        self.ax.grid(color='black')

        south_frame = Frame(self)
        
        south_frame.configure(bg='#2f2f2f')
        #self.ax.set_xlabel('Seconds', color='white')
        self.ax.set_ylabel('Voltage (V)', color='white')
        self.ax.set_facecolor('#2f2f2f')
        self.ax.spines['bottom'].set_color('white')
        self.ax.spines['top'].set_color('white')
        self.ax.spines['right'].set_color('white')
        self.ax.spines['left'].set_color('white')
        self.ax.tick_params(axis='x', colors='white')
        self.ax.tick_params(axis='y', colors='white')
        self.ax.grid(color='grey')
        self.i_fig.set_facecolor('#2f2f2f')

        self.legend = self.ax.text(0.5, 0.95, '', bbox={'facecolor': 'w', 'alpha': 0.5, 'pad': 5}, 
                                transform=self.ax.transAxes, ha='center', fontsize=16, color='white')
        #else:
        #    self.title = self.ax.text(0.5, 0.95, '', bbox={'facecolor': 'w', 'alpha': 0.5, 'pad': 5}, 
        #                          transform=self.ax.transAxes, ha='center', fontsize=16)
        
        self.ax.set_xlim(0, 60)

        self.l1, = self.ax.plot(self.x, self.y, color='red')
        self.sp, = self.ax.stackplot(self.x, self.y, color='red', alpha=0.3)

        self.canvas = FigureCanvasTkAgg(self.i_fig, master=self)
        self.canvas.get_tk_widget().pack(side='top', anchor='n', padx=10, expand=True, fill='both')

        south_frame.pack(side='bottom', pady=10)

        vbtn = ttk.Button(south_frame, text='Volts', command=lambda: self.set_prop('Voltage'))
        abtn = ttk.Button(south_frame, text='Amps', command=lambda: self.set_prop('Amperage'))
        wbtn = ttk.Button(south_frame, text='Watts', command=lambda: self.set_prop('Wattage'))
        #outbtn = ttk.Button(south_frame, text='-', command=self.zoomOut)
        #inbtn = ttk.Button(south_frame, text='+', command=self.zoomIn)
        #btn3 = ttk.Button(south_frame, text='All', command=lambda: self.set_prop('All'))
        
        vbtn.pack(side='left', padx=5)
        abtn.pack(side='left', padx=5)
        wbtn.pack(side='left', padx=5)
        #outbtn.pack(side='left', padx=5)
        #inbtn.pack(side='left', padx=5)

        #self.add_toolbar()

        self.i_proc = Thread(target=self.start_anim)
        self.i_proc.start()
        #self.canvas.draw()


    # Destroys graph element
    def Clear(self):
        self.destroy()


    def animate(self, i):
        '''
            Sets data for internal graph animation
        '''
        self.tick += 1
        self.x.append(self.tick)
        #print(self.prop)
        if self.prop == 'Amperage':
            tmp = s_probe.sProbe.amps
        if self.prop == 'Voltage':
            tmp = s_probe.sProbe.voltage
        if self.prop == 'Wattage':
            tmp = s_probe.sProbe.watts
        if self.prop == 'All':
            tmp = self.charg or self.disch
        self.y.append(tmp)

        # adds scrolling x axis after maxX seconds
        if len(self.x) > self.maxX:
            self.x.pop(0)
            self.y.pop(0)
            # + 1 to add space after line
            self.ax.set_xlim([self.x[0], self.x[-1]+1])

        self.ymax = max(self.y)
        self.ax.set_ylim(0, self.ymax+1)

        self.l1.set_data(self.x, self.y)
        self.sp.remove()

        if self.prop == 'Amperage':
            self.sp, = self.ax.stackplot(self.x, self.y, color='cyan', alpha=0.3)
            self.legend.set_text(str(s_probe.sProbe.amps) + 'A')
        if self.prop == 'Voltage':
            self.sp, = self.ax.stackplot(self.x, self.y, color='red', alpha=0.3)
            self.legend.set_text(str(s_probe.sProbe.voltage) + 'V')
        if self.prop == 'Wattage':
            self.sp, = self.ax.stackplot(self.x, self.y, color='yellow', alpha=0.3)
            self.legend.set_text(str(s_probe.sProbe.watts) + 'W')

        return self.sp, self.l1, self.legend


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
            tmp = s_probe.sProbe.amps
            self.l1, = self.ax.plot(self.x, self.y, color='c')
            self.yl = 'Amperage (A)'
        if self.prop == 'Voltage':
            tmp = s_probe.sProbe.voltage
            self.l1, = self.ax.plot(self.x, self.y, color='red')
            self.yl = 'Voltage (V)'
        if self.prop == 'Wattage':
            tmp = s_probe.sProbe.watts
            self.l1, = self.ax.plot(self.x, self.y, color='m')
            self.yl = 'Power (W)'
        if self.prop == 'All':
            # TODO: make volts amps watts graph
            pass
        
        
        self.ax.set_ylabel(self.yl, color='white',fontsize=16)
        self.ax.grid(color='grey')
        self.legend = self.ax.text(0.5, 0.95, '', bbox={'facecolor': 'w', 'alpha': 0.5, 'pad': 5}, 
                                transform=self.ax.transAxes, ha='center', fontsize=20, color='white')
        
        self.ax.set_xlim(0, 60)
        self.ax.set_ylim(0, tmp + 1)
        self.y = [tmp]
        self.canvas.draw()

    
    def zoomOut(self):
        plt.close(self.i_fig)
        self.init_window()
        self.internal_dpi -= 5
        self.i_fig.set_dpi(self.internal_dpi)

    
    def zoomIn(self):
        self.internal_dpi += 5
        self.i_fig.set_dpi(self.internal_dpi)


    def start_anim(self):
        self.ani = animation.FuncAnimation(self.i_fig, self.animate, cache_frame_data=False, interval=1000, blit=True)


    def add_toolbar(self) -> None:
        # Optional toolbar
        self.toolbar = NavigationToolbar2Tk(self.canvas, self, pack_toolbar=False)
        self.toolbar.config(background='#2f2f2f', highlightbackground='#2f2f2f')
        self.toolbar._message_label.config(background='#2f2f2f')#, highlightbackground='#2f2f2f')
        self.toolbar.update()
        self.toolbar.pack(side='bottom', expand=False)
        