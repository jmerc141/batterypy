'''
credit to Freepik for battery image:
    <a href="https://www.flaticon.com/free-icons/battery" title="battery icons">Battery icons created by Freepik - Flaticon</a>

add gridlines to single / multi plot
'''

import sys, os, internal, plot, hist_plot, hplot
import tkinter as tk
from tkinter import ttk
import TKinterModernThemes as TKMT

sys.path.append(".")

class App(TKMT.ThemedTKinterFrame):
    def __init__(self, theme, mode, usecommandlineargs=True, usethemeconfigfile=True):
        super().__init__('Batterypy', theme, mode, usecommandlineargs, usethemeconfigfile)
        # Run on_close when window is closed
        self.master.protocol('WM_DELETE_WINDOW', self.on_close)

        # Toggle internal plot display bool
        self.internal = False
        # Toggle Treeview entries
        self.portable_on = False
        self.win32bat_on = False
        self.rootwmi_on = False

        self.hist_init = False

        # Change directory to get icon resource
        try:
            os.chdir(sys._MEIPASS)
        except Exception:
            self.base_path = os.path.abspath(".")
        

        # Placeholder for internal or external graph
        self.i_pl = None
        self.pl = None

        # Set window size
        self.master.geometry('600x700')

        # Create Treev object depending on linux/win platform because
        # implementations are different
        if sys.platform == 'linux':
            import tree_l, s_probe_l
            self.tree = tree_l.Treev(self.master)
            if os.path.exists('./res/battery.png'):
                # should set small top-right corner icon
                i = tk.PhotoImage(file='./res/battery.png')
                self.master.iconphoto(False, i)
        elif sys.platform == 'win32':
            try:
                import tree, s_probe
                self.sp = s_probe
                self.tree = tree.Treev(self.master)
            except TypeError as t:
                tk.messagebox.showerror('Error', f'Win32Battery not found\nAre you using a desktop?\n{t}')
                self.master.on_close()
            if os.path.exists('./res/battery.ico'):
                self.master.iconbitmap('./res/battery.ico')
        else:
            print('Incompatible system, exiting')
            sys.exit()

        # Change dir again so history.json write to .exe dir
        if getattr(sys, 'frozen', False):
            os.chdir(os.path.dirname(sys.executable))
        else:
            os.chdir(os.path.dirname(os.path.abspath(__file__)))

        # Menubar
        mb = tk.Menu(self.master, background='black', fg='white')
        file_menu = tk.Menu(mb, tearoff=False)
        view_menu = tk.Menu(mb, tearoff=False)
        graph = tk.Menu(view_menu, tearoff=False)
        ext = tk.Menu(mb, tearoff=False)
        track_menu = tk.Menu(mb, tearoff=False)

        mb.add_cascade(label='File', menu=file_menu)
        mb.add_cascade(label='Graph', menu=view_menu)
        mb.add_cascade(label='Tracking', menu=track_menu)
        mb.add_cascade(label='Extra', menu=ext)

        # TODO add fonts
        view_menu.add_checkbutton(label='Graph (Internal)', command=self.create_internal_graph)
        view_menu.add_cascade(label='Graph (external)', menu=graph)
        graph.add_command(label='Single', command=self.create_external_single)
        graph.add_command(label='Multiple', command=self.create_external_graph)
        track_menu.add_checkbutton(label='Enable Tracking', command=s_probe.sProbe.activate_tracking)
        track_menu.add_command(label='View History', command=self.show_history)
        track_menu.add_command(label='Clear History', command=self.ask_clear_hist)
        
        if sys.platform == 'win32':
            ext.add_command(label='Win32_Battery', command=self.tree.get_win32batt)
            ext.add_command(label='Win32_PortableBattery', command=self.tree.get_portable)
            ext.add_command(label='Root\\Wmi', command=self.tree.get_rootwmi)

        file_menu.add_command(label='Exit', command=self.on_close)
        
        self.master.config(menu=mb)

        self.tree.tree.bind('<<TreeviewSelect>>', self.item_selected)

        # Horizontal scrollbar
        #scrollx = ttk.Scrollbar(self.master, orient=tk.HORIZONTAL, command=self.tree.tree.xview)
        #scrollx.grid(row=1, column=0, sticky='ew', padx=(10,0), pady=(0,10))

        # Vertical scrollbar
        scrolly = ttk.Scrollbar(self.master, orient=tk.VERTICAL, command=self.tree.tree.yview)
        scrolly.grid(row=0, column=0, sticky='nse', padx=(10,0), pady=10)
        self.tree.tree.configure(yscroll=scrolly.set)
        
        self.tree.tree.grid(row=0, column=0, sticky='nsew', padx=10, pady=10, columnspan=1)

        # TODO implement linux
        self.v = tk.DoubleVar(value=s_probe.sProbe.voltage)
        self.w = tk.DoubleVar(value=s_probe.sProbe.watts)
        self.c = tk.DoubleVar(value=s_probe.sProbe.amps)

        pi = self.addLabelFrame('Power Info', row=1, col=0, padx=10, pady=5)

        pi.Label('Voltage', row=0, col=0, size=10, pady=(10,0), sticky='w')
        pi.Label('', row=0, col=1, size=10, pady=0, sticky='e', widgetkwargs={'textvariable': self.v})
        pi.Progressbar(variable=self.v, row=1, col=0, upper=20, pady=0, colspan=2)

        # TODO change upper value
        pi.Label('Current (Amps)', row=2, col=0, size=10, pady=0, sticky='w')
        pi.Label('', row=2, col=1, size=10, pady=0, sticky='e', widgetkwargs={'textvariable': self.c})
        pi.Progressbar(variable=self.c, upper=5, row=3, col=0, pady=0, colspan=2)
        

        # TODO change upper value
        pi.Label('Wattage', row=4, col=0, size=10, pady=(10,0), sticky='w')
        pi.Label('', row=4, col=1, size=10, pady=0, sticky='e', widgetkwargs={'textvariable': self.w})
        pi.Progressbar(variable=self.w, row=5, col=0, pady=0, colspan=2)

        # Strech progressbars horizontally
        pi.master.columnconfigure(0, weight=1)

        #self.debugPrint()

        self.retree()


    '''
        Creates / destroys internal graph, changes window size
    '''
    def create_internal_graph(self):
        self.internal = not self.internal
        if self.internal:
            self.plf = ttk.Frame()
            self.i_pl = internal.Window(self.plf)
            self.plf.grid(column=2, row=0, sticky='w', pady=5)
            self.master.geometry('1200x700')
        else:
            self.i_pl.destroy()
            self.plf.destroy()
            self.i_pl = None
            self.master.geometry('600x700')


    '''
        Creates external window with multi-plot
    '''
    def create_external_graph(self):
        self.pl = plot.Plot(0)
        self.pl.on_close()
        self.pl = None


    '''
    
    '''
    def show_history(self):
        history_plot = hplot.Window(master=self.master)
        
        
        
        '''
        if not self.hist_init:
            try:
                hist_plot.Hist_plot.init_history_data()
                self.hist_init = True
            except Exception as e:
                tk.messagebox.showerror('Error', f'No history data found\n{e}')
            
            hist_plot.Hist_plot.show_plot()
            hist_plot.Hist_plot.onClose()
            
        else:
            hist_plot.Hist_plot.show_plot()
        '''

    
    '''
    
    '''
    def ask_clear_hist(self):
        if tk.messagebox.askyesno('Delete?', 'Delete all history data?'):
            self.sp.sProbe.del_history()

    '''
        Creates external window with single plot
    '''
    def create_external_single(self):
        self.pl = plot.Plot(1)
        self.pl.on_close()
        self.pl = None
            
    '''
        Set values in the treeview, runs every 1 second
    '''
    def retree(self):
        # overwrites values in the treeview, use only dynamic values
        self.c.set(self.sp.sProbe.amps)
        self.v.set(self.sp.sProbe.voltage)
        self.w.set(self.sp.sProbe.watts)
        
        self.tree.re_tree()
        self.master.after(1000, self.retree)


    '''
        Runs when an item on the treeview is clicked
        event: item clicked
    '''
    def item_selected(self, event):
        self.item = self.tree.tree.item(self.tree.tree.selection()[0])['text']
        # If graph is instantiated
        if self.i_pl is not None:
            # Everything that can be graphed
            if 'Voltage' == self.item:
                self.i_pl.set_prop(self.item)
            if 'Amperage' == self.item:
                self.i_pl.set_prop(self.item)
            if 'Discharge Power' == self.item:
                self.i_pl.set_prop(self.item)
            if 'Charge Power' == self.item:
                self.i_pl.set_prop(self.item)
        

    '''
        Runs when main window is closed
    '''
    def on_close(self):
        try:
            self.tree.on_close()
        except Exception as e:
            print('bad')
        plot.plt.close()
        self.master.update()
        self.master.destroy()

