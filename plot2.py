import tkinter, probe
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
from matplotlib import pyplot as plt, animation
import numpy as np

class Plot2:

    def pre(self, win):
        plt.rcParams["figure.figsize"] = [7.00, 3.50]
        plt.rcParams["figure.autolayout"] = True

        #root = tkinter.Tk()
        #root.wm_title("Embedding in Tk")

        plt.axes(xlim=(0, 2), ylim=(-2, 2))
        fig = plt.Figure(dpi=100)
        ax = fig.add_subplot(xlim=(0, 2), ylim=(-1, 1))
        self.line, = ax.plot([], [], lw=2)

        canvas = FigureCanvasTkAgg(fig, master=win)
        canvas.draw()

        toolbar = NavigationToolbar2Tk(canvas, win, pack_toolbar=False)
        toolbar.update()

        canvas.mpl_connect(
            "key_press_event", lambda event: print(f"you pressed {event.key}"))
        canvas.mpl_connect("key_press_event", key_press_handler)

        button = tkinter.Button(master=win, text="Quit", command=win.quit)
        button.pack(side=tkinter.BOTTOM)

        toolbar.pack(side=tkinter.BOTTOM, fill=tkinter.X)
        canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

        anim = animation.FuncAnimation(fig, self.animate, init_func=self.init, interval=1000, blit=False)

    def init(self):
        print('init')
        self.line.set_data([], [])
        self.p = probe.Probe()
        return self.line,

    def animate(self, i):
        #x = np.linspace(0, 2, 1000)
        #y = np.sin(2 * np.pi * (x - 0.01 * i))
        x=i+1
        y=self.p.voltage()
        print(y)
        self.line.set_data(x, y)
        return self.line,

