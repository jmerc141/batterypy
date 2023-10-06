# static probe.py
'''
power*  = microwatts / energy*
energy* = microwatt-hours
charge* = microamp-hours / current*
https://www.kernel.org/doc/Documentation/power/power_supply_class.txt
https://www.kernel.org/doc/Documentation/ABI/testing/sysfs-class-power
https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/include/linux/power_supply.h?h=v6.0.11
'''

import time, subprocess, os
from os import system
from threading import Thread

class sProbe(object):
    uevent = {}
    calculated_props = {'watts': '', 'timerem': '', 'amps': '', 'ah_full': '', 'ah_full_design': '', 'ah_now': '', 'wh_full': '',
                        'wh_full_design': '', 'wh_now': '', 'manufacture_date': ''}
    props = {'status': '', 'charge-type': '', 'authentic': '', 'health': '', 'voltage_now': '', 'voltage_ocv': '', 'voltage_max_design': '',
            'voltage_min_design': '', 'voltage_max': '', 'voltage_min': '', 'voltage_boot': '', 'current_boot': '', 'charge_full': '',
            'charge_empty': '','charge_full_design': '', 'charge_empty_design': '', 'energy_full_design': '', 'energy_empty_design': '',
            'energy_now': '', 'energy_full': '', 'charge_counter': '',
            'precharge_current': '','charge_term_current': '', 'constant_charge_current': '', 'constant_charge_current_max': '',
            'constant_charge_voltage': '', 'constant_charge_voltage_max': '', 'input_current_limit': '', 'charge_control_limit': '',
            'charge_control_limit_max': '', 'charge_control_start_threshold': '', 'charge_control_end_threshold': '',  'charge_type': '', 'present': '',
            'charge_behavior': '', 'calibrate': '', 'capacity': '', 'capacity_alert_min': '', 'capacity_alert_max': '', 'capacity_level': '',
            'capacity_error_margin': '', 'temp': '', 'temp_alert_min': '', 'temp_alert_max': '', 'temp_ambient': '', 'temp_ambient_alert_min': '',
            'temp_ambient_alert_max': '', 'temp_min': '', 'temp_max': '','time_to_empty': '', 'time_to_full': '', 'manufacturer': '', 'model_name': '',
            'serial_number': '', 'type': '', 'current_avg': '','current_max': '', 'current_now': '', 'technology': '', 'voltage_avg': '',
            'input_voltage_limit': '', 'input_power_limit': '', 'online': '', 'usb_type': '', 'charge_now': '', 'fast_charge_timer': '', 
            'top_off_threshold_current': '', 'top_off_timer': '', 'cycle_count': '', 'ovp_voltage': '', 'manufacture_year': '', 'manufacture_month': '',
            'manufacture_day': '', 'power_now': '', 'power_avg': '', 'manufacturer': ''}
    going = True

    @staticmethod
    def __init__() -> None:
        if os.path.exists('/sys/class/power_supply/BAT0'):
            sProbe.path = '/sys/class/power_supply/BAT0/'
        elif os.path.exists('/sys/class/power_supply/BAT1'):
            sProbe.path = '/sys/class/power_supply/BAT1/'
        else:
            print("No Batteries")
            raise Exception('No Batteries detected')
        sProbe.getStuff()
        sProbe.th = Thread(target=sProbe.refresh)
        sProbe.th.start()


    @staticmethod
    def check_prop(p: str) -> str:
        r = sProbe.props[p]
        if r == '':
            return 'N/A'
        else:
            return r


    @staticmethod
    def __catFile(fname: str) -> str:
        try:
            sProbe.props[fname] = subprocess.run(['cat', sProbe.path + fname], capture_output=True).stdout.decode().replace('\n', '')
        except KeyError as k:
            print('catfile error' + k)


    @staticmethod
    def get_uevent():
        # get all uevent props as dictionary
        u = subprocess.run(['cat', sProbe.path + 'uevent'], capture_output=True).stdout
        lines = u.splitlines()
        for properties in lines:
            str = properties.decode()
            s = str.split('=')
            sProbe.uevent[s[0]] = s[1]


    @staticmethod
    def getStuff():
        # cat all exisitng files and put into dictionary
        for i in sProbe.props:
            sProbe.__catFile(i)

        name = subprocess.run(['cat', '/etc/hostname'], capture_output=True)
        sProbe.props['sysname'] = name.stdout.decode()

        if sProbe.props['energy_now'] != '':
            # watt-hours / energy_now are available
            sProbe.wh = True
            sProbe.calculated_props['watts'] = sProbe.props['power_now']
            try:
                total_hours = int(sProbe.props['energy_now']) / int(sProbe.props['power_now'])
                hours = int(total_hours)
                mins = round(((total_hours - hours) * 60), 1)
                sProbe.calculated_props['timerem'] = str(hours) + 'h ' + str(mins) + 'm'
            except ZeroDivisionError as z:
                sProbe.calculated_props['timerem'] = 'N/A'

            try:
                sProbe.calculated_props['amps'] = (int(sProbe.props['power_now']) / int(sProbe.props['voltage_now']) * 1000000)
            except ZeroDivisionError as z:
                sProbe.calculated_props['amps'] = 'N/A'
            
            sProbe.calculated_props['ah_full'] = round(int(sProbe.props['energy_full']) / int(sProbe.props['voltage_now']), 3)
            sProbe.calculated_props['ah_full_design'] = round(int(sProbe.props['energy_full_design']) / int(sProbe.props['voltage_now']), 3)
            sProbe.calculated_props['ah_now'] = round(int(sProbe.props['energy_now']) / int(sProbe.props['voltage_now']), 3)
        elif sProbe.props['charge_now'] != '':
            sProbe.wh = False
            # amp-hours / charge_now are available
            try:
                total_hours = int(sProbe.props['charge_now']) / int(sProbe.props['current_now'])
                hours = int(total_hours)
                mins = round(((total_hours - hours) * 60), 1)
                sProbe.calculated_props['timerem'] = str(hours) + 'h ' + str(mins) + 'm'
            except ZeroDivisionError as z:
                sProbe.calculated_props['timerem'] = 'N/A'

            v = int(sProbe.props['voltage_now']) / 1000000
            sProbe.calculated_props['watts'] = (v * float(sProbe.props['current_now']))
            sProbe.calculated_props['amps'] = float(sProbe.props['current_now'])
            sProbe.calculated_props['wh_full'] = round((float(sProbe.props['charge_full']) / 1000000) * v, 3)
            sProbe.calculated_props['wh_full_design'] = round((int(sProbe.props['charge_full_design']) / 1000000) * 
                                                    v, 3)
            sProbe.calculated_props['wh_now'] = round((int(sProbe.props['charge_now']) / 1000000) * v, 3)

        if sProbe.props['manufacture_year'] != '':
            m_year = sProbe.__catFile('manufacture_year')
            m_month = sProbe.__catFile('manufacture_month')
            m_day = sProbe.__catFile('manufacture_day')
            sProbe.calculated_props['manufacture_date'] = sProbe.props['manufacture_year'] + '/' 
            + sProbe.props['manufacture_month'] + '/' + sProbe.props['manufacture_day']
        else:
            sProbe.calculated_props['manufacture_date'] = 'N/A'

    @staticmethod
    def refresh():
        while(sProbe.going):
            sProbe.getStuff()
            time.sleep(1)
    

    @staticmethod
    def on_close():
        print('closing')
        sProbe.going = False

