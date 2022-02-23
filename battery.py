import wmi, time, sys

c = wmi.WMI()
t = wmi.WMI(moniker = "//./root/wmi")

batts1 = c.CIM_Battery()
for i, b in enumerate(batts1):
    print("Name:                       " + b.Name)
    print('Battery %d Design Capacity:  %d mWh' % (i, b.DesignCapacity or 0))
    print("Type:                       " + b.Caption)
    print("Chemistry:                  " + str(b.Chemistry))
    print("Design Voltage:             " + str(b.DesignVoltage))
    print("%:                          " + str(b.EstimatedChargeRemaining))
    print("Status                      " + str(b.Status) + '\n')
    if(b.EstimatedRunTime != None):
        print("EstimatedTime:              %d hours %d mins" % 
            (b.EstimatedRunTime/60, b.EstimatedRunTime%60))

batcycle= t.ExecQuery('select * from BatteryCycleCount')
for i, b in enumerate(batcycle):
    print('Battery %d Cycle Count: %d' % (i, b.CycleCount))

batts = t.ExecQuery('Select * from BatteryFullChargedCapacity')
for i, b in enumerate(batts):
    print ('Battery %d Fully Charged Capacity: %d mWh' % 
          (i, b.FullChargedCapacity))

# negative when charging
battrun = t.ExecQuery('select EstimatedRuntime from BatteryRuntime')
for v, p in enumerate(battrun):
    estMins = p.EstimatedRuntime/100.0
    print("Other estimated time:       %d h %d m" % 
        (estMins//60, estMins%60))


'''
def info():
    batts = t.ExecQuery('Select * from BatteryStatus where Voltage > 0')
    for i, b in enumerate(batts):
        print ('\nBattery %d ***************' % (i))
        print ("Tag:                   " + str(b.Tag))
        print ("Name:                  " + b.InstanceName)
        print ("PowerOnline:           " + str(b.PowerOnline))
        print ("Discharging:           " + str(b.Discharging))
        print ("Charging:              " + str(b.Charging))
        print ("Voltage:               " + str(b.Voltage/1000) + " Volts")
        print ("DischargeRate:         " + str(b.DischargeRate/1000) + " Watts")
        print ("ChargeRate:            " + str(b.ChargeRate/100) + " Watts")
        print ("RemainingCapacity:     " + str(b.RemainingCapacity) + " mWh")
        print ("Active:                " + str(b.Active))
        print ("Critical:              " + str(b.Critical))
        print ("Amps:                  " + str(round((b.DischargeRate / b.Voltage), 4)) + " Amps")

while(True):
    try:
        info()
        time.sleep(3)
    except KeyboardInterrupt:
        print()
        sys.exit()
'''