"""
only use win32_battery, cim is parent class
address win32 battery: w[0].property

amps = discharge rate / voltage
ah = wh / v
"""

import wmi

w = wmi.WMI().instances('win32_battery')        # w[0] is battery
t = wmi.WMI(moniker = "//./root/wmi")

# all win32battery properties
print('{:>22}{:10}{:<}'.format('Name:', ' ', w[0].name))
print('{:>22}{:10}{:<}'.format('Caption:', ' ', w[0].Caption))
print('{:>22}{:10}{:<}'.format('Description:', ' ', w[0].description))
print('{:>22}{:10}{:<d}'.format('Availability:', ' ', w[0].Availability))
print('{:>22}{:10}{:<d}'.format('Battery Status:', ' ', w[0].batterystatus))

print('{:>22}{:10}{:<d}'.format('Chemistry:', ' ', w[0].Chemistry))
print('{:>22}{:10}{:<d}h {:d}m'.format('Time Remaining:', ' ',
                                       w[0].Estimatedruntime//60 % 24, w[0].estimatedruntime % 60))

print('{:>22}{:10}{:<g} V'.format('Design Voltage:', ' ', int(w[0].designvoltage) / 1000))
print('{:>22}{:10}{:<d}%'.format('Charge %:', ' ', w[0].estimatedchargeremaining))
print('{:>22}{:10}{:<}'.format('Status:', ' ', w[0].Status))


# always used [0] subscript because there should only ever be 1 instance
# in the class
# all root/wmi instances and properties
print('\nRoot/wmi')
runtime = t.ExecQuery('select * from BatteryRunTime where EstimatedRunTime > 0')    # in seconds
for i, b in enumerate(runtime):
    secs = b.EstimatedRunTime / 60
    print('{:>22}{:10}{:<d}h {:<d}m'.format('Other Estimated Time:', ' ', int(secs//60), int(secs%60)))

cyclecount = t.ExecQuery('select * from BatteryCycleCount where CycleCount > 0')
for i, b in enumerate(cyclecount):
    print('{:>22}{:10}{:<d} Cycles'.format('Cycle Count:', ' ', b.cyclecount))

fullcap = t.ExecQuery('select * from BatteryFullChargedCapacity where FullChargedCapacity > 0') # in milliwatt/hours
for i, b in enumerate(fullcap):
    wh = b.FullChargedCapacity / 1000
    print('{:>22}{:10}{:<g} Wh'.format('Full Charged Capacity:', ' ', wh))

# need property name
temp = t.ExecQuery('select * from BatteryTemperature')
for i, b in enumerate(cyclecount):
    print('{:>22}{:10}{:<d} C'.format('Temperature:', ' ', b.temperature))

tagchange = t.ExecQuery('select * from BatteryTagChange')
statchange = t.ExecQuery('selct * from BatteryStatusChange')

status = t.ExecQuery('select * from BatteryStatus')
for i, b in enumerate(status):
    print('{:>22}{:10}{:<g} W'.format('Charge Rate:', ' ', b.ChargeRate/1000))
    print(b.Charging)
    print(b.critical)
    print('{:>22}{:10}{:<g} W'.format('Discharge Rate:', ' ', b.disChargeRate/1000))
    print(b.discharging)
    print(b.poweronline)
    print('{:>22}{:10}{:<g} Wh'.format('Remaining Capacity:', ' ', b.remainingcapacity/1000))
    print('{:>22}{:10}{:<g} V'.format('Voltage:', ' ', b.voltage/1000))

staticdata = t.ExecQuery('select * from BatteryStaticData')
for i, b in enumerate(staticdata):
    print(b.capabilities)
    print(b.chemistry)
    print(b.criticalbias)
    print(b.defaultalert1)
    print(b.defaultalert2)
    print('{:>22}{:10}{:<g} Wh'.format('Designed Capacity:', ' ', b.designedcapacity/1000))
    print(b.granularity0)
    print(b.manufacturedate)
    print(b.serialnumber)
