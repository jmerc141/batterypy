"""
only use win32_battery, cim is parent class
dont forget other win32_battery properties, root/wmi done

add check for null, try except block
"""

import wmi


class Probe:

    def __init__(self):
        # get instance of win32battery, [0] for first entry
        # may need to refresh instance
        self.win = wmi.WMI().instances('win32_battery')[0]  # [0] is battery
        self.__rootwmi = wmi.WMI(moniker="//./root/wmi")

        self.runtime = self.__rootwmi.ExecQuery('select * from BatteryRunTime')[0].estimatedruntime / 60
        self.hours = int(self.runtime / 60)
        self.minutes = int(self.runtime % 60)
        self.fullcap = \
            self.__rootwmi.ExecQuery('select * from BatteryFullChargedCapacity where FullChargedCapacity > 0')[
                0].fullchargedcapacity / 1000
        try:
            self.cyclecount = str(self.__rootwmi.ExecQuery('select * from BatteryCycleCount')[
                                      0].cyclecount)
        except IndexError:
            print('Could not get Cycle Count')
            self.cyclecount = 'N/A'
        try:
            # get units
            self.temp = str(self.__rootwmi.ExecQuery('select * from BatteryTemperature')[0].temperature)
        except IndexError:
            print('Could net get Temperature')
            self.temp = 'N/A'

        # later
        self.tagchange = self.__rootwmi.ExecQuery('select * from BatteryTagChange')
        self.statchange = self.__rootwmi.ExecQuery('selct * from BatteryStatusChange')

        status = self.__rootwmi.ExecQuery('select * from BatteryStatus')
        self.chargerate = status[0].chargerate / 1000
        self.charging = status[0].charging
        self.critical = status[0].critical
        self.dischargerate = status[0].dischargerate / 1000
        self.discharging = status[0].discharging
        self.poweronline = status[0].poweronline
        self.remcap = status[0].remainingcapacity / 1000
        self.voltage = status[0].voltage / 1000

        staticdata = self.__rootwmi.ExecQuery('select * from BatteryStaticData')
        self.capab = staticdata[0].capabilities
        self.chem = staticdata[0].chemistry
        self.critbi = staticdata[0].criticalbias
        self.critalarm = staticdata[0].defaultalert1 / 1000
        self.lowalarm = staticdata[0].defaultalert2 / 1000
        self.descap = staticdata[0].designedcapacity / 1000
        self.mdate = staticdata[0].manufacturedate
        self.sn = staticdata[0].serialnumber
        self.g0 = float(staticdata[0].granularity0) / 100000000000
        self.g1 = float(staticdata[0].granularity1) / 10000000000000
        self.g2 = staticdata[0].granularity2
        self.g3 = staticdata[0].granularity3

        # calculated values
        self.ah = self.remcap / self.voltage
        self.amps = self.dischargerate / self.voltage
        self.bathealth = (self.fullcap / self.descap) * 100  # percent

    def refresh(self):
        # queries all wmi values and resets variables
        print('refreshed')
        self.runtime = self.__rootwmi.ExecQuery('select * from BatteryRunTime')[0].estimatedruntime / 60
        self.hours = int(self.runtime / 60)
        self.minutes = int(self.runtime % 60)
        self.fullcap = \
            self.__rootwmi.ExecQuery('select * from BatteryFullChargedCapacity where FullChargedCapacity > 0')[
                0].fullchargedcapacity / 1000
        try:
            self.cyclecount = str(self.__rootwmi.ExecQuery('select * from BatteryCycleCount')[
                                      0].cyclecount)
        except IndexError:
            print('Could not get Cycle Count')
            self.cyclecount = 'N/A'
        try:
            # get units
            self.temp = str(self.__rootwmi.ExecQuery('select * from BatteryTemperature')[0].temperature)
        except IndexError:
            print('Could net get Temperature')
            self.temp = 'N/A'

        # later
        self.tagchange = self.__rootwmi.ExecQuery('select * from BatteryTagChange')
        self.statchange = self.__rootwmi.ExecQuery('selct * from BatteryStatusChange')

        status = self.__rootwmi.ExecQuery('select * from BatteryStatus')
        self.chargerate = status[0].chargerate / 1000
        self.charging = status[0].charging
        self.critical = status[0].critical
        self.dischargerate = status[0].dischargerate / 1000
        self.discharging = status[0].discharging
        self.poweronline = status[0].poweronline
        self.remcap = status[0].remainingcapacity / 1000
        self.voltage = status[0].voltage / 1000

        # calculated values
        self.ah = self.remcap / self.voltage
        self.amps = self.dischargerate / self.voltage
        self.bathealth = (self.fullcap / self.descap) * 100  # percent


