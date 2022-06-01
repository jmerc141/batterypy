"""
holds battery info in a list of dicts
the list is necessary if there is more than one battery
"""

import wmi

batts = wmi.WMI().CIM_Battery()
a = wmi.WMI().CIM_Battery							# all possible properties
t = wmi.WMI(moniker = "//./root/wmi")

allbatteries = list()
mybatteries = dict()
mywmi = list()

# this part next, the root/wmi
mywmi.append(t.ExecQuery('select * from BatteryCycleCount'))
mywmi.append(t.ExecQuery('select * from BatteryStatus'))
batcycle = t.ExecQuery('select * from BatteryCycleCount')

for x, y in enumerate(batcycle):
	print(x, y.CycleCount)

# end of part

if len(batts) > 1:
	print('list needed')
	for i in range(len(batts)):						# loop through all connected batteries
		for prop in a.properties:					# loops through all possible properties, even empty
			val = getattr(batts[i], prop)			# gets the value of property
			if val == None or val == 0:				# ignores empty or 0 values
				pass
			else:
				tmp = mybatteries
				tmp.update({prop: val})				# add the key and value to the mybatteries dict (map)
		allbatteries.append(tmp)					# add populated dict to list
else:
	print('list not needed')

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
		for prop in list(a.properties):
				batteryInfo.val[i].up({prop: getattr(temp[i], prop, '')})

	# adds all connected batteries to val list
	# only run once
	# MORE THAN ONE BATTERY
	def create(self):
		for i in range(len(batts)):
			x = batteryInfo(dict())
			for prop in list(a.properties):
				x.up({prop: getattr(batts[i], prop, '')})
			batteryInfo.val.append(x)
