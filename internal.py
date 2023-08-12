# internal graph
import tkinter as tk
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import s_probe
from tkinter import Frame, Button, ttk
from threading import Thread

'''
Referencing plt will cause hanging,
Plot resizes after opening external plot (open external then internal and its resized)
'''

class Window(Frame):

    def __init__(self, master = None, dark: bool = None):
        Frame.__init__(self, master)
        self.master = master
        self.maxX = 60
        self.maxY = 10
        self.minY = 12
        self.tick = 0
        self.prop = None
        self.dark = dark

        self.s = ttk.Style(self)

        if self.dark:
            self.configure(bg='#2f2f2f')
            try:
                self.tk.call('lappend', 'auto_path', 'res/awthemes-10.4.0')
                self.tk.call('package', 'require', 'awdark')
                self.s.theme_use('awdark')
            except Exception as e:
                print(e)
                tk.messagebox.showerror('Error', f'Cannot apply theme\n{e}')
        
        self.init_window()


    # Destroys graph element
    def Clear(self):
        self.destroy()


    def animate(self,i):
        #self.p.refresh()
        self.tick += 1
        self.x.append(self.tick)

        if self.prop == 'Amperage':
            tmp = s_probe.sProbe.amps
        if self.prop == 'Voltage':
            tmp = s_probe.sProbe.voltage
        if self.prop == 'Discharge Power':
            tmp = s_probe.sProbe.dischargerate
        if self.prop == 'Charge Power':
            tmp = s_probe.sProbe.chargerate
        self.y.append(tmp)
        
        if self.dark:
            self.ax.set_title(str(tmp), color='white')
        else:
            self.ax.set_title(str(tmp), color='black')

        # adds scrolling x axis after maxX seconds
        if len(self.x) > self.maxX:
            self.x.pop(0)
            self.y.pop(0)
            # + 1 to add space after line
            self.ax.set_xlim([self.x[0], self.x[-1]+1])

        self.ymax = max(self.y)
        self.ax.set_ylim(0, self.ymax+1)

        self.l1.set_data(self.x, self.y)

        if self.prop == 'Amperage':
            self.line, = self.ax.stackplot(self.x, self.y, color='cyan', alpha=0.5)
        if self.prop == 'Voltage':
            self.line, = self.ax.stackplot(self.x, self.y, color='red', alpha=0.5)
        if self.prop == 'Discharge Power':
            self.line, = self.ax.stackplot(self.x, self.y, color='magenta', alpha=0.5)
        if self.prop == 'Charge Power':
            self.line, = self.ax.stackplot(self.x, self.y, color='yellow', alpha=0.5)

        return self.line, self.l1, 


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
        if self.prop == 'Discharge Power':
            tmp = s_probe.sProbe.dischargerate
            self.l1, = self.ax.plot(self.x, self.y, color='m')
            self.yl = 'Discharge Power (W)'
        if self.prop == 'Charge Power':
            tmp = s_probe.sProbe.chargerate
            self.l1, = self.ax.plot(self.x, self.y, color='orange')
            self.yl = 'Charge Power (W)'
        if self.prop == 'All':
            print('all')
        
        if self.dark:
            self.ax.set_ylabel(self.yl, color='white')
            self.ax.set_title(str(tmp), color='white')
            self.ax.grid(color='white')
        else:
            self.ax.set_ylabel(self.yl, color='black')
            self.ax.set_title(str(tmp), color='black')
            self.ax.grid(color='black')

        self.ax.set_xlim(0, 60)
        self.ax.set_ylim(0, tmp + 1)
        self.y = [tmp]
        self.canvas.draw()
        

    def init_window(self):
        # Initializes to Voltage for now
        self.grid(row=0, column=2)

        self.v = 1.0
        self.A = 1.0

        self.i_fig = plt.Figure(facecolor='#f0f0f0', figsize=(7,8), dpi=75)
        self.i_fig.subplots_adjust(bottom=0.1, top=0.92, left=0.11)
        self.x = [0]
        self.prop = 'Voltage'
        self.y = [s_probe.sProbe.voltage]

        self.ax = self.i_fig.add_subplot(111, ylim=(0,20))
        self.ax.set_xlabel('Seconds', color='black')
        self.ax.set_ylabel('Voltage (V)', color='black')
        self.ax.grid(color='black')

        south_frame = Frame(self)
        
        if self.dark:
            south_frame.configure(bg='#2f2f2f')
            self.ax.set_xlabel('Seconds', color='white')
            self.ax.set_ylabel('Voltage', color='white')
            self.ax.set_title('Graph', color='white')
            self.ax.set_facecolor('#2f2f2f')
            self.ax.spines['bottom'].set_color('white')
            self.ax.spines['top'].set_color('white')
            self.ax.spines['right'].set_color('white')
            self.ax.spines['left'].set_color('white')
            self.ax.tick_params(axis='x', colors='white')
            self.ax.tick_params(axis='y', colors='white')
            self.ax.grid(color='white')
            self.i_fig.set_facecolor('#2f2f2f')
        
        self.ax.set_xlim(0, 60)

        self.l1, = self.ax.plot(self.x, self.y, color='red')

        self.canvas = FigureCanvasTkAgg(self.i_fig, master=self)
        self.canvas.get_tk_widget().pack(side='top', anchor='n', padx=10, expand=True, fill='both')

        
        south_frame.pack(side='bottom')

        vbtn = ttk.Button(south_frame, text='Volts', command=lambda: self.set_prop('Voltage'))
        abtn = ttk.Button(south_frame, text='Amps', command=lambda: self.set_prop('Amperage'))
        wbtn = ttk.Button(south_frame, text='Watts', command=lambda: self.set_prop('Discharge Power'))
        btn3 = ttk.Button(south_frame, text='All', command=lambda: self.set_prop('All'))
        
        vbtn.pack(side='left', padx=5)
        abtn.pack(side='left', padx=5)
        wbtn.pack(side='left', padx=5)
        btn3.pack(side='left', padx=5)

        #self.add_toolbar()

        self.i_proc = Thread(target=self.start_anim)
        self.i_proc.start()
        #self.canvas.draw()
        

    def start_anim(self):
        self.ani = animation.FuncAnimation(self.i_fig, self.animate, cache_frame_data=False, interval=1000, blit=True)


    def add_toolbar(self) -> None:
        # Optional toolbar
        self.toolbar = NavigationToolbar2Tk(self.canvas, self, pack_toolbar=False)
        self.toolbar.config(background='#2f2f2f', highlightbackground='#2f2f2f')
        self.toolbar._message_label.config(background='#2f2f2f')#, highlightbackground='#2f2f2f')
        self.toolbar.update()
        self.toolbar.pack(side='bottom', expand=False)
        