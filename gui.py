import sys, time, os
import tkinter as tk
from tkinter import ttk
import internal, plot, s_probe, tree
from threading import Thread

sys.path.append(".")

'''
wmi seems to update every 3 seconds
'''

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

        if os.path.exists('./res/battery.ico'):
            self.iconbitmap('./res/battery.ico')

        self.s = ttk.Style()
        try:
            self.tk.call('lappend', 'auto_path', 'res/awthemes-10.4.0')
            self.tk.call('package', 'require', 'awdark')
        except:
            #tk.messagebox.showerror('Error', f'Could not load themes\n{e}')
            pass
        
        s_probe.sProbe.init()

        # Placeholder for internal or external graph
        self.i_pl = None
        self.pl = None

        # creating tkinter window
        self.title('BatteryInfo')
        self.geometry('600x700')

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
        
        view_menu.add_checkbutton(label='Graph (Internal)', command=self.create_internal_graph)

        view_menu.add_cascade(label='Graph (external)', menu=graph)
        graph.add_command(label='Single', command=self.create_external_single)
        graph.add_command(label='Multiple', command=self.create_external_graph)
        
        ext.add_command(label='Win32_Battery', command=self.get_win32batt)
        ext.add_command(label='Win32_PortableBattery', command=self.get_portable)
        ext.add_command(label='Root\Wmi', command=self.get_rootwmi)

        file_menu.add_command(label='Exit', command=self.on_close)
        #theme_menu.add_command(label='Default', command=self.default_theme)
        theme_menu.add_checkbutton(label='Dark', command=self.dark_theme)
        self.config(menu=mb)

        
        self.tree = tree.Treev(self)

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
        self.pl = plot.Plot(1)
        self.pl.on_close()
        self.pl = None


    # takes about 8 seconds
    def get_rootwmi(self):
        if not self.rootwmi_on:
            self.rootwmi_on = True
            r = s_probe.sProbe.getRootWmi()
            self.tree.insert('', 'end', 'root/wmi', text='root/wmi', open=True)
            for i in r.classes:
                if "Battery" in i and "MS" not in i:
                    tmp = r.instances(i)
                    if len(tmp) > 0:
                        self.tree.insert('root/wmi', 'end', i, text=i, open=True)
                        for x in tmp[0].properties.keys():
                            self.tree.insert(i, 'end', str(i)+x, text=x, values=(getattr(tmp[0], x), ''))
        else:
            self.rootwmi_on = False
            self.tree.delete('root/wmi')


    def get_win32batt(self):
        if not self.win32bat_on:
            self.win32bat_on = True
            w = s_probe.sProbe.getWin32Bat()
            self.tree.insert('', 'end', 'Raw', text='win32_battery', open=True)
            for i in w.properties.keys():
                val = getattr(w, i)
                if val:
                    self.tree.insert('Raw', 'end', str('b' + i), text=i, values=(val, ''))
            self.tree.yview_moveto('1.0')
        else:
            self.win32bat_on = False
            self.tree.delete('Raw')


    def get_portable(self):
        if s_probe.sProbe.portable is not None:
            if not self.portable_on:
                self.portable_on = True
                self.tree.insert('', 'end', 'portable', text='Portable Battery', open=True)
                # Portable Battery (all static values)
                for i in s_probe.sProbe.portable.properties.keys():
                    val = getattr(s_probe.sProbe.portable, i)
                    # Not none values
                    if val:
                        if 'DesignVoltage' in i or 'DesignCapacity' in i:
                            val = str(int(val) / 1000)
                        self.tree.insert('portable', 'end', i, text=i, values=(val, ''))
                # Scroll to bottom
                self.tree.yview_moveto('1.0')
            else:
                self.portable_on = False
                self.tree.delete('portable')
        else:
            print('Portable does not exist')
            

    # Maybe put in thread
    def retree(self):
        # overwrites values in the treeview, use only dynamic values
        s_probe.sProbe.refresh()
        
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
        self.s.theme_use('vista')
        if self.i_pl is not None:
                self.dark = False
                self.create_internal_graph()
                self.create_internal_graph()
        self.dark = False
        

    def on_close(self):
        plot.plt.close()
        self.update()
        self.destroy()

