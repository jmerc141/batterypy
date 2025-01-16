'''
    TODO add linear regression
    TODO make plot a canvas so buttons etc can be added
'''

from matplotlib.widgets import Button, Slider
import matplotlib.pyplot as plt
import csv, json

'''
    Class that decodes history data and plots it
'''
class Hist_plot:
    showing = ''
    color = ''

    data = []
    ldata = {}

    day = ''
    current_sesh = 0
    sessions = []

    lines = []
    stackplots = []

    fig = ''
    ax1 = ''
    l1  = ''
    sp1 = ''


    '''
        Read json file into Hist_plot.data variable
    '''
    @staticmethod
    def init_history_data():
        try:
            with open('history.json') as hist:
                #Hist_plot.data = json.load(hist)
                csvFile = csv.reader(hist)
                
                    
        except IOError as e:
            raise IOError

        # Populate dict with names as keys and empty lists as values
        for k in Hist_plot.data[Hist_plot.current_sesh][0].keys():
            Hist_plot.ldata[k] = []
        

    '''
        Sets up figure and UI elements, then calls show()
    '''
    @staticmethod
    def show_plot():
        Hist_plot.fig = plt.figure(figsize=(8,6), dpi=80)
        Hist_plot.ax1 = Hist_plot.fig.add_subplot()
        Hist_plot.fig.subplots_adjust(left=0.08, right=0.95, top=0.95, bottom=0.2)
        Hist_plot.ax1.set_xlabel('Time')
        Hist_plot.ax1.set_ylabel('Power')
        
        
        #Hist_plot.ax1.xaxis.set_ticks(range(0, len(Hist_plot.data[Hist_plot.current_sesh])))
        Hist_plot.ax1.xaxis.set_ticklabels([x.split('|')[1] for x in Hist_plot.combine_reading(Hist_plot.current_sesh, 'curtime')])

        axes1  = plt.axes([0.01, 0.000001, 0.1, 0.07])
        bvolt = Button(axes1, 'Voltage', color="lightgrey", hovercolor='white')
        bvolt.on_clicked(Hist_plot.to_volts)

        axes2 = plt.axes([0.115, 0.000001, 0.1, 0.07])
        b2 = Button(axes2, 'Measured\nWh', color='lightgrey', hovercolor='white')
        b2.on_clicked(Hist_plot.to_measured_mWh)

        axes3 = plt.axes([0.222, 0.000001, 0.1, 0.07])
        b3 = Button(axes3, 'Remaining\nWh', color='lightgrey', hovercolor='white')
        b3.on_clicked(Hist_plot.to_rmWh)

        axes4 = plt.axes([0.329, 0.000001, 0.1, 0.07])
        b4 = Button(axes4, 'Measured\nAh', color='lightgrey', hovercolor='white')
        b4.on_clicked(Hist_plot.to_MmAh)

        axes5 = plt.axes([0.436, 0.000001, 0.1, 0.07])
        b5 = Button(axes5, 'Remaining\nAh', color='lightgrey', hovercolor='white')
        b5.on_clicked(Hist_plot.to_rmAh)

        axes6 = plt.axes([0.543, 0.000001, 0.1, 0.07])
        b6 = Button(axes6, 'Battery\nHealth', color='lightgrey', hovercolor='white')
        b6.on_clicked(Hist_plot.to_battHelth)

        axes7 = plt.axes([0.650, 0.000001, 0.1, 0.07])
        b7 = Button(axes7, 'Cap Diff', color='lightgrey', hovercolor='white')
        b7.on_clicked(Hist_plot.to_capdiff)

        axes8 = plt.axes([0.757, 0.000001, 0.1, 0.07])
        b8 = Button(axes8, 'Charge %', color='lightgrey', hovercolor='white')
        b8.on_clicked(Hist_plot.to_chrgp)

        axes9 = plt.axes([0.864, 0.000001, 0.1, 0.07])
        b9 = Button(axes9, 'Full Wh', color='lightgrey', hovercolor='white')
        b9.on_clicked(Hist_plot.to_fullmwh)

        sl_ax = plt.axes([0.2, 0.08, 0.7, 0.07])

        session_slider = Slider(ax=sl_ax, label='Sessions', valmin=0, valmax=len(Hist_plot.data)-1, valinit=0, valstep=1)
        
        session_slider.on_changed(Hist_plot.change_sesh)

        # Default to voltage
        Hist_plot.to_volts(0)

        plt.show()


    '''
        Gets called on slider change, changes data to another session
    '''
    @staticmethod
    def change_sesh(i):
        Hist_plot.current_sesh = i
        Hist_plot.ax1.set_title(f'Showing data from {Hist_plot.data[Hist_plot.current_sesh][0]['curtime'].split('|')[0]}')
        Hist_plot.ax1.xaxis.set_ticklabels([x.split('|')[1] for x in Hist_plot.combine_reading(Hist_plot.current_sesh, 'curtime')])
        Hist_plot.to_volts(0)

    
    '''
        Helper function to flatten a data point (key) from a session into a list
    '''
    @staticmethod
    def combine_reading(session_num, key):
        tmp = []
        t = 0
        for a in Hist_plot.data[session_num]:
            tmp.append(a[key])
        return tmp

    '''
        Re-draws line on plot to a new data point
    '''
    @staticmethod
    def lined():
        # Select which data to put in line
        l = Hist_plot.combine_reading(Hist_plot.current_sesh, Hist_plot.showing)
        
        Hist_plot.lines.append(Hist_plot.ax1.plot(l, label=Hist_plot.showing, color=Hist_plot.color, linewidth=2))

        Hist_plot.stackplots.append(Hist_plot.ax1.stackplot(range(0, len(l)), l, color=Hist_plot.color, alpha=0.2))

        Hist_plot.ax1.set_ylim(min(l)-1, max(l)+1)
        
        # Bring lines to edges
        Hist_plot.ax1.set_xlim(0, len(l)-1)

        Hist_plot.ax1.legend([Hist_plot.showing], loc=2)

        plt.draw()


    '''
        Special function that plots 3 lines instead of one
    '''
    @staticmethod
    def to_volts(p):
        Hist_plot.clear_lines()
        Hist_plot.showing = 'voltage'
        Hist_plot.color = 'red'

        v = Hist_plot.combine_reading(0, 'voltage')
        a = Hist_plot.combine_reading(0, 'amps')
        w = Hist_plot.combine_reading(0, 'watts')

        Hist_plot.lines.append(Hist_plot.ax1.plot(
            v, label=Hist_plot.showing, color=Hist_plot.color, linewidth=2))
        Hist_plot.lines.append(Hist_plot.ax1.plot(
            a, label=Hist_plot.showing, color='lightblue', linewidth=2))
        Hist_plot.lines.append(Hist_plot.ax1.plot(
            w, label=Hist_plot.showing, color='orange', linewidth=2))
        
        Hist_plot.stackplots.append(Hist_plot.ax1.stackplot(
            range(0, len(v)), v, color=Hist_plot.color, alpha=0.2))
        Hist_plot.stackplots.append(Hist_plot.ax1.stackplot(
            range(0, len(a)), a, color='lightblue', alpha=0.2))
        Hist_plot.stackplots.append(Hist_plot.ax1.stackplot(
            range(0, len(w)), w, color='orange', alpha=0.2))

        Hist_plot.ax1.set_ylim(0, max([max(v), max(a), max(w)])+1)
        Hist_plot.ax1.set_xlim(0, len(v)-1)

        Hist_plot.ax1.legend([f'Volts {round(sum(v)/len(v), 2)}',
                              f'Amps {round(sum(a)/len(a), 2)}',
                              f'Watts {round(sum(w)/len(w), 2)}'], loc=2)
        
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

    '''
        Closes plot window
    '''
    @staticmethod
    def onClose():
        Hist_plot.clear_lines()
        
        plt.close('all')
        