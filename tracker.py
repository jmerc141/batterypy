'''
Get linear regression line for predicted battery health
and capacity loss (percentage) per month/year
Test with charging
Reset tracking when plugged in / out
'''

import sys, os, json, time
from datetime import datetime
from threading import Thread

class Tracker(object):
    def __init__(self):

        if sys.platform == 'linux':
            import s_probe_l
            self.probe = s_probe_l.sProbe
        elif sys.platform == 'win32':
            import s_probe
            self.probe = s_probe.sProbe

        # If the history file exists, do not create a new one
        if os.path.exists('history.dat'):
            print('history')
        else:
            # Make a new history.dat file
            print('new')
        
        # Get time for key dict
        curtime = datetime.today().strftime('%Y-%m-%d|%H:%M:%S')
        
        # Dict for writing info to history file
        self.history_data = {}
        
        # Calculated value of mWh (watts * seconds)
        self.measured_mWh = 0
        # Number of readings taken, increments every second
        self.readings = 0
        # Value for when to write to history file
        self.write_now = 0
        # Percentage of battery when tracking begins
        self.starting_percent = self.probe.est_chrg
        # mWh reading when tracking begins
        self.starting_cap = self.probe.rem_cap

        
        
    
    '''
    Method to track current mAh, must update every second for accurate reading
    Runs only when conditions are met
    '''
    def track_norm(self):
        # If charge percent changes by 5
        if (self.probe.est_chrg - self.starting_percent) > 2:
            self.readings += 1

            self.get_readings()

            # Write to history file every 10 seconds
            if self.readings == 10:

                # write to file
                self.write_history()
                self.readings = 0


    def track_man(self):
        #self.readings +=1
        
        #if self.readings == 10:
        self.get_readings()
        #self.write_history()
        #self.readings = 0
        print(json.dumps(self.history_data, indent=4))
        print()
        


    '''
        Seperate function to populate the history_data dict
    '''
    def get_readings(self):
        # Get current time and add a new dict to history_data with time as key
        curtime = datetime.today().strftime('%Y-%m-%d|%H:%M:%S')
        self.history_data[curtime] = {}

        self.history_data[curtime]['health_percent'] = round(self.probe.bathealth, 3)
        self.history_data[curtime]['actual_mAh'] = (self.probe.rem_cap / self.probe.voltage)
        self.history_data[curtime]['measured_mAh'] = self.probe.amps * (1/3600)

        # Manually measure mWh
        self.measured_mWh += self.probe.watts * (1/3600)
        # Last measured full charged battery capacity
        self.history_data[curtime]['probes_full_mWh'] = self.probe.full_cap
        self.history_data[curtime]['measured_mWh'] = self.measured_mWh

        # If discharging starting_cap - rem_cap,
        # if charging rem_cap - starting_cap to get laptops measured mWh difference
        self.history_data[curtime]['rem_mWh'] = self.probe.rem_cap

        self.history_data[curtime]['cap_diff'] = self.probe.rem_cap - self.starting_cap

        self.history_data[curtime]['voltage'] = self.probe.voltage

        self.history_data[curtime]['chrg_percent'] = self.probe.est_chrg

            
    '''
        Write history_data dict to history.dat file as JSON
        Possibly empty history_data here so we dont have to rewrite entire file
    '''
    def write_history(self):
        jsonobj = json.dumps(self.history_data, indent=4)
        with open('history.dat', 'a') as out:
            out.write(jsonobj)
            


    

