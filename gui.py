'''
credit to Freepik for battery image:
    <a href="https://www.flaticon.com/free-icons/battery" title="battery icons">Battery icons created by Freepik - Flaticon</a>

powercfg /batteryreport /output PATH

Warning about overlapping widgets can be ignored
'''

lazy import sys, os, internal, plot, hplot, s_probe, treev, pyglet, settings
lazy import tkinter as tk
lazy import tkinter.messagebox
lazy import TKinterModernThemes as TKMT
lazy from idlelib.tooltip import Hovertip
lazy from tkinter import ttk, messagebox

sys.path.append(".")

if sys.platform == 'linux':
    try:
        s_probe.sProbe.activate_l()
        s_probe.sProbe.th.start()
    except Exception as e:
        messagebox.showerror('Error', f'Error initializing sprobe\nAre you using a desktop?\n{e}')
        exit()
    
elif sys.platform == 'win32':
    try:
        s_probe.sProbe.activate()
        s_probe.sProbe.th.start()
    except Exception as e:
        import traceback
        messagebox.showerror('Error', f'Error initializing sprobe\nAre you using a desktop?\n{e}')
        traceback.print_exception(type(e), e, e.__traceback__)
        exit()
else:
    print('Incompatible system, exiting')
    sys.exit()


class App(TKMT.ThemedTKinterFrame):
    def __init__(self, theme, mode, usecommandlineargs=True, usethemeconfigfile=True):
        super().__init__('Batterypy', theme, mode, usecommandlineargs, usethemeconfigfile)
        # Run on_close when window is closed
        self.master.protocol('WM_DELETE_WINDOW', self.on_close)

        # Change directory to get icon resource
        try:
            os.chdir(sys._MEIPASS)
        except Exception:
            self.base_path = os.path.abspath(".")

        if sys.platform == 'linux':
            if os.path.exists('./res/battery.png'):
                # should set small top-right corner icon
                i = tk.PhotoImage(file='./res/battery.png')
                self.master.iconphoto(False, i)

            if os.path.exists('./res/battery.png'):
                # Set taskbar icon
                i = tk.PhotoImage(file='./res/battery.png')
                self.master.call('wm', 'iconphoto', self.master._w, i)
        elif sys.platform == 'win32':
            ico = '.\\res\\battery.ico'
            if os.path.exists(ico):
                # Set small corner icon
                self.master.iconbitmap(ico)

        pyglet.font.add_file(f'res/{settings.s['font']}.ttf')

        # Toggle internal plot display bool
        self.internal = False
        self.hist_init = False

        # Placeholder for internal or external graph
        self.i_pl = None
        self.pl = None

        self.bars_active = False

        # Set window size
        self.wid = 450
        self.hei = 500
        self.master.geometry(f'{self.wid}x{self.hei}')
        
        #self.master.resizable(False, False)    

        # Change dir again so history.csv writes to .exe dir
        if getattr(sys, 'frozen', False):
            os.chdir(os.path.dirname(sys.executable))
        else:
            os.chdir(os.path.dirname(os.path.abspath(__file__)))

        # Menubar
        mb = tk.Menu(self.master, background='black', fg='white')
        file_menu = tk.Menu(mb, tearoff=False)
        graph_menu = tk.Menu(mb, tearoff=False)
        track_menu = tk.Menu(mb, tearoff=False)

        mb.add_cascade(label='File', menu=file_menu)
        mb.add_cascade(label='Graph', menu=graph_menu)
        mb.add_cascade(label='Tracking', menu=track_menu)

        self.track_en = tk.BooleanVar()

        file_menu.add_command(label='Exit', command=self.on_close)

        graph_menu.add_command(label='Live Graph Single', command=self.create_external_single)
        graph_menu.add_command(label='Live Graph Multiple', command=self.create_external_graph)
        graph_menu.add_command(label='History Graph', command=self.show_history)

        track_menu.add_checkbutton(label='Enable Tracking', command=self.start_track, variable=self.track_en)
        track_menu.add_command(label='Clear Tracking History', command=self.ask_clear_hist)
        
        self.master.config(menu=mb)

        self.tv = self.Treeview(['Property', 'Value', 'Max'], [80, 90, 0], self.hei // 33, treev.Treev.setup_tree(),
                                'subdata', ['prop', 'val', 'max'], row=0, col=0, colspan=2, pady=5, padx=(10, 5))

        self.master.rowconfigure(0, weight=1)
        self.master.columnconfigure(0, weight=1)       
        
        #self.tv.bind('<<TreeviewSelect>>', self.item_selected)
        if s_probe.sProbe.health < 80:
            ht = Hovertip(self.tv, 'A battery\'s end of life is typically when the FullChargeCapacity property\nfalls below 80% of the DesignCapacity property')
        
        s = ttk.Style()
        s.configure('.', font=(f'{settings.s['font']}', settings.s['font_size']))
        s.configure('Treeview', indent=10)

        self.btn = self.AccentButton('Power Info', self.to_bars, row=2, col=0, pady=5)

        
        #self.debugPrint()
        self.updateUI()


    '''
        Set values in the treeview, runs every 1 second
    '''
    def updateUI(self):
        # overwrites values in the treeview, use only dynamic values
        if self.bars_active:
            self.v.set(f'{s_probe.sProbe.voltage:.3f}')
            self.c.set(f'{s_probe.sProbe.amps:.3f}')
            self.w.set(f'{s_probe.sProbe.watts:.3f}')
        else:
            # Update values in tree view 
            treev.Treev.update(self.tv)
            #if self.master.winfo_height() > 10:
            #    self.tv.config(height=self.master.winfo_height() // 33)
        self.master.after(1000, self.updateUI)
        

    def to_bars(self):
        if not self.bars_active:
            self.btn.configure(text='Back')
            self.bars_active = True

            tree = self.tv
            container = tree.master
            if container is self.master:
                for child in container.winfo_children():
                    if isinstance(child, ttk.Scrollbar):
                        child.destroy()
                tree.destroy()
            else:
                container.destroy()
            self.tv = None

            self.pi = self.addLabelFrame('Power Info', sticky='nsew', row=0, col=0, padx=10, pady=5, colspan=2)
            
            #pi.master.grid_propagate(False)
            #pi.master.rowconfigure(0, minsize=32)
            
            self.v  = tk.DoubleVar(value=s_probe.sProbe.voltage)
            self.w  = tk.DoubleVar(value=s_probe.sProbe.watts)
            self.c  = tk.DoubleVar(value=s_probe.sProbe.amps)
            self.hb = tk.DoubleVar(value=round(s_probe.sProbe.health, 1))
            
            v = self.pi.addFrame('volt', row=0, col=0, sticky='ns', padx=0, pady=5)
            a = self.pi.addFrame('amps', row=0, col=1, sticky='ns', padx=0, pady=5)
            w = self.pi.addFrame('watts', row=0, col=2, sticky='ns', padx=0, pady=5)
            health_bar = self.pi.addFrame('health', row=0, col=3, sticky='ns', padx=5, pady=5)

            v.Label('Volts', row=0, col=0, size=10, pady=(0,0), sticky='n',
                fontargs=('-family', f'{settings.s['font']}', '-size', f'{settings.s['font_size']}'))
            v.Progressbar(variable=self.v, row=1, col=0, upper=20, sticky='ns', widgetkwargs={'orient': 'vertical'})
            v.Label('', row=2, col=0, size=10, pady=(0,0), sticky='n', widgetkwargs={'textvariable': self.v},
                fontargs=('-family', f'{settings.s['font']}', '-size', f'{settings.s['font_size']}'))
            
            # TODO change upper value
            a.Label('Amps', row=0, col=0, size=10, pady=0, sticky='n',
                fontargs=('-family', f'{settings.s['font']}', '-size', f'{settings.s['font_size']}'))
            a.Progressbar(variable=self.c, upper=6, row=1, col=0, sticky='ns', widgetkwargs={'orient': 'vertical'})
            a.Label('', row=2, col=0, size=10, pady=0, sticky='s', widgetkwargs={'textvariable': self.c},
                fontargs=('-family', f'{settings.s['font']}', '-size', f'{settings.s['font_size']}'))
            
            # TODO change upper value
            w.Label('Watts', row=0, col=0, size=10, pady=(0,0), 
                fontargs=('-family', f'{settings.s['font']}', '-size', f'{settings.s['font_size']}'))
            w.Progressbar(variable=self.w, row=1, col=0, sticky='ns', widgetkwargs={'orient': 'vertical'})
            w.Label('', row=2, col=0, size=10, pady=(0,0), sticky='s', widgetkwargs={'textvariable': self.w},
                fontargs=('-family', f'{settings.s['font']}', '-size', f'{settings.s['font_size']}'))

            health_bar.Label('Health %', row=0, col=0, size=10, pady=0, sticky='n',
                fontargs=('-family', f'{settings.s['font']}', '-size', f'{settings.s['font_size']}'))
            tmp = health_bar.Progressbar(variable=self.hb, row=1, col=0, sticky='ns', widgetkwargs={'orient': 'vertical'})
            health_bar.Label('', row=2, col=0, size=10, pady=(0,0), sticky='n', widgetkwargs={'textvariable': self.hb},
                fontargs=('-family', f'{settings.s['font']}', '-size', f'{settings.s['font_size']}'))
            
            self.plf = ttk.Frame()
            self.i_pl = internal.Window(self.plf)
            self.plf.grid(column=0, row=1, sticky='nw', pady=5, rowspan=1)

            # Strech progressbars
            #for x in range()
            #self.pi.master.columnconfigure(0, weight=1)
            #self.pi.master.columnconfigure(1, weight=1)
            #self.pi.master.columnconfigure(2, weight=1)
            #self.pi.master.columnconfigure(3, weight=1)
            self.pi.master.rowconfigure(0, weight=1)
            i=0
            for el in (v, a, w, health_bar):
                self.pi.master.columnconfigure(i, weight=1)
                el.master.columnconfigure(0, weight=1)
                el.master.rowconfigure(1, weight=1)
                i=i+1
            
            
        else:
            self.i_pl.destroy()
            self.plf.destroy()
            self.i_pl = None
            self.pi.master.destroy()
            self.pi = None
            self.btn.configure(text='Power Info')
            
            self.tv = self.Treeview(['Property', 'Value', 'Max'], [80, 90, 0], self.hei // 33, treev.Treev.setup_tree(),
                                'subdata', ['prop', 'val', 'max'], row=0, col=0, colspan=2, pady=5, padx=(10,5))

            self.bars_active = False


    def start_track(self):
        if s_probe.sProbe.chargeRemaining == 100:
            messagebox.showerror('Error', f'Not tracking when battery is 100%')
            self.track_en.set(False)
        else:
            s_probe.sProbe.activate_tracking()


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
        if messagebox.askyesno('Delete?', 'Delete all history data?'):
            s_probe.sProbe.del_history()

    '''
        Creates external window with single plot
    '''
    def create_external_single(self):
        self.pl = plot.Plot(1)
        self.pl.on_close()
        self.pl = None


    '''
        Runs when main window is closed
    '''
    def on_close(self):
        #try:
        #    self.tree.on_close()
        #except Exception as e:
        #    print('bad')
        plot.plt.close()
        s_probe.sProbe.on_close()
        self.master.update()
        self.master.destroy()

