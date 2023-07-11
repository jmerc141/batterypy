# probe.py

import wmi
#from thread_decorator import *


class Probe:

    def __init__(self):
        # get instance of win32battery, [0] for first entry

        # ROOT\CIMV2
        self.win = wmi.WMI().instances('win32_battery')[0]  # [0] is battery
        # might not exist
        if wmi.WMI().instances('win32_portablebattery'):
            self.portable = wmi.WMI().instances('win32_portablebattery')[0]
        # ROOT\WMI
        self.rootwmi = wmi.WMI(moniker="//./root/wmi")

        self.runtime = self.tryinstance(self, 'BatteryRunTime')
        
        self.fullcap = self.tryinstance(self, 'BatteryFullChargedCapacity')
        self.cyclecount = self.tryinstance(self, 'BatteryCycleCount')
        self.temp = self.tryinstance(self, 'BatteryTemperature')

        # later
        self.tagchange = self.rootwmi.ExecQuery('select * from BatteryTagChange')
        self.statchange = self.rootwmi.ExecQuery('selct * from BatteryStatusChange')

        status = self.tryinstance(self, 'BatteryStatus')
        self.chargerate = status.chargerate / 1000
        self.charging = status.charging
        self.critical = status.critical
        if status.dischargerate > 0:
            self.dischargerate = status.dischargerate / 1000
        else:
            self.dischargerate = 0
        self.discharging = status.discharging
        self.poweronline = status.poweronline
        self.remcap = status.remainingcapacity / 1000
        self.voltage = status.voltage / 1000
        self.cap2 = status.caption

        staticdata = self.rootwmi.ExecQuery('select * from BatteryStaticData')[0]
        self.capab = staticdata.capabilities
        self.ogchem = staticdata.chemistry
        self.critbi = staticdata.criticalbias
        self.critalarm = staticdata.defaultalert1 / 1000    #mwh
        self.lowalarm = staticdata.defaultalert2 / 1000
        self.descap = staticdata.designedcapacity / 1000
        self.mdate = staticdata.manufacturedate
        self.sn = staticdata.serialnumber
        self.g0 = float(staticdata.granularity0) / 100000000000
        self.g1 = float(staticdata.granularity1) / 10000000000000
        self.g2 = staticdata.granularity2
        self.g3 = staticdata.granularity3

        # calculated values
        self.ah = self.remcap / self.voltage
        self.amps = self.calcamps(self)
        self.bathealth = (self.fullcap / self.descap) * 100  # overall battery degradation %
        #self.capleft = self.fullcap * (self.estimatedchargeremaining)

        # require processing
        self.ogbatstat = self.win.batterystatus
        self.batstat = self.getStatus(self)
        self.ogavail = self.win.Availability
        self.avail = self.getAvail(self)
        self.chem = self.getchem(self)
        # look up codes
        self.pmc = self.win.powermanagementcapabilities
        self.pms = self.win.powermanagementsupported

        if self.win.maxrechargetime is None:
            self.maxre = None
        else:
            self.maxre = self.win.maxrechargetime
            self.rehours = self.maxre / 60
            self.remins = self.maxre % 60

        if self.win.timetofullcharge is None:
            self.ttf = 0
        else:
            self.ttf = self.win.timetofullcharge
        self.ttfhours = self.ttf / 60
        self.ttfmins = self.ttf % 60

        if self.win.timeonbattery is None:
            self.tob = 0
        else:
            self.tob = self.win.timeonbattery       # in seconds       


    def refresh_voltage(self):
        self.voltage = self.rootwmi.ExecQuery('select * from BatteryStatus')[0].voltage

    
    def refresh(self):
        # queries all wmi values and resets variables
        print('refreshed')
        self.win = wmi.WMI().instances('win32_battery')[0]

        if self.runtime is not None:
            self.runtime = \
                self.tryinstance(self, 'BatteryRunTime')
            self.hours = int(self.runtime / 60)
            self.minutes = int(self.runtime % 60)

        self.fullcap = \
            self.rootwmi.ExecQuery('select FullChargedCapacity from BatteryFullChargedCapacity where FullChargedCapacity > 0')[0].fullchargedcapacity / 1000
        req = self.rootwmi.ExecQuery('select * from BatteryCycleCount')[0]

        self.tryinstance(self, 'BatteryTemperature')
        self.tryinstance(self, 'BatteryCycleCount')

        # later
        #self.tagchange = self.rootwmi.ExecQuery('select * from BatteryTagChange')
        #self.statchange = self.rootwmi.ExecQuery('selct * from BatteryStatusChange')

        status = self.rootwmi.ExecQuery('select * from BatteryStatus')[0]
        self.chargerate = status.chargerate / 1000
        self.charging = status.charging
        self.critical = status.critical
        if status.dischargerate > 0:
            self.dischargerate = status.dischargerate / 1000
        else:
            self.dischargerate = 0
        self.discharging = status.discharging
        self.poweronline = status.poweronline
        self.remcap = status.remainingcapacity / 1000
        self.voltage = status.voltage / 1000

        # calculated values
        self.ah = self.remcap / self.voltage
        self.amps = self.calcamps(self)
        self.bathealth = (self.fullcap / self.descap) * 100  # percent

        # require processing
        self.batstat = self.getStatus(self)
        self.avail = self.getAvail(self)
        self.chem = self.getchem(self)
        #self.proc.join()


    @staticmethod
    def getStatus(self):
        statcode = self.win.batterystatus
        if statcode == 1:
            statcode = 'Other'
        elif statcode == 2:
            statcode = 'Unknown'
        elif statcode == 3:
            statcode = 'Fully Charged'
        elif statcode == 4:
            statcode = 'Low'
        elif statcode == 5:
            statcode = 'Critical'
        elif statcode == 6:
            statcode = 'Charging'
        elif statcode == 7:
            statcode = 'Charging and High'
        elif statcode == 8:
            statcode = 'Charging and Low'
        elif statcode == 9:
            statcode = 'Charging and Critical'
        elif statcode == 10:
            statcode = 'Undefined'
        elif statcode == 11:
            statcode = 'Partially Charged'
        return statcode


    @staticmethod
    def getAvail(self):
        # only call from refresh
        avail = self.win.Availability
        if avail == 1:
            avail = 'Other'
        elif avail == 2:
            avail = 'Unknown'
        elif avail == 3:
            avail = 'Running at full power'
        elif avail == 4:
            avail = 'Warning'
        elif avail == 5:
            avail = 'Test Mode'
        elif avail == 6:
            avail = 'N/A'
        elif avail == 7:
            avail = 'Power Off'
        elif avail == 8:
            avail = 'Off Line'
        elif avail == 9:
            avail = 'Off Duty'
        elif avail == 10:
            avail = 'Degraded'
        elif avail == 11:
            avail = 'Not Installed'
        elif avail == 12:
            avail = 'Install Error'
        elif avail == 13:
            avail = 'Power Save'
        elif avail == 14:
            avail = 'Power Save (Low Power Mode)'
        elif avail == 15:
            avail = 'Power Save (Standby)'
        elif avail == 16:
            avail = 'Power Cycle'
        elif avail == 17:
            avail = 'Power Save (Warning)'
        elif avail == 18:
            avail = 'Paused'
        elif avail == 19:
            avail = 'Not Ready'
        elif avail == 20:
            avail = 'Not Configured'
        elif avail == 21:
            avail = 'Quiesced'
        else:
            avail = 'Unknown'
        return avail


    @staticmethod
    def getchem(self):
        # only call from refresh
        if self.win.chemistry == 1:
            chem = 'Other'
        elif self.win.chemistry == 2:
            chem = 'Unknown'
        elif self.win.chemistry == 3:
            chem = 'Lead Acid'
        elif self.win.chemistry == 4:
            chem = 'Nickel Cadmium'
        elif self.win.chemistry == 5:
            chem = 'Nickel Metal Hydride'
        elif self.win.chemistry == 6:
            chem = 'Lithium-ion'
        elif self.win.chemistry == 7:
            chem = 'Zinc air'
        elif self.win.chemistry == 8:
            chem = 'Lithium Polymer'
        return chem


    @staticmethod
    def calcamps(self):
        if self.dischargerate > 0:
            return round(self.dischargerate / self.voltage, 3)
        elif self.chargerate > 0:
            return round(self.chargerate / self.voltage, 3)
        else:
            return 0


    # get object by name, used for treeview click to graph
    # discharge/charge power, amps, voltage, 
    def getbyname(self, name):
        # check portable
        name = name.replace(' ','')
        wbat = wmi.WMI().instances('win32_battery')[0]
        wport = wmi.WMI().instances('win32_portablebattery')[0]
        rwmi = self.rootwmi

        try:
            if name in rwmi.instances('BatteryStatus')[0].properties.keys():
                return rwmi.instances('BatteryStatus')[0].voltage
            if name in wbat.properties.keys():
                print(name)
                return getattr(wbat, name)

            if name in rwmi.instances('BatteryTemperature')[0].properties.keys():
                return rwmi.instances('BatteryTemperature')[0].temperature
            
            if name in rwmi.instances('BatteryStatus')[0].properties.keys():
                return rwmi.instances('BatteryStatus')[0].dischargerate
        except:
            print('no instance')


    # Some instances might not exist
    @staticmethod
    def tryinstance(self, prop):
        # for root/wmi instances
        tmp = self.rootwmi.instances(prop)
        if not tmp:     # check if empty
            return None
        else:
            if prop == 'BatteryCycleCount':
                return tmp[0].cyclecount
            elif prop == 'BatteryFullChargedCapacity':
                return tmp[0].fullchargedcapacity / 1000
            elif prop == 'BatteryControl':
                return tmp[0]
            elif prop == 'BatteryRunTime':
                if tmp[0].estimatedruntime <= 0:
                    self.hours = 0
                    self.minutes = 0
                    return 0
                else:
                    self.hours = int(tmp[0].estimatedruntime / 60)
                    self.minutes = int(tmp[0].estimatedruntime % 60)
                    return tmp[0].estimatedruntime / 60
            elif prop == 'BatteryTemperature':
                return tmp[0].temperature
            else:
                return tmp[0]
