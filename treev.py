class Treev:

    maxv = maxa = maxw = 0

    @staticmethod
    def setup_tree(probe):
        if probe.charging:
            charge_string = 'Charging Power 🔌'
        else:
            charge_string = 'Discharge Power ⚡'

        
        tree_data_2 = [
            {'prop': 'Device Name', 'val': probe.msbatt['BatteryStaticData']['DeviceName'], 'max': '', 'open': False, 'subdata': []},
            {'prop': 'Manufacturer', 'val': probe.msbatt['BatteryStaticData']['ManufactureName'], 'max': '', 'open': False, 'subdata': []},
            {'prop': 'Unique ID', 'val': probe.msbatt['BatteryStaticData']['UniqueID'], 'max': '', 'open': False, 'subdata': []},
            {'prop': 'Chemistry', 'val': probe.getchemstr(), 'max': '', 'open': False, 'subdata': []},
            {'prop': 'Health (Degraded)', 'val': probe.get_health(), 'max': '', 'open': False, 'subdata': []},
            {'prop': 'Cycle Count', 'val': probe.msbatt['BatteryCycleCount']['CycleCount'], 'max': '', 'open': False, 'subdata': []},
            {'prop': 'Status', 'val': probe.win32bat['Status'], 'max': '', 'open': False, 'subdata': []},
            # Power info
            {'prop': charge_string, "val": "", 'max': '', "open": True, "subdata": [
                {"prop": 'Design Voltage', 'val': int(probe.win32bat['DesignVoltage']) / 1000, 'max': ''},
                {"prop": 'Voltage', 'val': probe.voltage, 'max': 0},
                {"prop": 'Amps', 'val': probe.amps, 'max': 0},
                {"prop": 'Watts', 'val': probe.watts, 'max': 0},
            ]},
            # Capacity info
            {'prop': 'Capacity', 'val': '', 'max': '', 'open': True, 'subdata': [
                {'prop': 'Design Wh', 'val': f'{probe.msbatt['BatteryStaticData']['DesignedCapacity'] / 1000} Wh', 'max': ''},
                {'prop': 'Full Charged Wh', 'val': f'{probe.msbatt['BatteryFullChargedCapacity']['FullChargedCapacity'] / 1000} Wh', 'max': ''},
                {'prop': 'Remaining Wh', 'val': f'{probe.msbatt['BatteryStatus']['RemainingCapacity'] / 1000} Wh', 'max': ''},
                {'prop': 'Est. Time', 'val': f'{probe.hours}h {probe.minutes}m', 'max': ''},
            ]},   
        ]

        return tree_data_2


    @ staticmethod
    def update(tv, probe):
        if probe.msbatt['BatteryStatus']['Charging']:
            charge_string = 'Charging Power 🔌'
        elif probe.msbatt['BatteryStatus']['Discharging']:
            charge_string = 'Discharge Power ⚡'
        else:
            charge_string = '???'

        if probe.msbatt['BatteryStatus']['Charging']:
            if probe.chargerate > Treev.maxw:
                Treev.maxw = probe.chargerate
        else:
            if probe.dischargerate > Treev.maxw:
                Treev.maxw = probe.dischargerate

        # Max values column
        if probe.voltage > Treev.maxv:
            Treev.maxv = probe.voltage
        if probe.amps > Treev.maxa:
            Treev.maxa = probe.amps

        # Thanks ChatGPT
        # Update charging string in tree, using index in tree
        tv.item(8, text=f'{charge_string}')

        # Update values in tree
        tv.item(10, values=(f'{probe.voltage:.3f} V', Treev.maxv))
        tv.item(11, values=(f'{probe.amps:.3f} A', Treev.maxa))
        tv.item(12, values=(f'{probe.watts:.3f} W', Treev.maxw))
        
        tv.item(16, values=(f'{probe.msbatt['BatteryStatus']['RemainingCapacity'] / 1000} Wh', ''))
        tv.item(17, values=(f'{probe.hours}h {probe.minutes}m', ''))
        

