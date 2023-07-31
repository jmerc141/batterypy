# external graph
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.animation as animation
from matplotlib import style
import probe
from multiprocessing import Process

class Plot:

    # multi graph, heavy on resources when updating
    def anim2(self, i):
        self.ax1.cla()
        self.ax2.cla()
        self.ax3.cla()
        self.a.refresh()
        self.xs.append(i)
        self.volty.append(self.a.voltage)
        self.ampy.append(self.a.amps)
        self.watty.append(self.a.dischargerate)

        self.ax1.set_title(f'Voltage ({self.a.voltage})' , color='white')
        self.ax2.set_title(f'Amps ({self.a.amps})', color='white')
        self.ax3.set_title(f'Watts ({self.a.dischargerate})', color='white')
        
        self.ax1.stackplot(self.xs, self.volty, color='red', alpha=0.5)
        self.ax2.stackplot(self.xs, self.ampy, color='cyan', alpha=0.5)
        self.ax3.stackplot(self.xs, self.watty, color='magenta', alpha=0.5)

    # single plot
    def anim1(self, i):
        self.a.refresh()
        self.volty.append(self.a.voltage)
        self.ampy.append(self.a.amps)
        self.watty.append(self.a.chargerate)

        self.ymax.append(max(max([self.volty, self.ampy, self.watty])))
        self.ax1.set_ylim(0, max(self.ymax) + 1)

        self.volty.pop(0)
        self.ampy.pop(0)
        self.watty.pop(0)

        self.L.get_texts()[0].set_text(f'Volts ({self.a.voltage})')
        self.L.get_texts()[1].set_text(f'Amps ({self.a.amps})')
        self.L.get_texts()[2].set_text(f'Watts ({self.a.chargerate})')

        self.l1.set_ydata(self.volty)
        self.l2.set_ydata(self.ampy)
        self.l3.set_ydata(self.watty)

        self.sp1, = self.ax1.stackplot(self.xs, self.volty, color='red', alpha=0.5)
        self.sp2, = self.ax1.stackplot(self.xs, self.ampy, color='cyan', alpha=0.5)
        self.sp3, = self.ax1.stackplot(self.xs, self.watty, color='yellow', alpha=0.5)

        return self.l1, self.l2, self.l3, self.L, self.sp1, #self.sp2, self.sp3


    def setup_1(self):
        self.maxX = 60
        self.ymax = []
        for i in range(self.maxX):
            self.xs.append(i)
            self.volty.append(0)
            self.watty.append(0)
            self.ampy.append(0)
            self.ymax.append(0)
        
        self.fig = plt.figure(facecolor='#2f2f2f', figsize=(6,6))
        self.ax1 = self.fig.add_subplot()
        plt.title('Power', color = 'white')
        plt.xlabel('Seconds', color='white')
        self.ax1.set_facecolor('#2f2f2f')
        self.ax1.tick_params(axis='x', colors='white')
        self.ax1.tick_params(axis='y', colors='white')

        self.fig.subplots_adjust(bottom=0.09, top=0.93)

        self.ax1.set_xlim([0, self.maxX])

        self.l1, = plt.plot(self.volty, label='Volts', color='red', linewidth=2)
        self.l2, = plt.plot(self.ampy, label='Amps', color='blue', linewidth=2)
        self.l3, = plt.plot(self.watty, label='Watts', color='orange', linewidth=2)
        self.L = self.ax1.legend(loc=2)
        

    def setup_2(self):
        self.fig = plt.figure(facecolor='#2f2f2f', figsize=(8,6))
        # horizontal graphs
        #self.ax1 = self.fig.add_subplot(3,1,1)
        #self.ax2 = self.fig.add_subplot(3,1,2)
        #self.ax3 = self.fig.add_subplot(3,1,3)
        # vertical graphs
        self.ax1 = self.fig.add_subplot(1,3,1)
        self.ax2 = self.fig.add_subplot(1,3,2)
        self.ax3 = self.fig.add_subplot(1,3,3)

        #self.ax2.set_xlabel('Time (seconds)', color='white')
        #plt.xlabel('Time (seconds)', color='white')
        self.ax1.set_title('Voltage', color='white')
        self.ax2.set_title('Amps', color='white')
        self.ax3.set_title('Watts', color='white')
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


    def set_prop(self, prop):
        self.prop = prop


    def run(self, t):
        self.prop = 0
        style.use('fivethirtyeight')

        self.a = probe.Probe()
        self.xs = []

        self.volty = []
        self.ampy  = []
        self.watty = []

        if t == 0:
            self.setup_2()
            ani = animation.FuncAnimation(self.fig, self.anim2, interval=1000, cache_frame_data=False)
        if t == 1:
            self.setup_1()
            ani = animation.FuncAnimation(self.fig, self.anim1, interval=1000, cache_frame_data=False, blit=True)

        plt.show()


    def __init__(self, t):
        self.proc = Process(target=self.run , args=(t,))
        self.proc.start()
    
 