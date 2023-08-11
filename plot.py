# external graph
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import s_probe
from threading import Thread

class Plot:

    def setup_2(self):
        self.fig = plt.figure(facecolor='#2f2f2f', figsize=(8,6), dpi=80)
        # horizontal graphs
        #self.ax1 = self.fig.add_subplot(3,1,1)
        #self.ax2 = self.fig.add_subplot(3,1,2)
        #self.ax3 = self.fig.add_subplot(3,1,3)
        # vertical graphs
        self.ax1 = self.fig.add_subplot(1,3,1)
        self.ax2 = self.fig.add_subplot(1,3,2)
        self.ax3 = self.fig.add_subplot(1,3,3)

        self.vline, = self.ax1.plot(self.xs, self.volty, color='red', linewidth=2)
        self.aline, = self.ax2.plot(self.xs, self.ampy, color='cyan', linewidth=2)
        self.wline, = self.ax3.plot(self.xs, self.watty, color='magenta', linewidth=2)

        self.ax1.set_xlim(0, 10)
        self.ax2.set_xlim(0, 10)
        self.ax3.set_xlim(0, 10)

        self.ax1.set_title('Voltage', color='white', fontsize=12)
        self.ax2.set_title('Amps', color='white', fontsize=12)
        self.ax3.set_title('Watts', color='white', fontsize=12)
        self.ax1.set_facecolor('#2f2f2f')
        self.ax2.set_facecolor('#2f2f2f')
        self.ax3.set_facecolor('#2f2f2f')
        self.ax1.tick_params(axis='x', colors='white', labelsize=10)
        self.ax1.tick_params(axis='y', colors='white', labelsize=10)
        self.ax2.tick_params(axis='x', colors='white', labelsize=10)
        self.ax2.tick_params(axis='y', colors='white', labelsize=10)
        self.ax3.tick_params(axis='x', colors='white', labelsize=10)
        self.ax3.tick_params(axis='y', colors='white', labelsize=10)
        self.fig.subplots_adjust(bottom=.13, left=.07, hspace=.36, wspace=0.3)

 
    def anim2(self, i):
        self.xs.append(i)
        self.volty.append(s_probe.sProbe.voltage)
        self.ampy.append(s_probe.sProbe.amps)
        self.watty.append(s_probe.sProbe.dischargerate)

        self.ax1.set_title(f'Voltage ({s_probe.sProbe.voltage})', color='white', fontsize=12)
        self.ax2.set_title(f'Amps ({s_probe.sProbe.amps})', color='white', fontsize=12)
        self.ax3.set_title(f'Watts ({s_probe.sProbe.dischargerate})', color='white', fontsize=12)

        self.vline.set_data(self.xs, self.volty)
        self.aline.set_data(self.xs, self.ampy)
        self.wline.set_data(self.xs, self.watty)

        self.ax1.set_ylim(0, max(self.volty) + 1)
        
        #self.spm1, = self.ax1.stackplot(self.xs, self.volty, color='red', alpha=0.5)
        #self.spm2, = self.ax2.stackplot(self.xs, self.ampy, color='cyan', alpha=0.5)
        #self.spm3, = self.ax3.stackplot(self.xs, self.watty, color='magenta', alpha=0.5)

        return self.vline, self.aline, self.wline,# self.spm1, self.spm2, self.spm3,


    def setup_1(self):
        self.maxX = 60
        self.ymax = []
        for i in range(self.maxX):
            self.xs.append(i)
            self.volty.append(0)
            self.watty.append(0)
            self.ampy.append(0)
            self.ymax.append(0)
        
        self.fig = plt.figure(dpi=75, figsize=(8,8))
        self.ax1 = self.fig.add_subplot()
        print(self.dark)
        if self.dark:
            plt.title('Power', color='white')
            plt.xlabel('Seconds', color='white')
            self.fig.set_facecolor('#2f2f2f')
            self.ax1.set_facecolor('#2f2f2f')
            self.ax1.tick_params(axis='x', colors='white')
            self.ax1.tick_params(axis='y', colors='white')
        else:
            plt.title('Power', color='black')
            plt.xlabel('Seconds', color='black')
            #self.fig.set_facecolor('#2f2f2f')
            #self.ax1.set_facecolor('#2f2f2f')
            self.ax1.tick_params(axis='x', colors='black')
            self.ax1.tick_params(axis='y', colors='black')

        self.fig.subplots_adjust(bottom=0.09, top=0.93)

        self.ax1.set_xlim([0, self.maxX])

        self.l1, = plt.plot(self.volty, label='Volts', color='red', linewidth=2)
        self.l2, = plt.plot(self.ampy, label='Amps', color='cyan', linewidth=2)
        self.l3, = plt.plot(self.watty, label='Watts', color='orange', linewidth=2)
        self.L = self.ax1.legend(loc=2)
        

    # single plot
    def anim1(self, i):
        self.volty.append(s_probe.sProbe.voltage)
        self.ampy.append(s_probe.sProbe.amps)
        self.watty.append(s_probe.sProbe.chargerate)

        self.ymax.append(max(max([self.volty, self.ampy, self.watty])))
        self.ax1.set_ylim(0, max(self.ymax) + 1)

        self.volty.pop(0)
        self.ampy.pop(0)
        self.watty.pop(0)

        self.L.get_texts()[0].set_text(f'Volts ({s_probe.sProbe.voltage})')
        self.L.get_texts()[1].set_text(f'Amps ({s_probe.sProbe.amps})')
        self.L.get_texts()[2].set_text(f'Watts ({s_probe.sProbe.chargerate})')

        self.l1.set_ydata(self.volty)
        self.l2.set_ydata(self.ampy)
        self.l3.set_ydata(self.watty)

        self.sp1, = self.ax1.stackplot(self.xs, self.volty, color='red', alpha=0.2)
        self.sp2, = self.ax1.stackplot(self.xs, self.ampy, color='cyan', alpha=0.2)
        self.sp3, = self.ax1.stackplot(self.xs, self.watty, color='yellow', alpha=0.2)

        return self.l1, self.l2, self.l3, self.L, self.sp3, self.sp2, self.sp1


    def set_prop(self, prop):
        self.prop = prop    


    def a(self, func):
        ani = animation.FuncAnimation(self.fig, func, interval=1000, cache_frame_data=False, blit=True)


    def __init__(self, t, dark: bool = None):
        self.prop = 0
        self.dark = dark
        style.use('fivethirtyeight')

        self.xs = []

        self.volty = []
        self.ampy  = []
        self.watty = []

        if t == 0:
            self.setup_2()
            self.proc = Thread(target=self.a, args=(self.anim2,))
            self.proc.start()
        if t == 1:
            self.setup_1()
            self.proc = Thread(target=self.a, args=(self.anim1,))
            self.proc.start()

        plt.show()
        

    def on_close(self):
        #print('close')
        plt.close('all')
