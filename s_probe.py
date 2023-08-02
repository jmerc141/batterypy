# probe.py

import wmi

class sProbe(object):

    #voltage = amps = watts = runtime = fullcap = remcap = 0

    @staticmethod
    def init() -> None:
        stat = wmi.WMI(moniker="//./root/wmi").instances('BatteryStatus')[0]
        # Assume these always exist
        sProbe.voltage = stat.voltage / 1000
        if stat.dischargerate > 0:
            sProbe.discharge_rate = stat.dischargerate
            sProbe.amps = sProbe.discharge_rate / sProbe.voltage
        else:
            sProbe.discharge_rate = 'N/A'
            sProbe.amps = 'N/A'
        
        # Might be negative
        if stat.chargerate > 0:
            sProbe.charge_rate = stat.chargerate / 1000
            sProbe.amps = sProbe.charge_rate / sProbe.voltage
        else:
            sProbe.charge_rate = 'N/A'
            sProbe.amps = 'N/A'

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

        # static data
        sd = wmi.WMI(moniker="//./root/wmi").instances('BatteryStaticData')[0]
        sProbe.capab = sd.capabilities
        sProbe.ogchem = sd.chemistry
        sProbe.critbi = sd.criticalbias
        sProbe.critalarm = sd.defaultalert1 / 1000    #mwh
        sProbe.lowalarm = sd.defaultalert2 / 1000
        sProbe.descap = sd.designedcapacity / 1000
        sProbe.mdate = sd.manufacturedate
        sProbe.sn = sd.serialnumber
        sProbe.g0 = float(sd.granularity0) / 100000000000
        sProbe.g1 = float(sd.granularity1) / 10000000000000
        sProbe.g2 = sd.granularity2
        sProbe.g3 = sd.granularity3

        # win32battery
        w = wmi.WMI().instances('win32_battery')[0]
        sProbe.avail = w.availability
        sProbe.bstatus = w.batterystatus
        sProbe.caption = w.caption
        sProbe.wchem = w.chemistry
        sProbe.desc = w.description
        sProbe.design_voltage = w.designvoltage
        sProbe.des_cap2 = w.designcapacity
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
        sProbe.system_name = w.systemname
            

        print()


    # Some instances might not exist
    @staticmethod
    def tryinstance(prop):
        # for root/wmi instances
        try:
            tmp = wmi.WMI(moniker="//./root/wmi").instances(prop)
            if prop == 'BatteryCycleCount':
                return tmp[0].cyclecount
            elif prop == 'BatteryFullChargedCapacity':
                return tmp[0].fullchargedcapacity / 1000
            elif prop == 'BatteryControl':
                return tmp[0]
            elif prop == 'BatteryRunTime':
                if tmp[0].estimatedruntime <= 0:
                    sProbe.hours = 0
                    sProbe.minutes = 0
                    return None
                else:
                    sProbe.hours = int(tmp[0].estimatedruntime / 60)
                    sProbe.minutes = int(tmp[0].estimatedruntime % 60)
                    return tmp[0].estimatedruntime / 60
            elif prop == 'BatteryTemperature':
                return tmp[0].temperature
            else:
                return tmp[0]
        except Exception as e:
            print(f'{prop} does not exist \n{e}')
            return 'N/A'
