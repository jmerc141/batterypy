# internal graph
lazy import tkinter as tk
lazy from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
lazy import matplotlib.pyplot as plt
lazy import matplotlib.animation as animation
lazy from tkinter import Frame, ttk
lazy from threading import Thread
lazy import sys, s_probe

'''
Referencing plt will cause hanging,
Plot resizes after opening external plot (open external then internal and its resized)
TODO: remove self.sp, replace with s_probe static calls
'''

class Window(Frame):

    graph_background_color = '#fafafa' #'#2f2f2f'
    graph_line_color = '#555555' #'#f0f0f0'
    spine_color = 'grey'
    text_color = 'black'

    def __init__(self, master = None):
        Frame.__init__(self, master)
        self.master = master
        self.maxX = 60
        self.maxY = 10
        self.minY = 12
        self.tick = 0
        self.prop = None

        self.internal_dpi = 60

        self.configure(bg=self.graph_background_color)
            
        self.grid(row=0, column=2)

        self.v = 1.0
        self.A = 1.0

        self.i_fig = plt.Figure(facecolor=self.graph_line_color, figsize=(7,4), dpi=self.internal_dpi)
        self.i_fig.subplots_adjust(bottom=0.05, top=0.975, left=0.05, right=.975)
        self.x = [0]
        self.volt_data = [0]
        self.amp_data = [0]
        self.watt_data = [0]

        self.ax = self.i_fig.add_subplot(111, ylim=(0,20))
        #self.ax.set_ylabel('Voltage (V)', color='black', fontsize=16)
        #self.ax.grid(color='black')

        south_frame = Frame(self)
        
        south_frame.configure(bg=self.graph_background_color)
        #self.ax.set_xlabel('Seconds', color='white')
        self.ax.set_facecolor(self.graph_background_color)
        self.ax.spines['bottom'].set_color(self.spine_color)
        self.ax.spines['top'].set_color(self.spine_color)
        self.ax.spines['right'].set_color(self.spine_color)
        self.ax.spines['left'].set_color(self.spine_color)
        self.ax.tick_params(axis='x', colors=self.spine_color)
        self.ax.tick_params(axis='y', colors=self.spine_color)
        self.ax.grid(color='grey')
        self.i_fig.set_facecolor(self.graph_background_color)

        #self.legend = self.ax.text(0.5, 0.95, '', bbox={'facecolor': 'blue', 'alpha': 0.5, 'pad': 5}, 
        #                        transform=self.ax.transAxes, ha='center', fontsize=16, color=self.text_color)
        #else:
        #    self.title = self.ax.text(0.5, 0.95, '', bbox={'facecolor': 'w', 'alpha': 0.5, 'pad': 5}, 
        #                          transform=self.ax.transAxes, ha='center', fontsize=16)
        
        self.ax.set_xlim(0, 60)

        self.volt_line, = self.ax.plot(self.x, self.volt_data, color='red')
        self.volt_sp, = self.ax.stackplot(self.x, self.volt_data, color='red', alpha=0.3)
        self.amp_line, = self.ax.plot(self.x, self.amp_data, color='cyan')
        self.amp_sp, = self.ax.stackplot(self.x, self.amp_data, color='cyan', alpha=0.3)
        self.watt_line, = self.ax.plot(self.x, self.watt_data, color='yellow')
        self.watt_sp, = self.ax.stackplot(self.x, self.watt_data, color='yellow', alpha=0.3)

        self.canvas = FigureCanvasTkAgg(self.i_fig, master=self)
        self.canvas.get_tk_widget().pack(side='top', anchor='n', padx=5, expand=True, fill='both')

        south_frame.pack(side='bottom', pady=5)

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
        
        self.volt_data.append(s_probe.sProbe.voltage)
        self.amp_data.append(s_probe.sProbe.amps)
        self.watt_data.append(s_probe.sProbe.watts)

        # adds scrolling x axis after maxX seconds
        if len(self.x) > self.maxX:
            self.x.pop(0)
            self.volt_data.pop(0)
            self.amp_data.pop(0)
            self.watt_data.pop(0)
            # + 1 to add space after line
            self.ax.set_xlim([self.x[0], self.x[-1]+1])

        self.ymax = max(max([self.volt_data, self.amp_data, self.watt_data]))
        self.ax.set_ylim(0, self.ymax+1)

        self.volt_line.set_data(self.x, self.volt_data)
        self.amp_line.set_data(self.x, self.amp_data)
        self.watt_line.set_data(self.x, self.watt_data)
        
        self.volt_sp.remove()
        self.amp_sp.remove()
        self.watt_sp.remove()

        self.volt_sp, = self.ax.stackplot(self.x, self.volt_data, color='red', alpha=0.3)
        self.amp_sp, = self.ax.stackplot(self.x, self.amp_data, color='cyan', alpha=0.3)
        self.watt_sp, = self.ax.stackplot(self.x, self.watt_data, color='yellow', alpha=0.3)

        return self.volt_sp, self.amp_sp, self.watt_sp, self.volt_line, self.amp_line, self.watt_line


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
            self.l1, = self.ax.plot(self.x, self.y, color='y')
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
        self.toolbar.config(background=self.graph_background_color, highlightbackground=self.graph_background_color)
        self.toolbar._message_label.config(background=self.graph_background_color)#, highlightbackground='#2f2f2f')
        self.toolbar.update()
        self.toolbar.pack(side='bottom', expand=False)
        