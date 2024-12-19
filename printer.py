'''
    TODO Make CLI option
'''

import sys

if sys.platform == 'linux':
    import s_probe_l
    probe = s_probe_l.sProbe
elif sys.platform == 'win32':
    import s_probe
    probe = s_probe.sProbe


def printbat():
    # all win32battery properties
    print('{:>22}{:10}{:<}'.format('Name:', ' ', probe.win.name))
    print('{:>22}{:10}{:<}'.format('Caption:', ' ', probe.win.Caption))
    print('{:>22}{:10}{:<}'.format('Description:', ' ', probe.win.description))
    print('{:>22}{:10}{:<d}'.format('Availability:', ' ', probe.win.Availability))  # decode
    print('{:>22}{:10}{:<d}'.format('Battery Status:', ' ', probe.win.batterystatus))   # decode
    print('{:>22}{:10}{:<d}'.format('Chemistry:', ' ', probe.win.Chemistry))    # decode number
    print('{:>22}{:10}{:<d}h {:d}m'.format('Time Remaining:', ' ',
                                           probe.win.Estimatedruntime // 60 % 24, probe.win.estimatedruntime % 60))

    print('{:>22}{:10}{:<g} V'.format('Design Voltage:', ' ', int(probe.win.designvoltage) / 1000))
    print('{:>22}{:10}{:<d}%'.format('Charge:', ' ', probe.win.estimatedchargeremaining))
    print('{:>22}{:10}{:<}'.format('Status:', ' ', probe.win.Status))

    print('\nFrom root/wmi:')
    print('{:>22}{:10}{:<d}h {:<d}m'.format('Other Estimated Time:', ' ', int(probe.hours), int(probe.minutes)))
    print('{:>22}{:10}{:<g} Wh'.format('Designed Capacity:', ' ', probe.descap))
    print('{:>22}{:10}{:<g} Wh'.format('Full Charged Capacity:', ' ', probe.fullcap))
    print('{:>22}{:10}{:<} Cycles'.format('Cycle Count:', ' ', probe.cyclecount))
    print('{:>22}{:10}{:<} C'.format('Temperature:', ' ', probe.temp))
    print('{:>22}{:10}{:<}'.format('Charging:', ' ', str(probe.charging)))
    print('{:>22}{:10}{:<g} W'.format('Charge Rate:', ' ', probe.chargerate))
    print('{:>22}{:10}{:<}'.format('Discharging:', ' ', str(probe.discharging)))
    print('{:>22}{:10}{:<g} W'.format('Discharge Rate:', ' ', probe.dischargerate))
    print('{:>22}{:10}{:<g} Wh'.format('Remaining Capacity:', ' ', probe.remcap))
    print('{:>22}{:10}{:<g} V'.format('Voltage:', ' ', probe.voltage))
    print('{:>22}{:10}{:<}'.format('Power Online:', ' ', str(probe.poweronline)))
    print('{:>22}{:10}{:<}'.format('Critical:', ' ', str(probe.critical)))
    print('{:>22}{:10}{:<}'.format('Capabilities:', ' ', str(probe.capab)))
    print('{:>22}{:10}{:<}'.format('Chemistry?:', ' ', str(probe.chem)))
    print('{:>22}{:10}{:<g} Wh'.format('Low Alarm:', ' ', probe.lowalarm))
    print('{:>22}{:10}{:<g} Wh'.format('Critical Alarm:', ' ', probe.critalarm))
    print('{:>22}{:10}{:<}'.format('Critical Bias:', ' ', str(probe.critbi)))
    print('{:>22}{:10}{:<}'.format('Manufacture Date:', ' ', probe.mdate))
    print('{:>22}{:10}{:<}'.format('Serial Number:', ' ', probe.sn))
    print('{:>22}{:10}{:<g} Wh'.format('Granularity 1:', ' ', probe.g0))
    print('{:>22}{:10}{:<g} Wh'.format('Granularity 2:', ' ', probe.g1))

    print('{:>22}{:10}{:<g} Ah'.format('Amp / Hour:', ' ', probe.ah))
    print('{:>22}{:10}{:<g} A'.format('Amps:', ' ', probe.amps))

#printbat()

import time

while(True):
    probe.refresh()
    print(probe.dischargerate)
    time.sleep(1)
