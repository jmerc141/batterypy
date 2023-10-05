import tkinter as tk
from tkinter import ttk
import s_probe_l

class Treev(ttk.Treeview):

    def __init__(self, master = None):
        self.master = master
        self.tree = ttk.Treeview(master, columns=('val', 'max'), height=30, padding=[2,2])
        try:
            s_probe_l.sProbe()
        except TypeError as e:
            raise TypeError(e)
        
        self.init()
        

    def init(self):
        #self.tree.tag_configure(font=['FiraMono Nerd Font Mono', 12, 'normal'])
        self.tree.insert('', 'end', 'system', text='System Name', values=(s_probe_l.sProbe.props['sysname'], ''), open=True)
        
        self.tree.insert('system', 0, 'name', text='Name', values=(s_probe_l.sProbe.props['model_name'], ''))
        self.tree.insert('system', 'end', 'batstat', text='Status', values=(s_probe_l.sProbe.props['status'], ''))
        self.tree.insert('system', 'end', 'chargepercent', text='Charge Percent',
                         values=(str(s_probe_l.sProbe.props['capacity']) + ' %', ''))
   
        self.tree.insert('system', 'end', 'manufacture_date', text='Manufacture Date', values=(s_probe_l.sProbe.calculated_props['manufacture_date'], ''))

        self.tree.insert('system', 'end', 'bathealth', text='Battery Health',
                        values=(s_probe_l.sProbe.check_prop('health'), ''))
        
        self.tree.insert('system', 'end', 'time', text='Time Remaining', values=(s_probe_l.sProbe.calculated_props['timerem'], ''))
        self.tree.insert('system', 'end', 'cycle', text='Cycle Count', values=(s_probe_l.sProbe.props['cycle_count'], ''))

        # initialize max var, and initialize column
        self.maxv = int(s_probe_l.sProbe.props['voltage_now']) / 1000000
        self.maxdis = int(s_probe_l.sProbe.calculated_props['watts']) / 1000000
        self.maxamps = int(s_probe_l.sProbe.calculated_props['amps']) / 1000000
        self.maxcharge = int(s_probe_l.sProbe.calculated_props['watts']) / 1000000
        

        # Check "maxrechargetime", ""
        if s_probe_l.sProbe.props['status'] == 'Charging':
            self.tree.insert('system', 'end', 'power', text=str('Power' + '🔌'), open=True)
            self.tree.insert('power', 'end', 'chargepower', text='Charge Power',
                             values=(str(s_probe_l.sProbe.calculated_props['watts']) + ' W', ''))
            # no need to check, only initializing max column
            self.tree.set('chargepower', 'max', self.maxcharge + ' W')
            if 'time_to_full' in s_probe_l.sProbe.props:
                self.tree.insert('timerem', 'end', 'ttf', text='Time to Full Charge',
                             values=(str(s_probe_l.sProbe.ttf / 60) + 'h ' + str(s_probe_l.sProbe.ttf % 60) + 'm', ''))
        elif s_probe_l.sProbe.props['status'] == 'Discharging':   #discharging
            if 'timrem' in s_probe_l.sProbe.props:
                self.tree.insert('system', 'end', 'timerem', text='Time Remaining',
                    values=(str(s_probe_l.sProbe.hours) + 'h ' + str(s_probe_l.sProbe.minutes) + 'm ', ''))
            self.tree.insert('system', 'end', 'power', text=str('Power' + ' ⚡'), open=True)
            self.tree.insert('power', 'end', 'dpower', text='Discharge Power',
                         values=(str(int(s_probe_l.sProbe.props['watts']) / 1000000) + ' W', ''))
            self.tree.set('dpower', 'max', str(self.maxdis) + ' W')
        else:   #Uknown status
            self.tree.insert('system', 'end', 'power', text="Power Unknown", open=True)
            self.tree.insert('power', 'end', 'dpower', text="Watts", values=s_probe_l.sProbe.props['power_now'])

        self.tree.insert('power', 'end', 'amps', text='Amperage', values=(str(s_probe_l.sProbe.calculated_props['amps']) + ' A', ''))

        self.tree.insert('system', 'end', 'v', text='Voltage', open=True)
        self.tree.insert('v', 'end', 'voltnow', text='Voltage', values=(str(int(s_probe_l.sProbe.props['voltage_now']) / 100000) + ' V', ''))
        self.tree.insert('v', 'end', 'desvolt', text='Min Design Voltage',
                         values=(str(int(s_probe_l.sProbe.props['voltage_min_design']) / 1000000) + ' V', ''))
        self.tree.set('voltnow', 'max', str(self.maxv) + ' V')
        self.tree.set('amps', 'max', str(self.maxamps) + ' A')
        
        self.tree.insert('system', 'end', 'cap', text='Capacity', open=True)
        if s_probe_l.sProbe.props['energy_now'] != '':
            deg = round((int(s_probe_l.sProbe.props['energy_full']) /
                                        int(s_probe_l.sProbe.props['energy_full_design'])) * 100, 3)
            self.tree.insert('cap', 'end', 'descap', text='Design Capacity',
                            values=(str(int(s_probe_l.sProbe.props['energy_full_design']) / 1000000) + ' Wh (' 
                                    + str(s_probe_l.sProbe.calculated_props['ah_full_design']) + ' Ah)', ''))
            self.tree.insert('cap', 'end', 'fullcap', text='Full Charge Capacity',
                            values=(str(int(s_probe_l.sProbe.props['energy_full']) / 1000000) + ' Wh ('
                                    + str(s_probe_l.sProbe.calculated_props['ah_full']) + ' Ah)', ''))
            self.tree.insert('cap', 'end', 'degradation', text='Degradation %',
                            values=(str(deg) + ' %', ''))
            self.tree.insert('cap', 'end', 'capleft', text='Remaining Capacity',
                            values=(str(int(s_probe_l.sProbe.props['energy_now']) / 1000000) + ' Wh ('
                                    + str(s_probe_l.sProbe.calculated_props['ah_now']) + ' Ah)', ''))
        elif s_probe_l.sProbe.props['charge_now'] != '':
            # add wh equivalent
            deg = round((int(s_probe_l.sProbe.props['charge_full']) /
                                        int(s_probe_l.sProbe.props['charge_full_design'])) * 100, 3)
            self.tree.insert('cap', 'end', 'descap', text='Design Capacity',
                            values=(str(int(s_probe_l.sProbe.props['charge_full_design']) / 1000000) + ' Ah ('
                                + str(s_probe_l.sProbe.calculated_props['wh_full_design']) + ' Wh)', ''))
            self.tree.insert('cap', 'end', 'fullcap', text='Full Charge Capacity',
                            values=(str(int(s_probe_l.sProbe.props['charge_full']) / 1000000) + ' Ah', ''))
            self.tree.insert('cap', 'end', 'capleft', text='Remaining Capacity',
                            values=(str(int(s_probe_l.sProbe.props['charge_now']) / 1000000) + ' Ah)', ''))
            self.tree.insert('cap', 'end', 'degradation', text='Degradation %',
                            values=(str(round(int(s_probe_l.sProbe.props['charge_full']) /
                                        int(s_probe_l.sProbe.props['charge_full_design']), 3) ) + ' %', ''))

        # extra info
        self.tree.insert('system', 'end', 'info', text='Extra Info', open=True)
        if s_probe_l.sProbe.props['technology'] is not None:
            self.tree.insert('info', 'end', 'chem', text='Chemistry', values=(str(s_probe_l.sProbe.props['technology']), ''))

        self.tree.insert('info', 'end', text='Min Alert', values=(s_probe_l.sProbe.check_prop('capacity_alert_min') + ' %',''))
        self.tree.insert('info', 'end', text='Max Alarm', values=(s_probe_l.sProbe.check_prop('capacity_alert_max') + ' %', ''))

        self.tree.insert('system', 'end', 'all', text="All", open=True)

        # all properties
        for i in s_probe_l.sProbe.props:
            try:
                self.tree.insert('all', 'end', i, text=i, values=(s_probe_l.sProbe.props[i], ''))
            except Exception as e:
                print(e)
            '''
            if i == 'uevent':
                self.tree.insert('all', 'end', i, text=i, open=True)
                for j in s_probe_l.sProbe.props['uevent']:
                    self.tree.insert('uevent', 'end', j, text=j, values=(s_probe_l.sProbe.props['uevent'][j], ''))
            else:
                try:
                    self.tree.insert('all', 'end', i, text=i, values=(s_probe_l.sProbe.props[i], ''))
                except Exception as e:
                    pass
            '''

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


    def re_tree(self):
        v = int(s_probe_l.sProbe.props['voltage_now']) / 1000000
        w = int(s_probe_l.sProbe.calculated_props['watts']) / 1000000

        if s_probe_l.sProbe.props['status'] == 'Charging':
            # CHARGING
            self.tree.set('chargepower', 'val', str(w) + ' W')
            if 'time_to_full' in s_probe_l.sProbe.props:  # fix this
                self.tree.set('ttf', 'val', str(str(s_probe_l.sProbe.ttfhours) + 'h ' + str(s_probe_l.sProbe.ttfmins) + 'm'))
            if w > self.maxcharge:
                self.maxcharge = w
                self.tree.set('chargepower', 'max', str(self.maxcharge) + ' W')
        else:
            # DISCHARGING
            self.tree.set('dpower', 'val', str(w) + ' W')
            if w > self.maxdis:
                self.maxdis = w
                self.tree.set('dpower', 'max', str(self.maxdis) + ' W')

        self.tree.set('batstat', 'val', str(s_probe_l.sProbe.props['status']))
        self.tree.set('voltnow', 'val', str(v) + ' V')
        self.tree.set('amps', 'val', str(round(s_probe_l.sProbe.calculated_props['amps'] / 1000000, 3)) + ' A')

        # Max values column
        if v > self.maxv:
            self.maxv = int(s_probe_l.sProbe.props['voltage_now'])
            self.tree.set('voltnow', 'max', str(self.maxv) + ' V')
        if v > self.maxamps:
            self.maxamps = s_probe_l.sProbe.calculated_props['amps']
            self.tree.set('amps', 'max', str(self.maxamps) + ' A')

        if s_probe_l.sProbe.wh:
            en = str(int(s_probe_l.sProbe.props['energy_now']) / 1000000)
            ef = str(int(s_probe_l.sProbe.props['energy_full']) / 1000000)
            self.tree.set('capleft', 'val', en + ' Wh ('
                                    + str(s_probe_l.sProbe.calculated_props['ah_now']) + ' Ah)')
            # doubt this changes often
            self.tree.set('fullcap', 'val', ef + ' Wh ('
                                    + str(s_probe_l.sProbe.calculated_props['ah_full']) + ' Ah)')
        else:
            cn = str(int(s_probe_l.sProbe.props['charge_now']) / 1000000)
            cf = str(int(s_probe_l.sProbe.props['charge_full']) / 1000000)
            self.tree.set('capleft', 'val', cn + ' Ah ('
                                    + str(s_probe_l.sProbe.props['wh_now']) + ' Wh)')
            # doubt this changes often
            self.tree.set('fullcap', 'val', cf + ' Ah ('
                                    + str(s_probe_l.sProbe.props['wh_full']) + ' Wh)')

        self.tree.set('chargepercent', 'val', str(s_probe_l.sProbe.props['capacity']) + ' %')


    def on_close(self):
        s_probe_l.sProbe.on_close()

