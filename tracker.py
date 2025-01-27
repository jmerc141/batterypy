'''
 - Get linear regression line for predicted battery health
    and capacity loss (percentage) per month/year
 - Test with charging
 - Reset tracking when plugged in / out
 - 1 write every 10s = 1MB per hour
 - get % per hour
'''

import sys, os, json, csv, settings
from datetime import datetime

class Tracker(object):
    def __init__(self):

        if sys.platform == 'linux':
            import s_probe_l
            self.probe = s_probe_l.sProbe
        elif sys.platform == 'win32':
            import s_probe
            self.probe = s_probe.sProbe

        self.headers = ['session_num','curtime','health_percent','probes_full_Wh','measured_Ah','measured_Wh',
                   'rem_Ah','rem_Wh','cap_diff','voltage','amps','watts','chrg_percent','charging']
        
        self.num_sessions = 0
        
        # Write headers to new file
        if os.path.exists(settings.s['filename']):
            self.num_sessions = self.readCsv()
            self.num_sessions += 1
        else:
            with open(settings.s['filename'], newline='', mode='w') as f:
                writer = csv.writer(f)
                writer.writerow(self.headers)
        
        #self.sessions.append([])

        # List for writing info to history file
        self.history_data = []
        
        self.measured_Ah = 0
        self.measured_Wh = 0

        # Number of readings taken, increments every second
        self.readings = 0
        
        # Percentage of battery when tracking begins
        self.starting_percent = s_probe.sProbe.win32bat['EstimatedChargeRemaining']
        
        # mWh reading when tracking begins
        self.starting_cap = s_probe.sProbe.msbatt['BatteryStatus']['RemainingCapacity']

        self.start_state = s_probe.sProbe.msbatt['BatteryStatus']['Charging']

        self.tmp_data = []


    '''
        Read csv file on startup to get the number of sessions
    '''
    def readCsv(self):
        session_count = []
        with open(settings.s['filename']) as f:
            csvFile = csv.reader(f)
            # Skip header
            next(csvFile, None)
            for l in csvFile:
                session_count.append(l[0])
        
        if len(session_count) > 0:
            return int(max(session_count))
        else:
            return 0
    

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
        # if unplugged or plugged in, create a new session
        print(self.start_state)
        if self.start_state != self.probe.msbatt['BatteryStatus']['Charging']:
            self.num_sessions += 1
            self.start_state = self.probe.chargerate
        self.readings += 1
        self.get_readings()
        if self.readings == 10:
            #self.write_history()
            self.write_csv()
            self.readings = 0
        

    '''
        Seperate function to populate the history_data dict, order matters with csv
    '''
    def get_readings(self):
        full_cap = self.probe.msbatt['BatteryFullChargedCapacity']['FullChargedCapacity'] / 1000
        est_chrg = self.probe.win32bat['EstimatedChargeRemaining']
        rem_cap = self.probe.msbatt['BatteryStatus']['RemainingCapacity'] / 1000

        # How much Wh was gained / lost
        if self.probe.msbatt['BatteryStatus']['Charging']:
            cap_diff = (rem_cap - self.starting_cap)
        else:
            cap_diff = (self.starting_cap - rem_cap)

        self.measured_Ah += self.probe.amps * (1/3600)
        self.measured_Wh += self.probe.watts * (1/3600)
        
        self.history_data.append([self.num_sessions, datetime.today().strftime('%Y-%m-%d|%H:%M:%S'), round(self.probe.get_health(), 3),
                                  full_cap, self.measured_Ah, self.measured_Wh, round((rem_cap / self.probe.voltage), 3),
                                  rem_cap, cap_diff, self.probe.voltage, self.probe.amps, self.probe.watts, est_chrg, self.probe.msbatt['BatteryStatus']['Charging']])
        


    '''
        Write session list to history.json file as JSON
    '''
    def write_history(self):
        with open(self.filename, 'w') as f:
            jsonobj = json.dump(self.sessions, f, indent=4)


    '''
        Write header
    '''
    def write_csv(self):
        with open(settings.s['filename'], newline='', mode='a') as f:
            w = csv.writer(f)
            for h in self.history_data:
                w.writerow(h)
        self.history_data = []

        
    '''
    
    '''
    def clear_history(self):
        os.remove(self.filename)
