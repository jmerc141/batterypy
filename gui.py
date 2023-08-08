import sys, time, os
import tkinter as tk
from tkinter import ttk, messagebox, PanedWindow
import internal, plot, s_probe

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

        # Change directory to get icon resource
        try:
            os.chdir(sys._MEIPASS)
        except Exception:
            self.base_path = os.path.abspath(".")

        if os.path.exists('./res/battery.ico'):
            self.iconbitmap('./res/battery.ico')

        self.s = ttk.Style()
        
        s_probe.sProbe.init()

        # Probe object reference
        #self.p = probe.Probe()
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
        theme_menu.add_command(label='Default', command=self.default_theme)
        theme_menu.add_command(label='Dark', command=self.dark_theme)
        self.config(menu=mb)

        # Initialize tree view
        #pw = ttk.PanedWindow(self, orient='vertical')
        #f = ttk.Frame()

        self.tree = ttk.Treeview(self, columns=('val', 'max'), height=30, padding=[2,2])
        #pw.add(self.tree)
        #pw.grid(row=0, column=0, sticky='nesw')
        self.tree.insert('', 'end', 'system', text='System Name', values=(s_probe.sProbe.system_name, ''), open=True)
        
        self.tree.insert('system', 0, 'name', text='Name', values=(s_probe.sProbe.name, ''))
        self.tree.insert('system', 'end', text='Status', values=(s_probe.sProbe.status, ''))
        self.tree.insert('system', 'end', 'chargepercent', text='Charge Percent',
                         values=(str(s_probe.sProbe.est_chrg) + ' %', ''))

        if s_probe.sProbe.runtime != 'N/A':
            self.tree.insert('system', 'end', 'timerem', text='Time Remaining',
                values=(str(s_probe.sProbe.hours) + 'h ' + str(s_probe.sProbe.minutes) + 'm ', ''))

        if s_probe.sProbe.maxrechargetime is not None:
            self.tree.insert('system', 'end', 'maxchargetime', text='Max Recharge Time',
                values=(s_probe.sProbe.maxrechargetime,''))

        self.tree.insert('system', 'end', 'manufacturedate', text='Manufacture Date', values=(s_probe.sProbe.mdate, ''))

        self.tree.insert('system', 'end', 'deviceid', text='Device ID', values=(s_probe.sProbe.device_id, ''))

        self.tree.insert('system', 'end', 'power', text='Power', open=True)

        # Check "maxrechargetime", ""
        if s_probe.sProbe.charging:
            self.tree.insert('power', 'end', 'chargepower', text='Charge Power',
                             values=(str(s_probe.sProbe.chargerate) + ' W', ''))
            #self.tree.insert('timerem', 'end', 'rechargetime', text='Max Recharge Time',
            #                 values=(str(self.p.rehours) + 'h ' + str(self.p.remins) + 'm', ''))
            if s_probe.sProbe.ttf is not None:
                self.tree.insert('timerem', 'end', 'ttf', text='Time to Full Charge',
                             values=(str(s_probe.sProbe.ttf / 60) + 'h ' + str(s_probe.sProbe.ttf % 60) + 'm', ''))
        else:   #discharging
            self.tree.insert('power', 'end', 'dpower', text='Discharge Power',
                         values=(str(s_probe.sProbe.dischargerate) + ' W', ''))

        self.tree.insert('power', 'end', 'amps', text='Amperage', values=(str(s_probe.sProbe.amps) + ' A', ''))

        self.tree.insert('system', 'end', 'v', text='Voltage', open=True)
        self.tree.insert('v', 'end', 'voltnow', text='Voltage', values=(str(s_probe.sProbe.voltage) + ' V', ''))
        self.tree.insert('v', 'end', 'desvolt', text='Design Voltage',
                         values=(str(int(s_probe.sProbe.design_voltage) / 1000) + ' V', ''))

        self.tree.insert('system', 'end', 'capacity', text='Capacity', open=True)
        self.tree.insert('capacity', 'end', 'descap', text='Design Capacity', values=(str(s_probe.sProbe.descap / 1000) + ' Wh', ''))
        self.tree.insert('capacity', 'end', 'fullcap', text='Full Charge Capacity',
                         values=(str(s_probe.sProbe.full_cap / 1000) + ' Wh', ''))
        self.tree.insert('capacity', 'end', 'bathealth', text='Battery Health',
                         values=(str(round(s_probe.sProbe.bathealth, 2)) + ' %', ''))
        self.tree.insert('capacity', 'end', 'capleft', text='Remaining Capacity', values=(str(s_probe.sProbe.rem_cap) + ' Wh', ''))

        # extra info
        self.tree.insert('system', 'end', 'info', text='Extra Info', open=True)
        self.tree.insert('info', 'end', text='Cycle Count', values=(s_probe.sProbe.cycle_count, ''))
        self.tree.insert('info', 'end', text='Temperature', values=(s_probe.sProbe.temp, ''))
        self.tree.insert('info', 'end', 'cap', text='Caption', values=(s_probe.sProbe.caption, ''))
        self.tree.insert('info', 'end', 'desc', text='Description', values=(s_probe.sProbe.desc, ''))
        self.tree.insert('info', 'end', 'avail', text='Availability', values=(s_probe.sProbe.avail, ''))
        self.tree.insert('info', 'end', 'batstat', text='Battery Status', values=(str(s_probe.sProbe.bstatus)+' ('+str(s_probe.sProbe.stat_str)+')', ''))
        if s_probe.sProbe.ogchem is not None:
            self.tree.insert('info', 'end', 'chem', text='Chemistry', values=(str(s_probe.sProbe.ogchem)+' ('+str(s_probe.sProbe.chem_str)+')', ''))

        if s_probe.sProbe.err_desc is not None:
            self.tree.insert('info', 'end', text='Error Description', values=(s_probe.sProbe.err_desc, ''))

        if s_probe.sProbe.pmc:
            # Set to True
            self.tree.insert('info', 'end', text='Power Mgmt Capabilities', values=(s_probe.sProbe.pmc, ''))

        self.tree.insert('info', 'end', text='Low Alarm', values=(str(s_probe.sProbe.lowalarm) + ' Wh',''))
        self.tree.insert('info', 'end', text='Critical Alarm', values=(str(s_probe.sProbe.critalarm) + ' Wh', ''))
        self.tree.insert('info', 'end', text='Critical Bias', values=(str(s_probe.sProbe.critbi) + '', ''))

        # column headings
        self.tree.heading('#0', text='Property', anchor=tk.CENTER)
        self.tree.column('#0', width=200, stretch=tk.YES)
        self.tree.heading('0', text='Value')
        self.tree.column('0', width=200)
        self.tree.heading('1', text='Max')
        self.tree.column('1', width=150)

        # treeview stretches with window
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.tree.bind('<<TreeviewSelect>>', self.item_selected)

        self.tree.grid(row=0, column=0, sticky='nsew', padx=(10,0), pady=(10,2))

        scrolly = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        scrollx = ttk.Scrollbar(self, orient=tk.HORIZONTAL, command=self.tree.xview)
        scrolly.grid(row=0, column=1, sticky='ns', pady=(10,0))
        #scrollx.grid(row=1, column=0, sticky='ew', padx=(10,0), pady=(0,10))

        self.tree.configure(yscroll=scrolly.set)

        # initialize max var, and initialize column
        self.maxv = s_probe.sProbe.voltage
        self.maxdis = s_probe.sProbe.dischargerate
        self.maxcharge = s_probe.sProbe.chargerate
        self.maxamps = s_probe.sProbe.amps

        if s_probe.sProbe.charging:
            pass
            #self.tree.set('charge', 'max', str(self.maxcharge) + ' W')
            self.tree.set('chargepower', 'max', str(self.maxcharge) + ' W')
        else:
            self.tree.set('dpower', 'max', str(self.maxdis) + ' W')
        self.tree.set('voltnow', 'max', str(self.maxv) + ' V')
        self.tree.set('amps', 'max', str(self.maxamps) + ' A')

        self.retree()


    def create_internal_graph(self):
        self.internal = not self.internal
        if self.internal:
            #try:
            self.plf = ttk.Frame()
            self.i_pl = internal.Window(self.plf)
            self.plf.grid(column=2, row=0, sticky='w')
            self.geometry('1200x700')
            #except Exception as e:
            #    print('Can\'t create internal graph')
            #    print(sys.exc_info()[2])
        else:
            self.i_pl.destroy()
            self.plf.destroy()
            self.i_pl = None
            self.geometry('600x700')
            

    def create_external_graph(self):
        self.pl = plot.Plot(0)
        self.pl = None


    def create_external_single(self):
        self.pl = plot.Plot(1)
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
        #self.p.refresh()  # refreshes instance and updates variables
        s_probe.sProbe.refresh()
        #print(self.pl, self.i_pl)

        if s_probe.sProbe.charging:
            self.tree.set('chargepower', 'val', str(s_probe.sProbe.chargerate) + ' W')
            if s_probe.sProbe.ttf is not None:
                self.tree.set('ttf', 'val', str(str(s_probe.sProbe.ttfhours) + 'h ' + str(s_probe.sProbe.ttfmins) + 'm'))
            if s_probe.sProbe.chargerate > self.maxcharge:
                self.maxcharge = s_probe.sProbe.chargerate
                self.tree.set('chargepower', 'max', str(self.maxcharge) + ' W')
            if s_probe.sProbe.maxrechargetime is not None:
                self.tree.set('rechargetime', 'val', str(str(s_probe.sProbe.rehours) + 'h ' + str(s_probe.sProbe.remins) + 'm'))
        else:
            self.tree.set('dpower', 'val', str(s_probe.sProbe.dischargerate) + ' W')
            if s_probe.sProbe.dischargerate > self.maxdis:
                self.maxdis = s_probe.sProbe.dischargerate
                self.tree.set('dpower', 'max', str(self.maxdis) + ' W')
                self.tree.set('dpower', 'max', str(self.maxdis) + ' W')
        if s_probe.sProbe.runtime != 'N/A':
            self.tree.set('timerem', 'val', str(str(s_probe.sProbe.hours) + 'h ' + str(s_probe.sProbe.minutes) + 'm'))

        self.tree.set('batstat', 'val', str(str(s_probe.sProbe.bstatus) + ' ('+str(s_probe.sProbe.stat_str)+')'))
        self.tree.set('voltnow', 'val', str(s_probe.sProbe.voltage) + ' V')
        self.tree.set('avail', 'val', str(s_probe.sProbe.avail) + ' (' + str(s_probe.sProbe.avail_str)+')')
        self.tree.set('amps', 'val', str(s_probe.sProbe.amps) + ' A')

        # Max values column
        if s_probe.sProbe.voltage > self.maxv:
            self.maxv = s_probe.sProbe.voltage
            self.tree.set('voltnow', 'max', str(self.maxv) + ' V')
        if s_probe.sProbe.amps > self.maxamps:
            self.maxamps = s_probe.sProbe.amps
            self.tree.set('amps', 'max', str(self.maxamps) + ' A')
        
        self.tree.set('capleft', 'val', str(s_probe.sProbe.rem_cap / 1000) + ' Wh')

        # doubt this changs often
        self.tree.set('fullcap', 'val', str(s_probe.sProbe.full_cap / 1000) + ' Wh')
        self.tree.set('chargepercent', 'val', str(s_probe.sProbe.est_chrg) + ' %')
        self.after(1000, self.retree)


    def item_selected(self, event):
        self.item = self.tree.item(self.tree.selection()[0])['text']
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
        self.tk.call('lappend', 'auto_path', 'res/awthemes-10.4.0')
        try:
            self.tk.call('package', 'require', 'awdark')
            self.s.theme_use('awdark')
            self.configure(bg='#2f2f2f')
        except Exception as e:
            tk.messagebox.showerror('Error', f'Cannot apply theme\n{e}')

    
    def default_theme(self) -> None:
        self.configure(bg='#F0F0F0')
        self.s.theme_use('vista')
        

    def on_close(self):
        '''
        try:
            self.pl.close()
            #self.pl.proc.terminate()
        except:
            print('Unable to close graph')
            pass
        '''
        #self.pl.close()

        self.quit()

