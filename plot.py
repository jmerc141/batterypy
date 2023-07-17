# external graph
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.animation as animation
from matplotlib import style
import probe
from multiprocessing import Process

class Plot:

    def anim2(self, i):
        self.a.refresh()
        self.xs.append(i)
        self.volty.append(self.a.voltage)
        self.ampy.append(self.a.amps)
        self.watty.append(self.a.dischargerate)

        ymax = max([self.a.voltage, self.a.amps, self.a.dischargerate])
        self.ax1.set_ylim(0, ymax+1)
        self.ax1.plot(self.xs, self.volty, 'r-')
        self.ax2.plot(self.xs, self.ampy, 'c-')
        self.ax3.plot(self.xs, self.watty, 'm-')


    def anim1(self, i):
        self.a.refresh()
        self.xs.append(i)
        self.volty.append(self.a.voltage)
        self.ampy.append(self.a.amps)
        self.watty.append(self.a.dischargerate)

        ymax = max([self.a.voltage, self.a.amps, self.a.dischargerate])
        self.ax1.set_ylim(0, ymax+1)
        self.ax1.plot(self.xs, self.volty, 'r-')
        self.ax1.plot(self.xs, self.ampy, 'c-')
        self.ax1.plot(self.xs, self.watty, 'm-')


    def setup_1(self):
        self.fig = plt.figure(facecolor='#2f2f2f', figsize=(7,7))
        self.ax1 = self.fig.add_subplot()
        self.ax1.set_title("Power", color='white')
        self.ax1.set_facecolor('#2f2f2f')
        self.ax1.tick_params(axis='x', colors='white')
        self.ax1.tick_params(axis='y', colors='white')
        v_patch = mpatches.Patch(color='red', label='Voltage')
        a_patch = mpatches.Patch(color='cyan', label='Amps')
        w_patch = mpatches.Patch(color='magenta', label='Watts')
        plt.legend(handles=[v_patch, a_patch, w_patch])

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

        self.ax2.set_xlabel('Time (seconds)', color='white')
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
        print(t)
        self.prop = 0
        style.use('fivethirtyeight')

        if t == 0:
            self.setup_2()
            ani = animation.FuncAnimation(self.fig, self.anim2, interval=1000, cache_frame_data=False)
        if t == 1:
            self.setup_1()
            ani = animation.FuncAnimation(self.fig, self.anim1, interval=1000, cache_frame_data=False)

        self.a = probe.Probe()
        self.xs = []

        self.volty = []
        self.ampy  = []
        self.watty = []

        plt.show()


    def __init__(self, t):
        self.proc = Process(target=self.run , args=(t,))
        self.proc.start()
    
 