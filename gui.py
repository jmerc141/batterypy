'''
credit to Freepik for battery image: <a href="https://www.flaticon.com/free-icons/battery" title="battery icons">Battery icons created by Freepik - Flaticon</a>
'''

import sys, os, internal, plot, matplotlib.font_manager
import tkinter as tk
from tkinter import ttk

sys.path.append(".")

class App(tk.Tk):

    def __init__(self):
        super().__init__()
        self.protocol('WM_DELETE_WINDOW', self.on_close)

        self.internal = False
        self.portable_on = False
        self.win32bat_on = False
        self.rootwmi_on = False
        self.dark = False

        # Change directory to get icon resource
        try:
            os.chdir(sys._MEIPASS)
        except Exception:
            self.base_path = os.path.abspath(".")

        self.s = ttk.Style()
        self.s.configure('Treeview', font=['CascadiaMono', 10, 'normal'])
        try:
            self.tk.call('lappend', 'auto_path', 'res/awthemes-10.4.0')
            self.tk.call('package', 'require', 'awdark')
        except Exception as e:
            tk.messagebox.showerror('Error', f'Could not load themes\n{e}')

        # Placeholder for internal or external graph
        self.i_pl = None
        self.pl = None

        # creating tkinter window
        self.title('BatteryPy')
        self.geometry('600x700')

        if sys.platform == 'linux':
            import tree_l
            self.tree = tree_l.Treev(self)
            if os.path.exists('./res/battery.png'):
                # should set small top-right corner icon
                i = tk.PhotoImage(file='./res/battery.png')
                self.iconphoto(False, i)
        elif sys.platform == 'win32':
            try:
                import tree
                self.tree = tree.Treev(self)
            except TypeError as t:
                tk.messagebox.showerror('Error', f'Win32Battery not found\nAre you using a desktop?\n{e}')
                self.on_close()

            if os.path.exists('./res/battery.ico'):
                self.iconbitmap('./res/battery.ico')
        else:
            print('Incompatible system, exiting')
            sys.exit()

        #self.tree = tree.Treev(self)

        # Menubar
        mb = tk.Menu(self)
        file_menu = tk.Menu(mb, tearoff=False)
        view_menu = tk.Menu(mb, tearoff=False)
        theme_menu = tk.Menu(mb, tearoff=False)
        graph = tk.Menu(view_menu, tearoff=False)
        ext = tk.Menu(mb, tearoff=False)

        mb.add_cascade(label='File', menu=file_menu)
        mb.add_cascade(label='View', menu=view_menu)
        mb.add_cascade(label='Theme', menu=theme_menu)
        mb.add_cascade(label='Extra', menu=ext)
        # TODO add fonts
        view_menu.add_checkbutton(label='Graph (Internal)', command=self.create_internal_graph)

        view_menu.add_cascade(label='Graph (external)', menu=graph)
        graph.add_command(label='Single', command=self.create_external_single)
        graph.add_command(label='Multiple', command=self.create_external_graph)
        
        if sys.platform == 'win32':
            ext.add_command(label='Win32_Battery', command=self.tree.get_win32batt)
            ext.add_command(label='Win32_PortableBattery', command=self.tree.get_portable)
            ext.add_command(label='Root\Wmi', command=self.tree.get_rootwmi)

        file_menu.add_command(label='Exit', command=self.on_close)
        #theme_menu.add_command(label='Default', command=self.default_theme)
        theme_menu.add_checkbutton(label='Dark', command=self.dark_theme)
        self.config(menu=mb)

        self.tree.tree.bind('<<TreeviewSelect>>', self.item_selected)

        # treeview stretches with window
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.retree()


    def create_internal_graph(self):
        self.internal = not self.internal
        if self.internal:
            self.plf = ttk.Frame()
            self.i_pl = internal.Window(self.plf, self.dark)
            self.plf.grid(column=2, row=0, sticky='w')
            self.geometry('1200x700')
        else:
            self.i_pl.destroy()
            self.plf.destroy()
            self.i_pl = None
            self.geometry('600x700')


    def create_external_graph(self):
        self.pl = plot.Plot(0)
        self.pl.on_close()
        self.pl = None


    def create_external_single(self):
        self.pl = plot.Plot(1, self.dark)
        self.pl.on_close()
        self.pl = None
            

    def retree(self):
        # overwrites values in the treeview, use only dynamic values
        self.tree.re_tree()
        self.after(1000, self.retree)


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


    def dark_theme(self) -> None:
        if not self.dark:
            try:
                self.s.theme_use('awdark')
                self.configure(bg='#2f2f2f')
                if self.i_pl is not None:
                    self.dark = True
                    self.create_internal_graph()
                    self.create_internal_graph()
                self.dark = True
            except Exception as e:
                tk.messagebox.showerror('Error', f'Cannot apply theme\n{e}')
        else:
            self.default_theme()

    
    def default_theme(self) -> None:
        self.configure(bg='#F0F0F0')
        self.s.theme_use('default')
        if self.i_pl is not None:
                self.dark = False
                self.create_internal_graph()
                self.create_internal_graph()
        self.dark = False
        

    def on_close(self):
        try:
            self.tree.on_close()
        except Exception as e:
            print('bad')
        plot.plt.close()
        self.update()
        self.destroy()

