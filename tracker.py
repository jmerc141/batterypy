'''
 - Get linear regression line for predicted battery health
    and capacity loss (percentage) per month/year
 - Test with charging
 - Reset tracking when plugged in / out
 - 1 write every 10s = 1MB per hour
 - Rewrite json.dumps to handle multiple sessions
 - get % per hour
 - add charging / discharging status
'''

import sys, os, json
from datetime import datetime

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
            with open('history.dat', 'r') as r:
                self.sessions = json.load(r)
                self.num_sessions = len(self.sessions)
        else:
            # Make a new history.dat file
            print('new')
            # List of charging sessions, holds history_data
            self.sessions = []

            # Total number of sessions
            self.num_sessions = 0

        self.sessions.append([])

        # Dict for writing info to history file
        self.history_data = {}
        
        self.history_data['measured_Ah'] = 0
        self.history_data['measured_Wh'] = 0

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


    '''
    
    '''
    def track_man(self):
        self.readings +=1
        self.get_readings()
        if self.readings == 10:
            self.write_history()
            
            self.readings = 0
        
        
    '''
        Stops writing JSON to file, checks for ending bracket
        and adds one if needed
    '''
    def end_tracking(self):
        #with open('history.dat', 'rb') as r:
        #    r.seek(-1, 2)
        #    if not r.read(1).decode() == ']':
        #        with open('history.dat', 'a') as f:
        #            f.write(']')
        pass


    '''
        Seperate function to populate the history_data dict
    '''
    def get_readings(self):
        # Get current time and add a new dict to history_data with time as key
        curtime = datetime.today().strftime('%Y-%m-%d|%H:%M:%S')
        #self.sessions
        self.history_data['curtime'] = curtime
        # This probably wont change in a single session
        self.history_data['health_percent'] = round(self.probe.bathealth, 3)
        
        # Last measured full charged battery capacity
        self.history_data['probes_full_Wh'] = self.probe.full_cap / 1000
        
        # Get mAh every second
        self.history_data['measured_Ah'] += self.probe.amps * (1/3600)

        # Manually measure mWh used or charged
        self.history_data['measured_Wh'] += self.probe.watts * (1/3600)

        # Remaining amp hour given by the system
        self.history_data['rem_Ah'] = round((self.probe.rem_cap / self.probe.voltage) / 1000, 3)

        # Remaining watt hour given by the system
        self.history_data['rem_Wh'] = self.probe.rem_cap / 1000

        # The difference between the remaining cap of the system and the starting 
        # cap when tracking started in Wh
        # Essentially how many Wh were spent / gained
        if self.probe.charging:
            self.history_data['cap_diff'] = (self.probe.rem_cap - self.starting_cap) / 1000
        else:
            self.history_data['cap_diff'] = self.starting_cap - (-self.probe.rem_cap)

        self.history_data['voltage'] = self.probe.voltage

        self.history_data['amps'] = self.probe.amps

        self.history_data['watts'] = self.probe.watts

        self.history_data['chrg_percent'] = self.probe.est_chrg

        # Add history data to only the session
        self.sessions[self.num_sessions].append(self.history_data)


    '''
        Write history_data dict to history.dat file as JSON
    '''
    def write_history(self):
        with open('history.dat', 'w') as f:
            jsonobj = json.dump(self.sessions, f, indent=4)

        # Reset history_data
        self.history_data = {}
        self.history_data['measured_Ah'] = 0
        self.history_data['measured_Wh'] = 0
            
