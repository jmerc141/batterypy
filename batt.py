import wmi

c = wmi.WMI()
batts = c.CIM_Battery()
batteries = []
a = wmi.WMI().CIM_Battery	

class battInfo:
	val = []
	def __init__(self, dictInfo = {}):
		self.dictInfo = dictInfo

	def up(self, obj):
		self.dictInfo.update(obj)

	# returns info in dictionary based on key, individual battery
	def getter(self, inf):
		return self.dictInfo[inf]

	# updates the value absed on key
	def update(self, i):
		temp = c.CIM_Battery()
		for prop in list(a.properties):
				battInfo.val[i].up({prop: getattr(temp[i], prop, '')})

	# adds all connected batteries to val list
	# only run once
	def create(self):
		for i in range(len(batts)):
			x = battInfo(dict())
			for prop in list(a.properties):
				x.up({prop: getattr(batts[i], prop, '')})
			battInfo.val.append(x)
