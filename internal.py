# internal graph
import tkinter as tk
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from tkinter import Frame, ttk
from threading import Thread
import sys

'''
Referencing plt will cause hanging,
Plot resizes after opening external plot (open external then internal and its resized)
'''

class Window(Frame):

    def __init__(self, master = None, dark: bool = None):
        if sys.platform == 'win32':
            import s_probe
            self.sp = s_probe
        elif sys.platform == 'linux':
            import s_probe_l
            self.sp = s_probe_l
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


    def updateValues(self):
        if sys.platform == 'win32':
            self.amps  = self.sp.sProbe.amps
            self.volts = self.sp.sProbe.voltage
            self.disch = self.sp.sProbe.dischargerate
            self.charg = self.sp.sProbe.chargerate
            self.charging = self.sp.sProbe.charging
        elif sys.platform == 'linux':
            self.amps  = int(self.sp.sProbe.calculated_props['amps']) / 1000000
            self.volts = int(self.sp.sProbe.props['voltage_now']) / 1000000
            self.disch = int(self.sp.sProbe.calculated_props['watts']) / 1000000
            self.charg = int(self.sp.sProbe.calculated_props['watts']) / 1000000
            self.charging = (self.sp.sProbe.props['status'] == 'Charging')


    # Destroys graph element
    def Clear(self):
        self.destroy()


    def animate(self,i):
        self.updateValues()

        self.tick += 1
        self.x.append(self.tick)

        if self.prop == 'Amperage':
            tmp = self.amps
        if self.prop == 'Voltage':
            tmp = self.volts
        if self.prop == 'Discharge Power':
            tmp = self.disch
        if self.prop == 'Charge Power':
            tmp = self.charg
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

        if self.prop == 'Amperage':
            self.line, = self.ax.stackplot(self.x, self.y, color='cyan', alpha=0.5)
            self.title.set_text(str(self.amps) + 'A')
        if self.prop == 'Voltage':
            self.line, = self.ax.stackplot(self.x, self.y, color='red', alpha=0.5)
            self.title.set_text(str(self.volts) + 'V')
        if self.prop == 'Discharge Power':
            self.line, = self.ax.stackplot(self.x, self.y, color='magenta', alpha=0.5)
            self.title.set_text(str(self.disch) + 'W')
        if self.prop == 'Charge Power':
            self.line, = self.ax.stackplot(self.x, self.y, color='yellow', alpha=0.5)
            self.title.set_text(str(self.charg) + 'W')

        return self.line, self.l1, self.title


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
        
        if self.dark:
            self.ax.set_ylabel(self.yl, color='white')
            self.ax.grid(color='white')
            self.title = self.ax.text(0.5, 0.95, '', bbox={'facecolor': 'w', 'alpha': 0.5, 'pad': 5}, 
                                  transform=self.ax.transAxes, ha='center', fontsize=20, color='white')
        else:
            self.ax.set_ylabel(self.yl, color='black')
            self.ax.set_title(str(tmp), color='black')
            self.ax.grid(color='black')
            self.title = self.ax.text(0.5, 0.95, '', bbox={'facecolor': 'w', 'alpha': 0.5, 'pad': 5}, 
                                  transform=self.ax.transAxes, ha='center', fontsize=20)

        self.ax.set_xlim(0, 60)
        self.ax.set_ylim(0, tmp + 1)
        self.y = [tmp]
        self.canvas.draw()
        

    def init_window(self):
        # Initializes to Voltage for now
        self.grid(row=0, column=2)

        self.v = 1.0
        self.A = 1.0

        self.i_fig = plt.Figure(facecolor='#f0f0f0', figsize=(7,8), dpi=80)
        self.i_fig.subplots_adjust(bottom=0.06, top=0.975, left=0.08, right=0.975)
        self.x = [0]
        self.prop = 'Voltage'
        self.y = [0]

        self.ax = self.i_fig.add_subplot(111, ylim=(0,20))
        self.ax.set_xlabel('Seconds', color='black', fontsize=16)
        self.ax.set_ylabel('Voltage (V)', color='black', fontsize=16)
        self.ax.grid(color='black')

        south_frame = Frame(self)
        
        if self.dark:
            south_frame.configure(bg='#2f2f2f')
            self.ax.set_xlabel('Seconds', color='white')
            self.ax.set_ylabel('Voltage (V)', color='white')
            self.ax.set_facecolor('#2f2f2f')
            self.ax.spines['bottom'].set_color('white')
            self.ax.spines['top'].set_color('white')
            self.ax.spines['right'].set_color('white')
            self.ax.spines['left'].set_color('white')
            self.ax.tick_params(axis='x', colors='white')
            self.ax.tick_params(axis='y', colors='white')
            self.ax.grid(color='white')
            self.i_fig.set_facecolor('#2f2f2f')
            self.title = self.ax.text(0.5, 0.95, '', bbox={'facecolor': 'w', 'alpha': 0.5, 'pad': 5}, 
                                  transform=self.ax.transAxes, ha='center', fontsize=16, color='white')
        else:
            self.title = self.ax.text(0.5, 0.95, '', bbox={'facecolor': 'w', 'alpha': 0.5, 'pad': 5}, 
                                  transform=self.ax.transAxes, ha='center', fontsize=16)
        
        self.ax.set_xlim(0, 60)

        self.l1, = self.ax.plot(self.x, self.y, color='red')

        self.canvas = FigureCanvasTkAgg(self.i_fig, master=self)
        self.canvas.get_tk_widget().pack(side='top', anchor='n', padx=10, expand=True, fill='both')

        
        south_frame.pack(side='bottom', pady=20)

        vbtn = ttk.Button(south_frame, text='Volts', command=lambda: self.set_prop('Voltage'))
        abtn = ttk.Button(south_frame, text='Amps', command=lambda: self.set_prop('Amperage'))
        wbtn = ttk.Button(south_frame, text='Watts', command=self.wattBtn)
        #btn3 = ttk.Button(south_frame, text='All', command=lambda: self.set_prop('All'))
        
        vbtn.pack(side='left', padx=5)
        abtn.pack(side='left', padx=5)
        wbtn.pack(side='left', padx=5)
        #btn3.pack(side='left', padx=5)

        #self.add_toolbar()

        self.i_proc = Thread(target=self.start_anim)
        self.i_proc.start()
        #self.canvas.draw()
        
    def wattBtn(self):
        if self.charging:
            self.set_prop('Charge Power')
        else:
            self.set_prop('Discharge Power')

    def start_anim(self):
        self.ani = animation.FuncAnimation(self.i_fig, self.animate, cache_frame_data=False, interval=1000, blit=True)


    def add_toolbar(self) -> None:
        # Optional toolbar
        self.toolbar = NavigationToolbar2Tk(self.canvas, self, pack_toolbar=False)
        self.toolbar.config(background='#2f2f2f', highlightbackground='#2f2f2f')
        self.toolbar._message_label.config(background='#2f2f2f')#, highlightbackground='#2f2f2f')
        self.toolbar.update()
        self.toolbar.pack(side='bottom', expand=False)
        