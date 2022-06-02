"""
holds battery info in a list of dicts
the list is necessary if there is more than one battery

figure out how to handle more than one battery with cim_battery, wmi only holds
one instance seemingly. Also figure out how to omit empty values in every query
"""

import wmi

cim_battery = wmi.WMI().CIM_Battery()				# batts[0] is 0 instance, batts[1] if second battery
p = wmi.WMI().CIM_Battery							# all possible properties
w = wmi.WMI(moniker = "//./root/wmi")

print(w.BatteryStatus()[0].ChargeRate)

allbatteries = list()
mybatteries = dict()
mywmi = list()

# this part next, the root/wmi
#mywmi.append(t.ExecQuery('select * from BatteryCycleCount'))
#mywmi.append(t.ExecQuery('select * from BatteryStatus'))
#batcycle = t.ExecQuery('select * from BatteryCycleCount')

print(getattr(cim_battery[0], "DesignVoltage"))

for x, y in enumerate(cim_battery):
	print(x, y.DesignVoltage)

# end of part

if len(cim_battery) > 1:
	print('list needed')
	for i in range(len(cim_battery)):						# loop through all connected batteries
		for prop in p.properties:					# loops through all possible properties, even empty
			val = getattr(cim_battery[i], prop)			# gets the value of property
			if val == None or val == 0:				# ignores empty or 0 values
				pass
			else:
				tmp = mybatteries
				tmp.update({prop: val})				# add the key and value to the mybatteries dict (map)
		allbatteries.append(tmp)					# add populated dict to list
else:
	print('list not needed, only 1 battery')



class batteryInfo:
	val = []
	def __init__(self, dictInfo = {}):
		self.dictInfo = dictInfo

	def up(self, obj):
		self.dictInfo.update(obj)

	def getter(self, inf):
		'''returns info in dictionary based on key, individual battery'''
		return self.dictInfo[inf]

	# updates the value based on key
	def update(self, i):
		temp = wmi.WMI().CIM_Battery()
		for prop in list(p.properties):
				batteryInfo.val[i].up({prop: getattr(temp[i], prop, '')})

	# adds all connected batteries to val list
	# only run once
	# MORE THAN ONE BATTERY
	def create(self):
		for i in range(len(cim_battery)):
			x = batteryInfo(dict())
			for prop in list(p.properties):
				x.up({prop: getattr(cim_battery[i], prop, '')})
			batteryInfo.val.append(x)
