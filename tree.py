from tkinter import ttk
import s_probe

'''
    Wrapper class for treeview
    windows implementation
'''
class Treev(ttk.Frame):

    def __init__(self, master = None):
        self.master = master
        self.tree = ttk.Treeview(self.master, columns=('val', 'max'), height=10, padding=5)
        try:
            # initiate sProbe static class, decide windows or linux and import
            s_probe.sProbe()
        except TypeError as e:
            raise TypeError(e)
        
        self.win32bat_on = False
        self.rootwmi_on = False
        self.portable_on = False
        
        self.init_windows()
        

    '''
        Create entries in treeview
    '''
    def init_windows(self):
        #self.tree.tag_configure(font=['FiraMono Nerd Font Mono', 12, 'normal'])
        dc_Ah = round((s_probe.sProbe.designedCapacity / s_probe.sProbe.voltage) / 1000, 3)
        dv = int(s_probe.sProbe.win32bat['DesignVoltage']) / 1000
        fc = int(s_probe.sProbe.msbatt['BatteryFullChargedCapacity']['FullChargedCapacity']) / 1000
        full_ah = '{:.3f}'.format((fc / s_probe.sProbe.voltage))
        rc = s_probe.sProbe.msbatt['BatteryStatus']['RemainingCapacity']
        
        self.tree.insert('', 'end', 'manu', text='Manufacturer', values=(s_probe.sProbe.msbatt['BatteryStaticData']['ManufactureName'], ''))
        
        self.tree.insert('', 'end', 'name', text='Name', values=(s_probe.sProbe.msbatt['BatteryStatus']['Name'] or s_probe.sProbe.win32bat['Name'], ''))
        
        self.tree.insert('', 'end', 'chargepercent', text='Charge Percent',
                        values=(f'{s_probe.sProbe.win32bat['EstimatedChargeRemaining']} %', ''))
        

        # This section should be dedicated to properties that aren't likely to exist but should be shown if they do

        # Randomly, sProbe has no attribute hours???
        if s_probe.sProbe.msbatt['BatteryRuntime']['EstimatedRuntime'] or s_probe.sProbe.win32bat['EstimatedRunTime']:
            self.tree.insert('', 'end', 'timerem', text='Time Remaining',
                values=(f'{s_probe.sProbe.hours} h {s_probe.sProbe.minutes} m', ''))
            
        # Time in minutes to recharge a fully depleted battery
        if s_probe.sProbe.win32bat['MaxRechargeTime']:
            self.tree.insert('', 'end', 'maxchargetime', text='Max Recharge Time',
                values=(s_probe.sProbe.win32bat['MaxRechargeTime'],''))
            
        # win32bat['BatteryRechargeTime'] and win32bat['ExpectedBatteryLife'] are obsolete
            
        # Time in minutes to depletion of a fully charged battery
        if s_probe.sProbe.win32bat['ExpectedLife']:
            self.tree.insert('', 'end', 'expectedlife', text='Time to Empty (Full)',
                values=(s_probe.sProbe.win32bat['ExpectedLife'],''))
            
        # TimeOnBattery does not apply: indicates the elapsed time in seconds since the computer system's UPS last switched to battery power,
        # or the time since the system or UPS was last restarted, whichever is less

        if s_probe.sProbe.win32bat['TimeToFullCharge']:
            self.tree.insert('', 'end', 'ttf', text='Time to Full',
                values=(s_probe.sProbe.win32bat['TimeToFullCharge'],''))

        # Power section
        self.tree.insert('', 'end', 'power', text='', open=True)
        #self.tree.insert('', 'end', 'v', text='Voltage', open=True)

        self.tree.insert('power', 'end', 'desvolt', text='Design Voltage', values=(f'{dv} V', ''))

        self.tree.insert('power', 'end', 'voltnow', text='Voltage', values=(f'{s_probe.sProbe.voltage / 1000} V', ''))
        
        self.tree.insert('power', 'end', 'amps', text='Amps', values=(f'{s_probe.sProbe.amps} A', ''))
        
        self.tree.insert('power', 'end', 'wattage', text='Watts')

        self.tree.insert('', 'end', 'capacity', text='Capacity', open=True)
        
        self.tree.insert('capacity', 'end', 'descap', text='Design Capacity', values=(f'{s_probe.sProbe.designedCapacity / 1000:.3f} Wh ({dc_Ah:.3f} Ah)', ''))
        
        self.tree.insert('capacity', 'end', 'fullcap', text='Full Charge Capacity', values=(f'{fc} Wh ({full_ah} Ah)', ''))
        
        self.tree.insert('capacity', 'end', 'bathealth', text='Battery Health',
                         values=(f'{round(s_probe.sProbe.get_health(), 3)} %', ''))
        
        self.tree.insert('capacity', 'end', 'capleft', text='Remaining Capacity', values=(f'{rc} Wh', ''))

        #self.tree.insert('', 'end', 'info', text='Extra Info', open=False)
        
        self.tree.insert('', 'end', 'batstat', text='Battery Status', values=(f'{s_probe.sProbe.win32bat['Status']} ({s_probe.sProbe.getStatus()})', ''))
        
        self.tree.insert('', 'end', 'avail', text='Availability', values=(s_probe.sProbe.win32bat['Availability'], ''))

        # win32 chemistry seems to be the accurate one
        c1 = s_probe.sProbe.getchemstr(s_probe.sProbe.msbatt['BatteryStaticData']['Chemistry'])
        c2 = s_probe.sProbe.getchemstr(s_probe.sProbe.win32bat['Chemistry'])
        self.tree.insert('', 'end', 'chem', text='Chemistry', values=(f'{s_probe.sProbe.win32bat['Chemistry']} ({c2})', ''))

        self.tree.insert('', 'end', text='Cycle Count', values=(s_probe.sProbe.msbatt['BatteryCycleCount']['CycleCount'], ''))

        self.tree.insert('', 'end', text='Low Alarm', values=(f'{s_probe.sProbe.msbatt['BatteryStaticData']['DefaultAlert2'] / 1000} Wh',''))

        self.tree.insert('', 'end', text='Critical Alarm', values=(f'{s_probe.sProbe.msbatt['BatteryStaticData']['DefaultAlert1']} Wh', ''))

        # Specify the amount, in milliwatt-hours, of any small reserved charge that remains when the critical battery level shows zero. 
        # Miniclass drivers should subtract this value from the battery's FullChargedCapacity and remaining capacity, which is reported in BATTERY_STATUS, before reporting those values.
        self.tree.insert('', 'end', text='Critical Bias', values=(f'{s_probe.sProbe.msbatt['BatteryStaticData']['CriticalBias']} mWh', ''))

        self.tree.insert('', 'end', text='Caption', values=(s_probe.sProbe.win32bat['Caption'], ''))



        
        # initialize max var, and initialize column
        self.maxv = s_probe.sProbe.voltage
        self.maxamps = s_probe.sProbe.amps

        if s_probe.sProbe.msbatt['BatteryStatus']['Charging']:
            self.maxdis = 0
            self.maxcharge = s_probe.sProbe.chargerate
            self.tree.set('wattage', 'max', str(self.maxcharge) + ' W')
        else:
            self.maxcharge = 0
            self.maxdis = s_probe.sProbe.dischargerate
            self.tree.set('wattage', 'max', str(self.maxdis) + ' W')
        
        self.tree.set('voltnow', 'max', str(self.maxv) + ' V')
        self.tree.set('amps', 'max', str(self.maxamps) + ' A')
        
        # column headings
        self.tree.heading('#0', text='Property')
        self.tree.column('#0', minwidth=10, stretch=True)
        self.tree.heading('0', text='Value')
        self.tree.column('0', minwidth=10, stretch=True)
        self.tree.heading('1', text='Max')
        self.tree.column('1', width=80, minwidth=10, stretch=True)

        #self.tree.bind('<<TreeviewSelect>>', self.item_selected)

        return self.tree


    '''
        Called from gui, sets values in treeview
    '''
    def re_tree(self):
        rem_Wh = '{:.3f}'.format(s_probe.sProbe.msbatt['BatteryStatus']['RemainingCapacity'] / 1000)
        rem_ah = '{:.3f}'.format((s_probe.sProbe.msbatt['BatteryStatus']['RemainingCapacity'] / s_probe.sProbe.voltage) / 1000, 3)
        #full_ah = '{:.3f}'.format((s_probe.sProbe.msbatt['BatteryFullChargedCapacity']['FullChargedCapacity'] / s_probe.sProbe.voltage) / 1000)

        if s_probe.sProbe.msbatt['BatteryStatus']['Charging']:
            self.tree.item('power', text=f'Charging Power 🔌')
            self.tree.set('wattage', 'val', f'{s_probe.sProbe.chargerate:.3f} W')
            
            #if s_probe.sProbe.ttf is not None:
            #    self.tree.set('ttf', 'val', str(str(s_probe.sProbe.ttfhours) + 'h ' + str(s_probe.sProbe.ttfmins) + 'm'))
            
            if s_probe.sProbe.chargerate > self.maxcharge:
                self.maxcharge = s_probe.sProbe.chargerate
                self.tree.set('wattage', 'max', f'{self.maxcharge:.3f} W')
            
            #if s_probe.sProbe.maxrechargetime:
            #    self.tree.set('rechargetime', 'val', str(str(s_probe.sProbe.rehours) + 'h ' + str(s_probe.sProbe.remins) + 'm'))

        else:
            self.tree.item('power', text=f'Discharge Power ⚡')
            self.tree.set('wattage', 'val', f'{s_probe.sProbe.dischargerate:.3f} W')
            
            if s_probe.sProbe.dischargerate > self.maxdis:
                self.maxdis = s_probe.sProbe.dischargerate
                self.tree.set('wattage', 'max', f'{self.maxdis:.3f} W')
        
        self.tree.set('timerem', 'val', f'{s_probe.sProbe.hours} h {s_probe.sProbe.minutes} m')
        
        # Status changes when plugging in / unplugging
        self.tree.set('batstat', 'val', f'{s_probe.sProbe.win32bat['Status']} ({s_probe.sProbe.getStatus()})')
        
        self.tree.set('voltnow', 'val', f'{s_probe.sProbe.voltage:.3f} V')
        
        self.tree.set('avail', 'val', f'{s_probe.sProbe.win32bat['Availability']} ({s_probe.sProbe.getAvail()})')
        
        self.tree.set('amps', 'val', f'{s_probe.sProbe.amps:.3f} A')

        # Max values column
        if s_probe.sProbe.voltage > self.maxv:
            self.maxv = s_probe.sProbe.voltage
            self.tree.set('voltnow', 'max', str(self.maxv) + ' V')
        if s_probe.sProbe.amps > self.maxamps:
            self.maxamps = s_probe.sProbe.amps
            self.tree.set('amps', 'max', str(self.maxamps) + ' A')
        
        self.tree.set('capleft', 'val', str(rem_Wh) + ' Wh (' + rem_ah + ' Ah)')

        # doubt this changs often
        #self.tree.set('fullcap', 'val', str(s_probe.sProbe.msbatt['BatteryFullChargedCapacity']['FullChargedCapacity'] / 1000) + ' Wh (' + full_ah + ' Ah)')
        
        self.tree.set('chargepercent', 'val', str(s_probe.sProbe.win32bat['EstimatedChargeRemaining']) + '%')


    '''
        Toggles root/wmi entries in treeview
        takes about 8 seconds
    '''
    def get_rootwmi(self):
        if not self.rootwmi_on:
            self.rootwmi_on = True
            r = s_probe.sProbe.getRootWmi()
            #print(r)
            self.tree.insert('', 'end', 'root/wmi', text='root/wmi', open=True)
            r = s_probe.sProbe.rwmi
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

    '''
        Toggles win32battery entries in treeview
    '''
    def get_win32batt(self):
        if not self.win32bat_on:
            self.win32bat_on = True
            w = s_probe.sProbe.getw32bat_inst()
            self.tree.insert('', 'end', 'Raw', text='win32_battery', open=True)
            for i in w.properties.keys():
                val = getattr(w, i)
                if val:
                    self.tree.insert('Raw', 'end', str('b' + i), text=i, values=(val, ''))
            self.tree.yview_moveto('1.0')
        else:
            self.win32bat_on = False
            self.tree.delete('Raw')

    '''
        Toggles portable_battery entries in treeview
    '''
    def get_portable(self):
        if not self.portable_on:
            self.portable_on = True
            self.tree.insert('', 'end', 'portable', text='Portable Battery', open=True)
            # Portable Battery (all static values)
            p = s_probe.sProbe.get_portable()
            for i in p.properties.keys():
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


    def on_close(self):
        s_probe.sProbe.on_close()

