from matplotlib.widgets import Button
import matplotlib.pyplot as plt
import json

class Hist_plot:

    showing = ''
    color = ''

    data = {}
    xaxis = []
    ldata = {'voltage': [], 'health_percent': [], "actual_mAh": [],
    "measured_mAh": [], "probes_full_mWh": [], "measured_mWh": [],
    "rem_mWh": [], "cap_diff": [], "voltage": [],
    "chrg_percent": []
    }
    xs = []

    ax1 = ''
    l1  = ''
    sp1 = ''

    #TODO multiple days?
    @staticmethod
    def show_history_data():
        try:
            # Check if last char is ]
            with open('history.dat') as hist:
                data = json.load(hist)
        except IOError as e:
            print(e)
            return

        fig = plt.figure(figsize=(8,6), dpi=80)
        Hist_plot.ax1 = fig.add_subplot()
        #fig.subplots_adjust()
        
        # Days split('|') need loop
        day = list(data[0].keys())[0].split('|')[0]

        tmp = 0

        for a in data:
            for x in a:
                Hist_plot.xs.append(tmp)
                Hist_plot.xaxis.append(x.split('|')[1])
                for b in list(list(a.values())[0].keys()):
                    Hist_plot.ldata[b].append(a[x][b])
                tmp += 1
                
        plt.title(day)
        Hist_plot.ax1.set_xlabel('Time')
        Hist_plot.ax1.xaxis.set_ticklabels(Hist_plot.xaxis)
        
        axes1  = plt.axes([0.5, 0.000001, 0.1, 0.07])
        bvolt = Button(axes1, 'Voltage', color="red", hovercolor='grey')
        bvolt.on_clicked(Hist_plot.to_volts)

        axes2 = plt.axes([0.61, 0.000001, 0.1, 0.075])
        bmmwh = Button(axes2, 'M mWh', color='purple', hovercolor='grey')
        bmmwh.on_clicked(Hist_plot.to_measured_mWh)

        # Default to voltage
        Hist_plot.showing = 'voltage'
        Hist_plot.color = 'red'
        Hist_plot.lined()

        plt.tight_layout()
        plt.show()
        

    @staticmethod
    def lined():
        # Select which data to put in line
        l = Hist_plot.ldata[Hist_plot.showing]
        
        Hist_plot.l1 = Hist_plot.ax1.plot(l, label=Hist_plot.showing, color=Hist_plot.color, linewidth=2)

        Hist_plot.sp1 = Hist_plot.ax1.stackplot(Hist_plot.xs, l, color=Hist_plot.color, alpha=0.2)

        Hist_plot.ax1.set_ylim(min(l)-0.1, max(l)+0.1)
        Hist_plot.ax1.set_xlim(0, len(l))

        plt.draw()


    @staticmethod
    def to_volts(p):
        if p.button == 1:
            Hist_plot.l1.pop(0)
            Hist_plot.showing = 'voltage'
            Hist_plot.color = 'red'
            Hist_plot.lined()


    @staticmethod
    def to_measured_mWh(p):
        if p.button == 1:
            t = Hist_plot.sp1.pop(0)
            t.remove()
            Hist_plot.showing = 'measured_mWh'
            Hist_plot.color = 'purple'
            Hist_plot.lined()
            