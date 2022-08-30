"""
holds battery info in a list of dicts
the list is necessary if there is more than one battery

figure out how to handle more than one battery with cim_battery, wmi only holds
one instance seemingly. Also figure out how to omit empty values in every query
allow option to hide empty key/values
"""

import wmi

class batteryInfo:
	cim_battery = wmi.WMI().CIM_Battery()  					# batts[0] is 0th instance, batts[1] if second battery
	cim_props = wmi.WMI().CIM_Battery.properties.keys()  	# all possible properties
	rootwmi = wmi.WMI(moniker="//./root/wmi")				# rootwmi reference

	"""init"""
	def __init__(self, empty = {}):
		self.cim = empty
		count = self.batCount()
		if count == 1:
			self.createOne()
		elif count == 2:
			self.createMany()
		else:
			print("Unable to get battery count")

	"""Get the number of connected batteries"""
	def batCount(self):
		return len(self.cim_battery)

	"""Returns root/wmi instance"""
	def getrw(self):
		return self.rootwmi

	def getter(self, inf):
		"""returns info in dictionary based on key, individual battery"""
		return self.cim[inf]

	# adds all connected batteries to val list
	# only run once
	# MORE THAN ONE BATTERY
	def createMany(self):
		if len(self.batteries) < 0:
			for i in range(len(self.cim_battery)):
				x = batteryInfo(dict())
				for prop in self.cim_props:
					x.update({prop: getattr(self.cim_battery[i], prop, '')})
				batteryInfo.val.append(x)
		else:
			print("already instatiated")

	"""If only one battery is found then put the data in one dictionary"""
	def createOne(self):
		for props in self.cim_props:
			self.cim.update({props: getattr(self.cim_battery[0], props, '')})