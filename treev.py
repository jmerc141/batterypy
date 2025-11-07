import s_probe

class Treev:
    '''
        This class does not hold the treeview gui element, it only handles treeview data
        TODO: change divide scale so windows and linux match
    '''

    maxv = maxa = maxw = 0

    @staticmethod
    def setup_tree():
        if s_probe.sProbe.charging:
            charge_string = 'Charging Power 🔌'
        else:
            charge_string = 'Discharge Power ⚡'

        
        tree_data_2 = [
            {'prop': 'Device Name', 'val': s_probe.sProbe.deviceName, 'max': '', 'open': False, 'subdata': []},
            {'prop': 'Manufacturer', 'val': s_probe.sProbe.manufName, 'max': '', 'open': False, 'subdata': []},
            {'prop': 'Serial Number', 'val': s_probe.sProbe.serial_num, 'max': '', 'open': False, 'subdata': []},
            {'prop': 'Chemistry', 'val': s_probe.sProbe.chemistry, 'max': '', 'open': False, 'subdata': []},
            {'prop': 'Cycle Count', 'val': s_probe.sProbe.cycleCount, 'max': '', 'open': False, 'subdata': []},
            {'prop': 'Status', 'val': s_probe.sProbe.status, 'max': '', 'open': False, 'subdata': []},
            {'prop': 'Est. Charge', 'val': s_probe.sProbe.chargeRemaining, 'max': '', 'open': False, 'subdata': []},
            # Power info
            {'prop': charge_string, "val": "", 'max': '', "open": True, "subdata": [
                {"prop": 'Design Voltage', 'val': f'{s_probe.sProbe.designVoltage:.3f}', 'max': ''},
                {"prop": 'Voltage', 'val': s_probe.sProbe.voltage, 'max': 0},
                {"prop": 'Amps', 'val': s_probe.sProbe.amps, 'max': 0},
                {"prop": 'Watts', 'val': s_probe.sProbe.watts, 'max': 0},
            ]},
            # Capacity info
            {'prop': 'Capacity', 'val': '', 'max': '', 'open': True, 'subdata': [
                {'prop': 'Design Wh', 'val': f'{s_probe.sProbe.designCapacity:.3f} Wh', 'max': ''},
                {'prop': 'Full Charged Wh', 'val': f'{s_probe.sProbe.fullChargeCap:.3f} Wh', 'max': ''},
                {'prop': 'Remaining Wh', 'val': f'{s_probe.sProbe.capRemaining:.3f} Wh', 'max': ''},
                {'prop': 'Health', 'val': f'{s_probe.sProbe.health:.2f}%', 'max': '', 'open': False, 'subdata': []},
                {'prop': 'Est. Time', 'val': f'{s_probe.sProbe.hours}h {s_probe.sProbe.minutes}m', 'max': ''},
            ]},   
        ]

        return tree_data_2


    @ staticmethod
    def update(tv):
        if s_probe.sProbe.charging:
            charge_string = 'Charging Power 🔌'
            if s_probe.sProbe.chargerate > Treev.maxw:
                Treev.maxw = s_probe.sProbe.chargerate
        elif not s_probe.sProbe.charging:
            charge_string = 'Discharge Power ⚡'
            if s_probe.sProbe.dischargerate > Treev.maxw:
                Treev.maxw = s_probe.sProbe.dischargerate
        else:
            charge_string = 'Full'
            

        # Max values column
        if s_probe.sProbe.voltage > Treev.maxv:
            Treev.maxv = s_probe.sProbe.voltage
        if s_probe.sProbe.amps > Treev.maxa:
            Treev.maxa = s_probe.sProbe.amps

        # Thanks ChatGPT
        # Update charging string in tree, using index in tree
        tv.item(7, values=(f'{s_probe.sProbe.chargeRemaining}%', ''))

        tv.item(8, text=f'{charge_string}')

        # Update values in tree
        # Volts
        tv.item(10, values=(f'{s_probe.sProbe.voltage:.3f} V', Treev.maxv))
        # Amps
        tv.item(11, values=(f'{s_probe.sProbe.amps:.3f} A', Treev.maxa))
        # Watts
        tv.item(12, values=(f'{s_probe.sProbe.watts:.3f} W', Treev.maxw))
        # Rem cap
        tv.item(16, values=(f'{s_probe.sProbe.capRemaining:.3f} Wh', ''))
        # Health
        tv.item(17, values=(f'{s_probe.sProbe.health:.2f}%', ''))
        # Time
        tv.item(18, values=(f'{s_probe.sProbe.hours}h {s_probe.sProbe.minutes}m', ''))

        # TODO: add health update here
        

