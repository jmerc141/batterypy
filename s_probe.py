# probe.py

import wmi, time, pythoncom
from threading import Thread

class sProbe(object):

    voltage = amps = watts = runtime = fullcap = rem_cap = dischargerate = chargerate = 0
    rwmi = wmi.WMI(moniker="//./root/wmi")
    going = True

    @staticmethod
    def __init__() -> None:
        try:
            sProbe.initWin32Bat()
        except TypeError as e:
            raise TypeError('Win32Battery is null', e)
        sProbe.getStaticData()
        sProbe.getRootWmi()
        sProbe.get_portable()
        sProbe.get_health()
        sProbe.get_chem()
        sProbe.th = Thread(target=sProbe.refresh)
        sProbe.th.start()


    @staticmethod
    def refresh():
        while(sProbe.going):
            pythoncom.CoInitialize()
            sProbe.getWin32Bat()
            sProbe.getRootWmi()
            time.sleep(1)
            

    @staticmethod
    def get_portable():
        if wmi.WMI().instances('win32_portablebattery'):
            sProbe.portable = wmi.WMI().instances('win32_portablebattery')[0]
        else:
            sProbe.portable = None

    @staticmethod
    def getRootWmi():
        #r = wmi.WMI(moniker="//./root/wmi").instances('BatteryStatus')[0]
        #stat = sProbe.rwmi.instances('BatteryStatus')[0]
        stat = wmi.WMI(moniker="//./root/wmi").instances('BatteryStatus')[0]
        #stat = sProbe.rwmi.ExecQuery('select * from BatteryStatus')[0]

        sProbe.charging = stat.charging
        sProbe.critical = stat.critical
        sProbe.discharging = stat.discharging
        sProbe.rem_cap = stat.remainingcapacity
        sProbe.power_online = stat.poweronline
        sProbe.active = stat.active
        sProbe.runtime = sProbe.tryinstance('BatteryRunTime')
        sProbe.cycle_count = sProbe.tryinstance('BatteryCycleCount')
        sProbe.full_cap = sProbe.tryinstance('BatteryFullChargedCapacity')
        sProbe.temp = sProbe.tryinstance('BatteryTempurature')
        sProbe.control = sProbe.tryinstance('BatteryControl')

        # Assume these always exist
        sProbe.voltage = stat.voltage / 1000
        if not sProbe.charging:
            if stat.dischargerate >= 0:
                sProbe.dischargerate = stat.dischargerate / 1000
                sProbe.amps = round(sProbe.dischargerate / sProbe.voltage, 3)
                sProbe.chargerate = 0
            else:
                sProbe.dischargerate = 0
                sProbe.amps = 0
        else:
            # Might be negative
            if stat.chargerate >= 0:
                sProbe.chargerate = stat.chargerate / 1000
                sProbe.amps = round(sProbe.chargerate / sProbe.voltage, 3)
            else:
                sProbe.chargerate = 0
                sProbe.amps = 0


    @staticmethod
    def getStaticData():
        sd = wmi.WMI(moniker="//./root/wmi").instances('BatteryStaticData')[0]
        sProbe.capab = sd.capabilities
        sProbe.ogchem = sd.chemistry
        sProbe.critbi = sd.criticalbias
        sProbe.critalarm = sd.defaultalert1 / 1000    #mwh
        sProbe.lowalarm = sd.defaultalert2 / 1000
        sProbe.descap = sd.designedcapacity
        sProbe.mdate = sd.manufacturedate
        sProbe.sn = sd.serialnumber
        sProbe.g0 = float(sd.granularity0) / 100000000000
        sProbe.g1 = float(sd.granularity1) / 10000000000000
        sProbe.g2 = sd.granularity2
        sProbe.g3 = sd.granularity3


    @staticmethod
    def getWin32Bat():
        w = wmi.WMI().instances('win32_battery')[0]
        sProbe.avail = w.availability
        sProbe.avail_str = sProbe.getAvail()
        sProbe.bstatus = w.batterystatus
        sProbe.est_chrg = w.estimatedchargeremaining
        sProbe.est_runtime = w.estimatedruntime
        sProbe.maxrechargetime = w.maxrechargetime
        sProbe.exp_bat_life = w.expectedbatterylife
        sProbe.exp_life = w.expectedlife
        sProbe.tob = w.timeonbattery
        sProbe.ttf = w.timetofullcharge
        sProbe.status = w.status
        sProbe.stat_str = sProbe.getStatus()

    @staticmethod
    def initWin32Bat():
        w = wmi.WMI().instances('win32_battery')[0]
        sProbe.avail = w.availability
        sProbe.avail_str = sProbe.getAvail()
        sProbe.bstatus = w.batterystatus
        sProbe.caption = w.caption
        sProbe.chem2 = w.chemistry
        sProbe.desc = w.description
        sProbe.design_voltage = w.designvoltage
        sProbe.descap2 = w.designcapacity
        sProbe.device_id = w.deviceid
        sProbe.est_chrg = w.estimatedchargeremaining
        sProbe.est_runtime = w.estimatedruntime
        sProbe.maxrechargetime = w.maxrechargetime
        sProbe.exp_bat_life = w.expectedbatterylife
        sProbe.exp_life = w.expectedlife
        sProbe.tob = w.timeonbattery
        sProbe.ttf = w.timetofullcharge
        sProbe.name = w.name
        sProbe.pmc = w.powermanagementcapabilities
        sProbe.status = w.status
        sProbe.stat_str = sProbe.getStatus()
        sProbe.system_name = w.systemname
        sProbe.err_desc = w.errordescription
    

    @staticmethod
    def getw32bat_inst():
            return wmi.WMI().instances('win32_battery')[0]


    @staticmethod
    def get_health():
        if sProbe.descap is not None:
            sProbe.bathealth = (sProbe.full_cap / sProbe.descap) * 100
        elif sProbe.descap2 is not None:
            sProbe.bathealth = sProbe.full_cap / sProbe.descap2

    
    @staticmethod
    def get_chem():
        if sProbe.ogchem is not None:
            sProbe.chem_str = sProbe.getchemstr(sProbe.ogchem)
        elif sProbe.chem2 is not None:
            sProbe.chem_str = sProbe.getchemstr(sProbe.chem2)

    # Some instances might not exist
    @staticmethod
    def tryinstance(prop):
        # for root/wmi instances
        try:
            tmp = wmi.WMI(moniker="//./root/wmi").instances(prop)
            if prop == 'BatteryCycleCount':
                return tmp[0].cyclecount
            elif prop == 'BatteryFullChargedCapacity':
                return tmp[0].fullchargedcapacity
            elif prop == 'BatteryControl':
                return tmp[0]
            elif prop == 'BatteryRunTime':
                if tmp[0].estimatedruntime <= 0:
                    sProbe.hours = 0
                    sProbe.minutes = 0
                    return None
                else:
                    sProbe.hours = int(tmp[0].estimatedruntime / 3600)
                    sProbe.minutes = int(tmp[0].estimatedruntime % 60)
                    return tmp[0].estimatedruntime / 60
            elif prop == 'BatteryTemperature':
                return tmp[0].temperature
            else:
                return tmp[0]
        except Exception as e:
            #print(f'{prop} does not exist \n{e}')
            return 'N/A'


    @staticmethod
    def getStatus() -> str:
        statcode = sProbe.status
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
    def getchemstr(ch) -> str:
        # only call from refresh
        if ch == 1:
            chem = 'Other'
        elif ch == 2:
            chem = 'Unknown'
        elif ch == 3:
            chem = 'Lead Acid'
        elif ch == 4:
            chem = 'Nickel Cadmium'
        elif ch == 5:
            chem = 'Nickel Metal Hydride'
        elif ch == 6:
            chem = 'Lithium-ion'
        elif ch == 7:
            chem = 'Zinc air'
        elif ch == 8:
            chem = 'Lithium Polymer'
        else:
            chem = 'N/A'
        return chem
    

    @staticmethod
    def getAvail() -> str:
        # only call from refresh
        avail = sProbe.avail
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
    def on_close():
        print('closing')
        sProbe.going = False

