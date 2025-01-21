'''
credit to Freepik for battery image:
    <a href="https://www.flaticon.com/free-icons/battery" title="battery icons">Battery icons created by Freepik - Flaticon</a>

add gridlines to single / multi plot
'''

import sys, os, internal, plot, hplot
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
        self.master.geometry('450x500')
        self.master.resizable(False, False)

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
                import s_probe
                self.sp = s_probe.sProbe()
                self.sp.th.start()
            except Exception as e:
                tk.messagebox.showerror('Error', f'Error initializing sprobe\nAre you using a desktop?\n{e}')
            try:
                import treev
                self.tree = treev
                pass
            except TypeError as t:
                tk.messagebox.showerror('Error', f'Error initializing tree\n{t}')
                self.master.on_close()
            

            if os.path.exists('./res/battery.ico'):
                self.master.iconbitmap('./res/battery.ico')
        else:
            print('Incompatible system, exiting')
            sys.exit()

        # Change dir again so history.csv writes to .exe dir
        if getattr(sys, 'frozen', False):
            os.chdir(os.path.dirname(sys.executable))
        else:
            os.chdir(os.path.dirname(os.path.abspath(__file__)))

        # Menubar
        mb = tk.Menu(self.master, background='black', fg='white')
        file_menu = tk.Menu(mb, tearoff=False)
        view_menu = tk.Menu(mb, tearoff=False)
        #graph = tk.Menu(view_menu, tearoff=False)
        ext = tk.Menu(mb, tearoff=False)
        track_menu = tk.Menu(mb, tearoff=False)

        mb.add_cascade(label='File', menu=file_menu)
        mb.add_cascade(label='Graph', menu=view_menu)
        mb.add_cascade(label='Tracking', menu=track_menu)
        mb.add_cascade(label='Extra', menu=ext)

        self.track_en = tk.BooleanVar()

        # TODO add fonts
        view_menu.add_checkbutton(label='Live Graph (Internal)', command=self.create_internal_graph)
        #view_menu.add_cascade(label='Graph (external)', menu=graph)
        view_menu.add_command(label='Live Graph Single', command=self.create_external_single)
        view_menu.add_command(label='Live Graph Multiple', command=self.create_external_graph)
        view_menu.add_command(label='History Graph', command=self.show_history)
        track_menu.add_checkbutton(label='Enable Tracking', command=self.start_track, variable=self.track_en)
        track_menu.add_command(label='Clear Tracking History', command=self.ask_clear_hist)
        
        #if sys.platform == 'win32':
        #    ext.add_command(label='Win32_Battery', command=self.tree.get_win32batt)
        #    ext.add_command(label='Win32_PortableBattery', command=self.tree.get_portable)
        #    ext.add_command(label='Root\\Wmi', command=self.tree.get_rootwmi)

        file_menu.add_command(label='Exit', command=self.on_close)
        
        self.master.config(menu=mb)

        #self.tree.tree.bind('<<TreeviewSelect>>', self.item_selected)

        # Horizontal scrollbar
        #scrollx = ttk.Scrollbar(self.master, orient=tk.HORIZONTAL, command=self.tree.tree.xview)
        #scrollx.grid(row=1, column=0, sticky='ew', padx=(10,0), pady=(0,10))

        # Vertical scrollbar
        #scrolly = ttk.Scrollbar(self.master, orient=tk.VERTICAL, command=self.tree.tree.yview)
        #scrolly.grid(row=0, column=0, sticky='nse', padx=(10,0), pady=10, rowspan=1)
        #self.tree.tree.configure(yscroll=scrolly.set)
        
        # TODO Fix tree not expanding to top of powerinfo frame
        # Resize the window vertically and there is a space between the bottom
        # of TreeView and top of PowerInfo Frame
        

        self.tv = self.Treeview(['Property', 'Value', 'Max'], [10, 10, 5], 14, self.tree.setup_tree(self.sp),
                                'subdata', ['prop', 'val', 'max'], row=0, col=0, pady=(10,0))
        
        
        
        pi = self.addLabelFrame('Power Info', padx=10, pady=(0,5), sticky='sew', row=1, col=0, 
                                 widgetkwargs={'height': 120}, )
        
        
        pi.master.grid_propagate(False)
        
        self.master.rowconfigure(0, weight=2)  # Top frame expands
        self.master.rowconfigure(1, weight=0)  # Bottom frame stays fixed
        
        
        # TODO implement linux
        self.v = tk.DoubleVar(value=s_probe.sProbe.voltage)
        self.w = tk.DoubleVar(value=s_probe.sProbe.watts)
        self.c = tk.DoubleVar(value=s_probe.sProbe.amps)
        
        v = pi.addFrame('volt', row=0, col=0, sticky='ew', padx=0, pady=0)
        a = pi.addFrame('amps', row=1, col=0, sticky='ew', padx=0, pady=0)
        w = pi.addFrame('watts', row=2, col=0, sticky='ew', padx=0, pady=0)

        v.Label('Voltage', row=0, col=0, size=10, pady=(0,0), sticky='sw')
        v.Label('', row=0, col=1, size=10, pady=0, sticky='e', widgetkwargs={'textvariable': self.v})
        v.Progressbar(variable=self.v, row=1, col=0, upper=20, pady=0, colspan=2, sticky='nsew')
        
        # TODO change upper value
        a.Label('Current (Amps)', row=0, col=0, size=10, pady=0, sticky='sw')
        a.Label('', row=0, col=1, size=10, pady=0, sticky='e', widgetkwargs={'textvariable': self.c})
        a.Progressbar(variable=self.c, upper=6, row=1, col=0, pady=0, colspan=2, sticky='nsew')
        
        # TODO change upper value
        w.Label('Wattage', row=0, col=0, size=10, pady=(0,0), sticky='sw')
        w.Label('', row=0, col=1, size=10, pady=0, sticky='e', widgetkwargs={'textvariable': self.w})
        w.Progressbar(variable=self.w, row=1, col=0, pady=(0,10), colspan=2, sticky='nswe')

        # Strech progressbars horizontally
        v.master.columnconfigure(0, weight=1)
        a.master.columnconfigure(0, weight=1)
        w.master.columnconfigure(0, weight=1)
        
        #self.debugPrint()
        self.updateUI()


    '''
        Set values in the treeview, runs every 1 second
    '''
    def updateUI(self):
        # overwrites values in the treeview, use only dynamic values
        self.v.set(f'{self.sp.voltage:.3f}')
        self.c.set(f'{self.sp.amps:.3f}')
        self.w.set(f'{self.sp.watts:.3f}')
        self.tree.update(self.tv, self.sp)
        #print(self.master.winfo_height() // 33)
        #self.tv.config(height=self.master.winfo_height() // 33)
        self.master.after(1000, self.updateUI)
        

    def start_track(self):
        if self.sp.win32bat['EstimatedChargeRemaining'] == 100:
            tk.messagebox.showerror('Error', f'Not tracking when battery is 100%')
            self.track_en.set(False)
        else:
            self.sp.activate_tracking()
            

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
        #try:
        #    self.tree.on_close()
        #except Exception as e:
        #    print('bad')
        plot.plt.close()
        self.sp.on_close()
        self.master.update()
        self.master.destroy()

