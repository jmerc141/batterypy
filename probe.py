from batt import batteryInfo

myb = batteryInfo()
print(myb.batCount())
#rootwmi
print(myb.getrw().BatteryStatus()[0].Voltage)
#cim
print(myb.cim.get('EstimatedRunTime'))

time = myb.cim.get('EstimatedRunTime')
days = time // 1440
hours = time // 60 % 24
mins = time % 60
print(str(days) + " days, " + str(hours) + " hours, " + str(mins) +  " mins. ")
print(myb.rootwmi.BatteryFullChargedCapacity()[0].FullChargedCapacity)


#print(getattr(cim_battery[0], "DesignVoltage"))

#for x, y in enumerate(cim_battery):
#	print(x, y.DesignVoltage)