
maxv = maxamps = maxw = 0


def setup_tree(probe):
    global maxw
    global maxv
    global maxamps

    if probe.charging:
        charge_string = 'Charging Power 🔌'
    else:
        charge_string = 'Discharge Power ⚡'

    # initialize max var, and initialize column
    maxv = probe.voltage
    maxamps = probe.amps
    maxw = probe.watts

    if probe.msbatt['BatteryStatus']['Charging']:
        if probe.chargerate > maxw:
            maxw = probe.chargerate
    else:
        if probe.dischargerate > maxw:
            maxw = probe.dischargerate

    # Max values column
    if probe.voltage > maxv:
        maxv = probe.voltage
    if probe.amps > maxamps:
        maxamps = probe.amps
    

    tree_data_2 = [
        {'prop': charge_string, "val": "", 'max': '', "open": True, "subdata": [
            {"prop": 'Design Voltage', 'val': int(probe.win32bat['DesignVoltage']) / 1000, 'max': ''},
            {"prop": 'Voltage', 'val': probe.voltage, 'max': maxv},
            {"prop": 'Amps', 'val': probe.amps, 'max': maxamps},
            {"prop": 'Watts', 'val': probe.watts, 'max': maxw},
        ]},
        #{"power": "orange", "color": "orange", "open": False, "subdata": [
        #    {"power": "pear"}
        #]},
        #{"power": "lemon"},
    ]

    return tree_data_2


def update(tv, probe):
    global maxw
    global maxv
    global maxamps

    if probe.msbatt['BatteryStatus']['Charging']:
        charge_string = 'Charging Power 🔌'
    elif probe.msbatt['BatteryStatus']['Discharging']:
        charge_string = 'Discharge Power ⚡'
    else:
        charge_string = 'Niether?'

    if probe.msbatt['BatteryStatus']['Charging']:
        if probe.chargerate > maxw:
            maxw = probe.chargerate
    else:
        if probe.dischargerate > maxw:
            maxw = probe.dischargerate

    # Max values column
    if probe.voltage > maxv:
        maxv = probe.voltage
    if probe.amps > maxamps:
        maxamps = probe.amps

    # Thanks ChatGPT

    # Update charging string in tree
    tv.item(1, text=f'{charge_string}')    

    # Update values in tree
    tv.item(3, values=(f'{probe.voltage:.3f} V', maxv))
    tv.item(4, values=(f'{probe.amps:.3f} A', maxamps))
    tv.item(5, values=(f'{probe.watts:.3f} W', maxw))
    

    


