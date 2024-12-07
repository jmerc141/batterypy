'''
 - Get linear regression line for predicted battery health
and capacity loss (percentage) per month/year
 - Test with charging
 - Reset tracking when plugged in / out
 - 1 write every 10s = 1MB per hour
 - Rewrite json.dumps to handle multiple sessions
 - get % per hour
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
        self.readings +=1
        self.get_readings()
        if self.readings == 10:
            self.write_history()
            
            self.readings = 0
        #print(json.dumps(self.history_data, indent=4))
        #print()
        
    '''
        Stops writing JSON to file, checks for ending bracket
        and adds one if needed
    '''
    def end_tracking(self):
        with open('history.dat', 'rb') as r:
            r.seek(-1, 2)
            if not r.read(1).decode() == ']':
                with open('history.dat', 'a') as f:
                    f.write(']')

    '''
        Seperate function to populate the history_data dict
    '''
    def get_readings(self):
        # Get current time and add a new dict to history_data with time as key
        curtime = datetime.today().strftime('%Y-%m-%d|%H:%M:%S')
        self.history_data[curtime] = {}

        self.history_data[curtime]['health_percent'] = round(self.probe.bathealth, 3)
        self.history_data[curtime]['rem_mAh'] = (self.probe.rem_cap / self.probe.voltage)
        # Get mAh every second
        self.history_data[curtime]['measured_mAh'] = round(self.probe.amps * (1/3600), 3)
        
        # Last measured full charged battery capacity
        self.history_data[curtime]['probes_full_mWh'] = self.probe.full_cap
        # Manually measure mWh used or charged
        self.history_data[curtime]['measured_mWh'] = round(self.probe.watts * (1/3600), 3)

        # If discharging starting_cap - rem_cap,
        # if charging rem_cap - starting_cap to get laptops measured mWh difference
        self.history_data[curtime]['rem_mWh'] = self.probe.rem_cap

        if self.probe.charging:
            self.history_data[curtime]['cap_diff'] = self.probe.rem_cap - self.starting_cap
        else:
            self.history_data[curtime]['cap_diff'] = self.starting_cap - self.probe.rem_cap

        self.history_data[curtime]['voltage'] = self.probe.voltage

        self.history_data[curtime]['chrg_percent'] = self.probe.est_chrg

            
    '''
        Write history_data dict to history.dat file as JSON
        Possibly empty history_data here so we dont have to rewrite entire file
    '''
    def write_history(self):
        with open('history.dat', 'a') as f:
            # If the file is empty, write the opening bracket for the JSON array
            if f.tell() == 0:
                f.write("[")
            else:
                # Add a comma before appending the new object, unless it's the first entry
                f.write(",\n")

            jsonobj = json.dump(self.history_data, f, indent=4)
        
        # Reset history_data
        self.history_data = {}
            
