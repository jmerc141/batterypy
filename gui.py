import sys, time
import tkinter as tk
from tkinter import ttk
import probe, test
#from multiprocessing import Process
import threading


sys.path.append(".")

'''
wmi seems to update every 3 seconds
'''

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        s = ttk.Style()
        self.tk.call('lappend', 'auto_path', '..\\awthemes-10.4.0')
        try:
            self.tk.call('package', 'require', 'awdark')
            s.theme_use('awdark')
            self.configure(bg='#2f2f2f')
        except:
            print('default theme')

        # Probe object reference
        self.p = probe.Probe()
        # Create graph window
        #self.pl = test.Window(self)

        #self.proc = Process(target=App.retree)
        

        # creating tkinter window
        self.title('BatteryInfo')
        self.geometry('1300x700')

        # initialize tree view
        self.tree = ttk.Treeview(self, columns=('val', 'max'), height=30)
        self.tree.insert('', 'end', 'system', text='System Name', values=(self.p.win.systemname, ''), open=True)
        
        self.tree.insert('system', 0, 'name', text='Name', values=(self.p.win.name, ''))
        self.tree.insert('system', 'end', text='Status', values=(self.p.win.status, ''))
        self.tree.insert('system', 'end', 'chargepercent', text='Charge Percent',
                         values=(str(self.p.win.estimatedchargeremaining) + ' %', ''))

        if self.p.runtime is not None:
            self.tree.insert('system', 'end', 'timerem', text='Time Remaining',
                         values=(str(self.p.hours) + 'h ' + str(self.p.minutes) + 'm ', ''))

        if self.p.win.maxrechargetime is not None:
            self.tree.insert('system', 'end', 'maxchargetime', text='Max Recharge Time',
            values=(self.p.win.maxrechargetime,''))

        self.tree.insert('system', 'end', 'manufacturedate', text='Manufacture Date', values=(self.p.mdate, ''))

        self.tree.insert('system', 'end', 'power', text='Power', open=True)

        if self.p.charging:
            self.tree.insert('power', 'end', 'chargepower', text='Charge Power',
                             values=(str(self.p.chargerate) + ' W', ''))
            #self.tree.insert('timerem', 'end', 'rechargetime', text='Max Recharge Time',
            #                 values=(str(self.p.rehours) + 'h ' + str(self.p.remins) + 'm', ''))
            self.tree.insert('timerem', 'end', 'ttf', text='Time to Full Charge', values=(str(self.p.ttfhours) + 'h ' + str(self.p.ttfmins) + 'm', ''))
        else:   #discharging
            self.tree.insert('power', 'end', 'dpower', text='Discharge Power',
                         values=(str(self.p.dischargerate) + ' W', ''))

        self.tree.insert('power', 'end', 'amps', text='Amperage', values=(str(self.p.amps) + ' A', ''))

        self.tree.insert('system', 'end', 'v', text='Voltage', open=True)
        self.tree.insert('v', 'end', 'voltnow', text='Voltage', values=(str(self.p.voltage) + ' V', ''))
        self.tree.insert('v', 'end', 'desvolt', text='Design Voltage',
                         values=(str(int(self.p.win.designvoltage) / 1000) + ' V', ''))

        self.tree.insert('system', 'end', 'capacity', text='Capacity', open=True)
        self.tree.insert('capacity', 'end', 'descap', text='Design Capacity', values=(str(self.p.descap) + ' Wh', ''))
        self.tree.insert('capacity', 'end', 'fullcap', text='Full Charge Capacity',
                         values=(str(self.p.fullcap) + ' Wh', ''))
        self.tree.insert('capacity', 'end', 'bathealth', text='Battery Health',
                         values=(str(round(self.p.bathealth, 3)) + ' %', ''))
        self.tree.insert('capacity', 'end', 'capleft', text='Remaining Capacity', values=(str(self.p.remcap) + ' Wh', ''))

        # extra info
        self.tree.insert('system', 'end', 'info', text='Extra Info', open=True)
        self.tree.insert('info', 'end', text='Cycle Count', values=(self.p.cyclecount, ''))
        self.tree.insert('info', 'end', text='Temperature', values=(self.p.temp, ''))
        self.tree.insert('info', 'end', 'cap', text='Caption', values=(self.p.win.caption, ''))
        self.tree.insert('info', 'end', 'desc', text='Description', values=(self.p.win.description, ''))
        self.tree.insert('info', 'end', 'avail', text='Availability', values=(self.p.avail, ''))
        self.tree.insert('info', 'end', 'batstat', text='Battery Status', values=(str(self.p.batstat)+' ('+str(self.p.ogbatstat)+')', ''))
        self.tree.insert('info', 'end', 'chem', text='Chemistry', values=(str(self.p.chem)+' ('+str(self.p.ogchem)+')', ''))

        if self.p.win.ErrorDescription is not None:
            self.tree.insert('info', 'end', text='Error Description', values=(self.p.win.ErrorDescription, ''))

        if self.p.pms:
            # Set to True
            self.tree.insert('info', 'end', text='Power Mgmt Capabilities', values=(self.p.pmc, ''))

        self.tree.insert('info', 'end', text='Low Alarm', values=(str(self.p.lowalarm) + ' Wh',''))
        self.tree.insert('info', 'end', text='Critical Alarm', values=(str(self.p.critalarm) + ' Wh', ''))
        self.tree.insert('info', 'end', text='Critical Bias', values=(str(self.p.critbi) + '', ''))
        
        self.get_portable()

        # win32_battery
        self.tree.insert('', 'end', 'Raw', text='win32_battery', open=False)
        
        for i in self.p.win.properties.keys():
            val = getattr(self.p.win, i)
            if val:
                self.tree.insert('Raw', 'end', str('b' + i), text=i, values=(val, ''))

        #self.get_rootwmi()

        # column headings
        self.tree.heading('#0', text='Property', anchor=tk.CENTER)
        self.tree.column('#0', width=200, stretch=tk.YES)
        self.tree.heading('0', text='Value')
        self.tree.column('0', width=200)
        self.tree.heading('1', text='Max')
        self.tree.column('1', width=150)

        # treeview stretches with window
        self.rowconfigure(0, weight=1)
        self.tree.bind('<<TreeviewSelect>>', self.item_selected)

        self.tree.grid(row=0, column=0, sticky='nsew', padx=(10,0), pady=(10,0))

        scrolly = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        scrollx = ttk.Scrollbar(self, orient=tk.HORIZONTAL, command=self.tree.xview)
        scrolly.grid(row=0, column=1, sticky='ns', pady=(10,0))
        scrollx.grid(row=1, column=0, sticky='ew', padx=(10,0), pady=(0,10))

        self.tree.configure(yscroll=scrolly.set)

        btn = ttk.Button(self, text='Start', command=self.retree)
        btn.grid(row=1, column=1, sticky='s')

        s1 = ttk.Scale(self, from_=0, to=12, orient=tk.HORIZONTAL, length=200)
        #s1.pack()

        #self.pb = ttk.Progressbar(self, orient='horizontal', mode='determinate', length=200)
        #self.pb.pack(side=tk.BOTTOM)
        
        #self.pl.init_window()

        # initialize max var, and initialize column
        self.maxv = self.p.voltage
        self.maxdis = self.p.dischargerate
        self.maxcharge = self.p.chargerate
        self.maxamps = self.p.amps

        if self.p.charging:
            pass
            #self.tree.set('charge', 'max', str(self.maxcharge) + ' W')
        else:
            self.tree.set('dpower', 'max', str(self.maxdis) + ' W')
        self.tree.set('voltnow', 'max', str(self.maxv) + ' V')
        self.tree.set('amps', 'max', str(self.maxamps) + ' A')

        self.retree()


    # takes about 8 seconds
    def get_rootwmi(self):
        self.tree.insert('', 'end', 'root/wmi', text='root/wmi', open=False)
        # root/wmi
        for i in self.p.rootwmi.classes:
            if "Battery" in i and "MS" not in i:
                tmp = self.p.rootwmi.instances(i)
                if len(tmp) > 0:
                    self.tree.insert('root/wmi', 'end', i, text=i, open=True)
                    for x in tmp[0].properties.keys():
                        self.tree.insert(i, 'end', str(i)+x, text=x, values=(getattr(tmp[0], x), ''))


    def get_portable(self):
        self.tree.insert('', 'end', 'portable', text='Portable Battery', open=False)
        # Portable Battery (all static values)
        for i in self.p.portable.properties.keys():
            val = getattr(self.p.portable, i)
            # Not none values
            if val:
                if 'DesignVoltage' in i or 'DesignCapacity' in i:
                    val = str(int(val) / 1000)
                self.tree.insert('portable', 'end', i, text=i, values=(val, ''))


    def retree(self):
        #self.pl.Clear()
        #self.pb['value'] += 10

        # overwrites values in the treeview, use only dynamic values
        print('retree')
        self.p.refresh()  # refreshes instance and updates variables
        if self.p.charging:
            self.tree.set('chargepower', 'val', str(self.p.chargerate) + ' W')
            if self.p.chargerate > self.maxcharge:
                self.maxcharge = self.p.chargerate
                self.tree.set('chargepower', 'max', str(self.maxcharge) + ' W')
        else:
            self.tree.set('dpower', 'val', str(self.p.dischargerate) + ' W')
            if self.p.dischargerate > self.maxdis:
                self.maxdis = self.p.dischargerate
                self.tree.set('dpower', 'maxdis', str(self.maxdis) + ' W')

        if self.p.runtime is not None:
            self.tree.set('timerem', 'val', str(str(self.p.hours) + 'h ' + str(self.p.minutes) + 'm'))

        self.tree.set('batstat', 'val', str(self.p.batstat)+' ('+str(self.p.ogbatstat)+')')
        self.tree.set('voltnow', 'val', str(self.p.voltage) + ' V')
        self.tree.set('avail', 'val', str(self.p.avail) + ' (' + str(self.p.ogavail)+')')
        self.tree.set('amps', 'val', str(self.p.amps) + ' A')

        # Max values column
        if self.p.voltage > self.maxv:
            self.maxv = self.p.voltage
            self.tree.set('voltnow', 'max', str(self.maxv) + ' V')
        if self.p.amps > self.maxamps:
            self.maxamps = self.p.amps
            self.tree.set('amps', 'max', str(self.maxamps) + ' A')
        
        if self.p.charging:
            self.tree.set('chargepower', 'val', str(self.p.chargerate) + ' W')
            self.tree.set('ttf', 'val', str(str(self.p.ttfhours) + 'h ' + str(self.p.ttfmins) + 'm'))
            if self.p.maxre is not None:
                self.tree.set('rechargetime', 'val', str(str(self.p.rehours) + 'h ' + str(self.p.remins) + 'm'))

        # doubt this changs often
        self.tree.set('fullcap', 'val', str(self.p.fullcap) + ' Wh')
        self.tree.set('chargepercent', 'val', str(self.p.win.estimatedchargeremaining) + ' %')
        self.p.refresh_voltage()
        self.after(1000, self.retree)


    def item_selected(self, event):
        self.item = self.tree.item(self.tree.selection()[0])['text']
        # Everything that can be graphed
        if 'Voltage' == self.item:
            #self.pl.set_prop(self.p.voltage)
            self.pl.set_prop(self.item)
        if 'Amperage' == self.item:
            self.pl.set_prop(self.item)
        if 'Discharge Power' == self.item:
            self.pl.set_prop(self.item)
        if 'Charge Power' == self.item:
            self.pl.set_prop(self.item)
        
'''
if __name__ == '__main__':
    app = App()
    app.mainloop()
'''