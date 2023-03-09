"""
all win32_battery properties
Availability: 3
BatteryRechargeTime:
BatteryStatus: 1
Caption: Internal Battery
Chemistry: 2
ConfigManagerErrorCode:
ConfigManagerUserConfig:
CreationClassName: Win32_Battery
Description: Internal Battery
DesignCapacity:
DesignVoltage: 7600
DeviceID: 00EmdoorLi-ion Battery
ErrorCleared:
ErrorDescription:
EstimatedChargeRemaining: 75
EstimatedRunTime: 252
ExpectedBatteryLife:
ExpectedLife:
FullChargeCapacity:
InstallDate:
LastErrorCode:
MaxRechargeTime:
Name: Li-ion Battery
PNPDeviceID:
PowerManagementCapabilities: 1
PowerManagementSupported: False
SmartBatteryVersion:
Status: OK
StatusInfo:
SystemCreationClassName: Win32_ComputerSystem
SystemName: DESKTOP-3QOIFTC
TimeOnBattery:
TimeToFullCharge:


"""


import probe

p = probe.Probe()


def printbat():
    # all win32battery properties
    print('{:>22}{:10}{:<}'.format('Name:', ' ', p.win.name))
    print('{:>22}{:10}{:<}'.format('Caption:', ' ', p.win.Caption))
    print('{:>22}{:10}{:<}'.format('Description:', ' ', p.win.description))
    print('{:>22}{:10}{:<d}'.format('Availability:', ' ', p.win.Availability))  # decode
    print('{:>22}{:10}{:<d}'.format('Battery Status:', ' ', p.win.batterystatus))   # decode
    print('{:>22}{:10}{:<d}'.format('Chemistry:', ' ', p.win.Chemistry))    # decode number
    print('{:>22}{:10}{:<d}h {:d}m'.format('Time Remaining:', ' ',
                                           p.win.Estimatedruntime // 60 % 24, p.win.estimatedruntime % 60))

    print('{:>22}{:10}{:<g} V'.format('Design Voltage:', ' ', int(p.win.designvoltage) / 1000))
    print('{:>22}{:10}{:<d}%'.format('Charge:', ' ', p.win.estimatedchargeremaining))
    print('{:>22}{:10}{:<}'.format('Status:', ' ', p.win.Status))

    print('\nFrom root/wmi:')
    print('{:>22}{:10}{:<d}h {:<d}m'.format('Other Estimated Time:', ' ', int(p.hours), int(p.minutes)))
    print('{:>22}{:10}{:<g} Wh'.format('Designed Capacity:', ' ', p.descap))
    print('{:>22}{:10}{:<g} Wh'.format('Full Charged Capacity:', ' ', p.fullcap))
    print('{:>22}{:10}{:<} Cycles'.format('Cycle Count:', ' ', p.cyclecount))
    print('{:>22}{:10}{:<} C'.format('Temperature:', ' ', p.temp))
    print('{:>22}{:10}{:<}'.format('Charging:', ' ', str(p.charging)))
    print('{:>22}{:10}{:<g} W'.format('Charge Rate:', ' ', p.chargerate))
    print('{:>22}{:10}{:<}'.format('Discharging:', ' ', str(p.discharging)))
    print('{:>22}{:10}{:<g} W'.format('Discharge Rate:', ' ', p.dischargerate))
    print('{:>22}{:10}{:<g} Wh'.format('Remaining Capacity:', ' ', p.remcap))
    print('{:>22}{:10}{:<g} V'.format('Voltage:', ' ', p.voltage))
    print('{:>22}{:10}{:<}'.format('Power Online:', ' ', str(p.poweronline)))
    print('{:>22}{:10}{:<}'.format('Critical:', ' ', str(p.critical)))
    print('{:>22}{:10}{:<}'.format('Capabilities:', ' ', str(p.capab)))
    print('{:>22}{:10}{:<}'.format('Chemistry?:', ' ', str(p.chem)))
    print('{:>22}{:10}{:<g} Wh'.format('Low Alarm:', ' ', p.lowalarm))
    print('{:>22}{:10}{:<g} Wh'.format('Critical Alarm:', ' ', p.critalarm))
    print('{:>22}{:10}{:<}'.format('Critical Bias:', ' ', str(p.critbi)))
    print('{:>22}{:10}{:<}'.format('Manufacture Date:', ' ', p.mdate))
    print('{:>22}{:10}{:<}'.format('Serial Number:', ' ', p.sn))
    print('{:>22}{:10}{:<g} Wh'.format('Granularity 1:', ' ', p.g0))
    print('{:>22}{:10}{:<g} Wh'.format('Granularity 2:', ' ', p.g1))

    print('{:>22}{:10}{:<g} Ah'.format('Amp / Hour:', ' ', p.ah))
    print('{:>22}{:10}{:<g} A'.format('Amps:', ' ', p.amps))

printbat()
