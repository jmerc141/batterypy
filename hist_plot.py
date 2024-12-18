'''
    TODO add linear regression
    add 
'''

from matplotlib.widgets import Button
from ipywidgets import Dropdown
import matplotlib.pyplot as plt
import json

class Hist_plot:

    showing = ''
    color = ''

    data = {}
    xaxis = []
    ldata = {'voltage': [], 'health_percent': [], "actual_mAh": [],
    "measured_Ah": [], "probes_full_Wh": [], "measured_Wh": [],
    "rem_Wh": [], "cap_diff": [], "voltage": [],
    "chrg_percent": [], 'rem_Ah': [], 'amps': [],
    'watts': [], 'curtime': []
    }

    sessions = []

    xs = []
    lines = []
    stackplots = []

    fig = ''
    ax1 = ''
    l1  = ''
    sp1 = ''

    day = ''

    #TODO multiple days?
    @staticmethod
    def init_history_data():
        try:
            with open('history.dat') as hist:
                data = json.load(hist)
        except IOError as e:
            print(e)
            raise IOError

        tmp = 0

        for a in data:
            Hist_plot.sessions.append(a)
            for x in a:
                Hist_plot.xs.append(tmp)
                Hist_plot.xaxis.append(x['curtime'].split('|')[1])
                for b in x:
                    
                    Hist_plot.ldata[b].append(x[b])
                tmp += 1
        

    @staticmethod
    def show_plot():
        Hist_plot.fig = plt.figure(figsize=(8,6), dpi=80)
        Hist_plot.ax1 = Hist_plot.fig.add_subplot()
        Hist_plot.fig.subplots_adjust(left=0.08, right=0.95, top=0.95, bottom=0.145)
        plt.title(Hist_plot.day)
        Hist_plot.ax1.set_xlabel('Time')
        Hist_plot.ax1.set_ylabel('Power')
        Hist_plot.ax1.xaxis.set_ticklabels(Hist_plot.xaxis)

        # Make buttons for switching plots
        axes1  = plt.axes([0.01, 0.000001, 0.1, 0.07])
        bvolt = Button(axes1, 'Voltage', color="lightgrey", hovercolor='white')
        bvolt.on_clicked(Hist_plot.to_volts)

        axes2 = plt.axes([0.11, 0.000001, 0.1, 0.07])
        b2 = Button(axes2, 'Measured\nWh', color='lightgrey', hovercolor='white')
        b2.on_clicked(Hist_plot.to_measured_mWh)

        axes3 = plt.axes([0.22, 0.000001, 0.1, 0.07])
        b3 = Button(axes3, 'Remaining\nWh', color='lightgrey', hovercolor='white')
        b3.on_clicked(Hist_plot.to_rmWh)

        axes4 = plt.axes([0.33, 0.000001, 0.1, 0.07])
        b4 = Button(axes4, 'Measured\nAh', color='lightgrey', hovercolor='white')
        b4.on_clicked(Hist_plot.to_MmAh)

        axes5 = plt.axes([0.44, 0.000001, 0.1, 0.07])
        b5 = Button(axes5, 'Remaining\nAh', color='lightgrey', hovercolor='white')
        b5.on_clicked(Hist_plot.to_rmAh)

        axes6 = plt.axes([0.55, 0.000001, 0.1, 0.07])
        b6 = Button(axes6, 'Battery\nHealth', color='lightgrey', hovercolor='white')
        b6.on_clicked(Hist_plot.to_battHelth)

        axes7 = plt.axes([0.66, 0.000001, 0.1, 0.07])
        b7 = Button(axes7, 'Cap Diff', color='lightgrey', hovercolor='white')
        b7.on_clicked(Hist_plot.to_capdiff)

        axes8 = plt.axes([0.77, 0.000001, 0.1, 0.07])
        b8 = Button(axes8, 'Charge %', color='lightgrey', hovercolor='white')
        b8.on_clicked(Hist_plot.to_chrgp)

        axes9 = plt.axes([0.88, 0.000001, 0.1, 0.07])
        b9 = Button(axes9, 'Full Wh', color='lightgrey', hovercolor='white')
        b9.on_clicked(Hist_plot.to_fullmwh)

        dd = Dropdown(options=[('first', 0), ('second', 1)], value=0, description='Here')
        #dd.observe()

        # Default to voltage
        Hist_plot.to_volts(0)

        plt.show()
        

    '''
    
    '''
    @staticmethod
    def lined():
        # Select which data to put in line
        l = Hist_plot.ldata[Hist_plot.showing]
        
        Hist_plot.lines.append(Hist_plot.ax1.plot(l, label=Hist_plot.showing, color=Hist_plot.color, linewidth=2))
        

        Hist_plot.stackplots.append(Hist_plot.ax1.stackplot(Hist_plot.xs, l, color=Hist_plot.color, alpha=0.2))

        Hist_plot.ax1.set_ylim(min(l)-1, max(l)+1)
        
        # Bring lines to edges
        Hist_plot.ax1.set_xlim(0, len(l)-1)

        plt.draw()


    @staticmethod
    def to_volts(p):
        Hist_plot.clear_lines()
        Hist_plot.showing = 'voltage'
        Hist_plot.color = 'red'

        Hist_plot.lines.append(Hist_plot.ax1.plot(
            Hist_plot.ldata[Hist_plot.showing], label=Hist_plot.showing, color=Hist_plot.color, linewidth=2))
        Hist_plot.lines.append(Hist_plot.ax1.plot(
            Hist_plot.ldata['amps'], label=Hist_plot.showing, color='lightblue', linewidth=2))
        Hist_plot.lines.append(Hist_plot.ax1.plot(
            Hist_plot.ldata['watts'], label=Hist_plot.showing, color='orange', linewidth=2))
        
        Hist_plot.stackplots.append(Hist_plot.ax1.stackplot(
            Hist_plot.xs, Hist_plot.ldata[Hist_plot.showing], color=Hist_plot.color, alpha=0.2))
        Hist_plot.stackplots.append(Hist_plot.ax1.stackplot(
            Hist_plot.xs, Hist_plot.ldata['amps'], color='lightblue', alpha=0.2))
        Hist_plot.stackplots.append(Hist_plot.ax1.stackplot(
            Hist_plot.xs, Hist_plot.ldata['watts'], color='orange', alpha=0.2))
        
        Hist_plot.ax1.set_ylim(0, max(Hist_plot.ldata['watts'])+1)
        Hist_plot.ax1.set_xlim(0, len(Hist_plot.ldata['watts'])-1)
        
        plt.draw()
            

    @staticmethod
    def to_measured_mWh(p):
        if p.button == 1:
            #plt.title('Measured milli-Watt hour')
            Hist_plot.clear_lines()
            Hist_plot.showing = 'measured_Wh'
            Hist_plot.color = 'orange'
            Hist_plot.lined()


    @staticmethod
    def to_rmAh(p):
        if p.button == 1:
            Hist_plot.clear_lines()
            Hist_plot.showing = 'rem_Ah'
            Hist_plot.color = 'yellow'
            Hist_plot.ax1.set_ylabel('Ah')
            Hist_plot.lined()


    @staticmethod
    def to_rmWh(p):
        if p.button == 1:
            Hist_plot.clear_lines()
            Hist_plot.showing = 'rem_Wh'
            Hist_plot.color = 'green'
            Hist_plot.ax1.set_ylabel('Wh')
            Hist_plot.lined()


    @staticmethod
    def to_battHelth(p):
        if p.button == 1:
            Hist_plot.clear_lines()
            Hist_plot.showing = 'health_percent'
            Hist_plot.color = 'blue'
            Hist_plot.ax1.set_ylabel('%')
            Hist_plot.lined()


    @staticmethod
    def to_MmAh(p):
        if p.button == 1:
            #plt.title('Measured milli-Amp hour')
            Hist_plot.clear_lines()
            Hist_plot.showing = 'measured_Ah'
            Hist_plot.color = 'indigo'
            Hist_plot.ax1.set_ylabel('Ah')
            Hist_plot.lined()


    @staticmethod
    def to_capdiff(p):
        if p.button == 1:
            Hist_plot.clear_lines()
            Hist_plot.showing = 'cap_diff'
            Hist_plot.color = 'violet'
            Hist_plot.ax1.set_ylabel('Wh')
            Hist_plot.lined()

    '''
    linear regression
    '''
    @staticmethod
    def to_chrgp(p):
        if p.button == 1:
            Hist_plot.clear_lines()
            Hist_plot.showing = 'chrg_percent'
            Hist_plot.color = 'brown'
            Hist_plot.ax1.set_ylabel('%')
            Hist_plot.lined()


    @staticmethod
    def to_fullmwh(p):
        if p.button == 1:
            Hist_plot.clear_lines()
            Hist_plot.showing = 'probes_full_Wh'
            Hist_plot.color = 'black'
            Hist_plot.ax1.set_ylabel('Wh')
            Hist_plot.lined()


    @ staticmethod
    def clear_lines():
        #print(Hist_plot.lines)
        if len(Hist_plot.lines) != 0:
            for l in Hist_plot.lines:
                l.pop(0).remove()
            Hist_plot.lines.clear()
        #print(Hist_plot.lines)
        
        if len(Hist_plot.stackplots) != 0:
            for s in Hist_plot.stackplots:
                s.pop().remove()

            Hist_plot.stackplots.clear()

    @staticmethod
    def onClose():
        Hist_plot.clear_lines()
        
        plt.close('all')
        