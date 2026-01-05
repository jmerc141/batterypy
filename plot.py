import matplotlib.pyplot as plt
import matplotlib.animation as animation
from threading import Thread
import s_probe


class Plot:
    '''
        Wrapper class for external plots
    '''

    def __init__(self, t):
        self.prop = 0

        self.xs = []

        self.volty = []
        self.ampy  = []
        self.watty = []

        self.dpi = 55

        # Disable toolbar in graph windows, must be BEFORE instantiating figures
        plt.rcParams['toolbar'] = 'None'

        # Create a seperate thread that runs the animation function
        if t == 0:
            self.setup_multi()
            self.proc = Thread(target=self.a, args=(self.anim_multi,))
            self.proc.start()
        if t == 1:
            self.setup_single()
            self.proc = Thread(target=self.a, args=(self.anim_single,))
            self.proc.start()
        
        plt.show()
        

    def setup_multi(self):
        '''
            Sets up figure, lines, axes for multi-plot window
        '''
        self.fig = plt.figure(figsize=(8,6), dpi=65, num='Power Graph')
        # horizontal graphs
        self.ax1 = self.fig.add_subplot(3,1,1)
        self.ax2 = self.fig.add_subplot(3,1,2)
        self.ax3 = self.fig.add_subplot(3,1,3)
        # vertical graphs
        #self.ax1 = self.fig.add_subplot(1,3,1)
        #self.ax2 = self.fig.add_subplot(1,3,2)
        #self.ax3 = self.fig.add_subplot(1,3,3)

        # create lines
        self.vline, = self.ax1.plot(self.xs, self.volty, color='red', linewidth=2)
        self.aline, = self.ax2.plot(self.xs, self.ampy, color='cyan', linewidth=2)
        self.wline, = self.ax3.plot(self.xs, self.watty, color='magenta', linewidth=2)

        self.vtitle = self.ax1.text(0.50, .85, "", 
                                    bbox={'facecolor': 'w', 'alpha': 0.5, 'pad': 5},
                                    transform=self.ax1.transAxes, ha='center')

        self.x_lim = 30
        for i in range(self.x_lim):
            self.xs.append(0)
            self.volty.append(0)
            self.watty.append(0)
            self.ampy.append(0)

        self.ax1.set_xlim(0, self.x_lim)
        self.ax2.set_xlim(0, self.x_lim)
        self.ax3.set_xlim(0, self.x_lim)

        self.ax1.set_title('Voltage', color='white', fontsize=12)
        self.ax2.set_title('Amps', color='white', fontsize=12)
        self.ax3.set_title('Watts', color='white', fontsize=12)
        
        self.fig.set_facecolor('#2f2f2f')
        self.ax1.set_facecolor('#2f2f2f')
        self.ax2.set_facecolor('#2f2f2f')
        self.ax3.set_facecolor('#2f2f2f')
        
        self.ax1.tick_params(axis='x', colors='white', labelsize=10)
        self.ax1.tick_params(axis='y', colors='white', labelsize=10)
        self.ax2.tick_params(axis='x', colors='white', labelsize=10)
        self.ax2.tick_params(axis='y', colors='white', labelsize=10)
        self.ax3.tick_params(axis='x', colors='white', labelsize=10)
        self.ax3.tick_params(axis='y', colors='white', labelsize=10)
        
        self.ax1.locator_params(axis='x', nbins=10)
        self.ax2.locator_params(axis='x', nbins=10)
        self.ax3.locator_params(axis='x', nbins=10)
        self.ax1.locator_params(axis='y', nbins=4)
        self.ax2.locator_params(axis='y', nbins=4)
        self.ax3.locator_params(axis='y', nbins=4)
        
        self.ax1.spines['bottom'].set_color('white')
        self.ax1.spines['top'].set_color('white')
        self.ax1.spines['right'].set_color('white')
        self.ax1.spines['left'].set_color('white')
        
        self.ax1.grid(color='grey')

        self.ax2.spines['bottom'].set_color('white')
        self.ax2.spines['top'].set_color('white')
        self.ax2.spines['right'].set_color('white')
        self.ax2.spines['left'].set_color('white')
        self.ax2.grid(color='grey')

        self.ax3.spines['bottom'].set_color('white')
        self.ax3.spines['top'].set_color('white')
        self.ax3.spines['right'].set_color('white')
        self.ax3.spines['left'].set_color('white')
        self.ax3.grid(color='grey')

        self.spm1, = self.ax1.stackplot(self.xs, self.volty, color='red', alpha=0.2)
        self.spm2, = self.ax2.stackplot(self.xs, self.ampy, color='cyan', alpha=0.2)
        self.spm3, = self.ax3.stackplot(self.xs, self.watty, color='magenta', alpha=0.2)

        self.fig.subplots_adjust(bottom=.05, left=.05, right=.98, top=.95, hspace=.36, wspace=0.3)

    
    def anim_multi(self, i):
        '''
            Function that returns elements to FuncAnimation for animating the multi-plot window
        '''
        self.xs.append(i)
        self.volty.append(s_probe.sProbe.voltage)
        self.ampy.append(s_probe.sProbe.amps)
        self.watty.append(s_probe.sProbe.watts)

        self.xs.pop(0)
        self.volty.pop(0)
        self.ampy.pop(0)
        self.watty.pop(0)
        for sp in [self.spm1, self.spm2, self.spm3]:
            sp.remove()

        self.ax1.set_title(f'Voltage ({s_probe.sProbe.voltage})', color='white', fontsize=12)
        self.ax2.set_title(f'Amps ({s_probe.sProbe.amps})', color='white', fontsize=12)
        self.ax3.set_title(f'Watts ({s_probe.sProbe.watts})', color='white', fontsize=12)

        self.vline.set_data(self.xs, self.volty)
        self.aline.set_data(self.xs, self.ampy)
        self.wline.set_data(self.xs, self.watty)

        self.ax1.set_ylim(0, max(self.volty) + 1)
        self.ax2.set_ylim(0, max(self.ampy) + 1)
        self.ax3.set_ylim(0, max(self.watty) + 1)

        #self.vtitle.set_text(s_probe.sProbe.voltage)
        
        self.spm1, = self.ax1.stackplot(self.xs, self.volty, color='red', alpha=0.2)
        self.spm2, = self.ax2.stackplot(self.xs, self.ampy, color='cyan', alpha=0.2)
        self.spm3, = self.ax3.stackplot(self.xs, self.watty, color='magenta', alpha=0.2)

        return self.vline, self.aline, self.wline, self.spm1, self.spm2, self.spm3,

    
    def setup_single(self):
        '''
            Sets up figure, lines, axes, etc. for single plot window
        '''
        self.maxX = 60
        self.ymax = []
        for i in range(self.maxX):
            self.xs.append(i)
            self.volty.append(0)
            self.watty.append(0)
            self.ampy.append(0)
            self.ymax.append(0)
        
        self.fig = plt.figure(dpi=self.dpi, figsize=(8.5,7), num='Power Graph')
        self.ax1 = self.fig.add_subplot()

        plt.title('Battery Power', color='white')
        plt.xlabel('Seconds', color='white')
        self.fig.set_facecolor('#2f2f2f')
        self.ax1.set_facecolor('#2f2f2f')
        self.ax1.tick_params(axis='x', colors='white')
        self.ax1.tick_params(axis='y', colors='white')
        self.ax1.grid(color='grey')
        self.ax1.spines['bottom'].set_color('white')
        self.ax1.spines['top'].set_color('white')
        self.ax1.spines['right'].set_color('white')
        self.ax1.spines['left'].set_color('white')
        self.ax1.locator_params(axis='y', nbins=10)

        self.fig.subplots_adjust(bottom=0.08, top=0.96, right=0.98, left=0.045)

        self.ax1.set_xlim([0, self.maxX])

        self.l1, = plt.plot(self.volty, label='Volts', color='red', linewidth=2)
        self.l2, = plt.plot(self.ampy, label='Amps', color='cyan', linewidth=2)
        self.l3, = plt.plot(self.watty, label='Watts', color='orange', linewidth=2)
        self.sp1, = self.ax1.stackplot(self.xs, self.volty, color='red', alpha=0.2)
        self.sp2, = self.ax1.stackplot(self.xs, self.ampy, color='cyan', alpha=0.2)
        self.sp3, = self.ax1.stackplot(self.xs, self.watty, color='yellow', alpha=0.2)
        self.L = self.ax1.legend(loc=2)

    
    def anim_single(self, i):
        '''
            Function that returns elements to FuncAnimation for animating the single plot window
        '''
        self.watty.append(s_probe.sProbe.watts)
        self.volty.append(s_probe.sProbe.voltage)
        self.ampy.append(s_probe.sProbe.amps)

        self.ymax.append(max(max([self.volty, self.ampy, self.watty])))
        self.ax1.set_ylim(0, max(self.ymax) + 1)

        self.volty.pop(0)
        self.ampy.pop(0)
        self.watty.pop(0)
        self.ymax.pop(0)

        for sp in [self.sp1, self.sp2, self.sp3]:
            sp.remove()

        self.L.get_texts()[0].set_text(f'Volts ({s_probe.sProbe.voltage})')
        self.L.get_texts()[1].set_text(f'Amps ({s_probe.sProbe.amps})')
        self.L.get_texts()[2].set_text(f'Watts ({s_probe.sProbe.watts})')

        self.l1.set_ydata(self.volty)
        self.l2.set_ydata(self.ampy)
        self.l3.set_ydata(self.watty)

        self.sp1, = self.ax1.stackplot(self.xs, self.volty, color='red', alpha=0.2)
        self.sp2, = self.ax1.stackplot(self.xs, self.ampy, color='cyan', alpha=0.2)
        self.sp3, = self.ax1.stackplot(self.xs, self.watty, color='yellow', alpha=0.2)

        return self.l1, self.l2, self.l3, self.L, self.sp3, self.sp2, self.sp1

    
    def a(self, func):
        '''
            Function to animate the plot window
            func: function to run along with animation
        '''
        ani = animation.FuncAnimation(self.fig, func, interval=1000, cache_frame_data=False, blit=True)

    
    def on_close(self):
        '''
            Closes all plots
        '''
        #print('close')
        plt.close('all')
