import tkinter as tk
from tkinter import ttk
import s_probe

class Treev(ttk.Treeview):

    def __init__(self, master = None):
        self.master = master
        self.tree = ttk.Treeview(master, columns=('val', 'max'), height=30, padding=[2,2])
        self.init()
        

    def init(self):
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

        # column headings
        self.tree.heading('#0', text='Property', anchor=tk.CENTER)
        self.tree.column('#0', width=200, stretch=tk.YES)
        self.tree.heading('0', text='Value')
        self.tree.column('0', width=200)
        self.tree.heading('1', text='Max')
        self.tree.column('1', width=150)

        self.tree.grid(row=0, column=0, sticky='nsew', padx=(10,0), pady=(10,2))

        scrolly = ttk.Scrollbar(self.master, orient=tk.VERTICAL, command=self.tree.yview)
        scrollx = ttk.Scrollbar(self.master, orient=tk.HORIZONTAL, command=self.tree.xview)
        scrolly.grid(row=0, column=1, sticky='ns', pady=(10,0))
        #scrollx.grid(row=1, column=0, sticky='ew', padx=(10,0), pady=(0,10))

        self.tree.configure(yscroll=scrolly.set)


        #self.tree.bind('<<TreeviewSelect>>', self.item_selected)
        return self.tree
    

    #def insert(self):
    #    self.t.insert()


    def re_tree(self):
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
            #self.tree.set('dpower', 'val', str(s_probe.sProbe.dischargerate) + ' W')
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