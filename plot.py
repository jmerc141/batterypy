import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import probe
from multiprocessing import Process

class Plot:

    def animate(self, i):
        self.a.refresh()
        self.xs.append(i)
        self.volty.append(self.a.voltage)
        self.ampy.append(self.a.amps)
        self.watty.append(self.a.dischargerate)
        
        self.ax1.set_ylim(self.a.voltage-.1, self.a.voltage+.1)
        self.ax1.plot(self.xs, self.volty, 'r-')
        self.ax2.plot(self.xs, self.ampy, 'c-')
        self.ax3.plot(self.xs, self.watty, 'm-')
        plt.draw()


    def set_prop(self, prop):
        self.prop = prop


    def run(self):
        self.prop = 0
        style.use('fivethirtyeight')
        fig = plt.figure(figsize=(10,5))
        
        self.ax1 = fig.add_subplot(3,1,1)
        self.ax2 = fig.add_subplot(3,1,2)
        self.ax3 = fig.add_subplot(3,1,3)
        self.ax3.set_xlabel('Time (seconds)')
        self.ax1.set_ylabel('Volts')
        self.ax2.set_ylabel('Amps')
        self.ax3.set_ylabel("Watts")
        self.ax1.set_title('Readings')
        fig.subplots_adjust(bottom=.13, left=.11, hspace=.36)

        self.a = probe.Probe()
        self.xs = []

        self.volty = []
        self.ampy  = []
        self.watty = []

        ani = animation.FuncAnimation(fig, self.animate, interval=1000, cache_frame_data=False)

        plt.show()


    def __init__(self):
        self.proc = Process(target=self.run)
        self.proc.start()
    
 