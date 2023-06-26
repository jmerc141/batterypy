import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import probe

class Plot:

    def animate(self, i):
        self.a.refresh()
        
        i=i+1
        self.xs.append(i)
        self.ys.append(self.a.voltage)
        
        #ax1.clear()
        self.ax1.plot(self.xs, self.ys, 'c-')
        plt.draw()


    def __init__(self):
        style.use('fivethirtyeight')
        fig = plt.figure(figsize=(10,6))
        self.ax1 = fig.add_subplot(1,1,1)
        self.ax1.set_xlabel('Time (seconds)')
        self.ax1.set_ylabel('Amps')
        self.ax1.set_title('Battery Amps')
        fig.subplots_adjust(bottom=.13)

        plt.ylim([11.9,12])

        self.a = probe.Probe()
        #self.i=0
        self.xs = []
        self.ys = []

        ani = animation.FuncAnimation(fig, self.animate, interval=1000)

        plt.show()
    

if __name__ == '__main__':
    p = Plot()
    #p.init()