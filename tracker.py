'''
 - Get linear regression line for predicted battery health
    and capacity loss (percentage) per month/year
 - Test with charging
 - Reset tracking when plugged in / out
 - 1 write every 10s = 1MB per hour
 - get % per hour
'''

import os, json, csv, settings, s_probe
from datetime import datetime


class Tracker(object):
    def __init__(self):
        self.headers = ['session_num','curtime','health_percent','probes_full_Wh','measured_Ah','measured_Wh',
                   'rem_Ah','rem_Wh','cap_diff','voltage','amps','watts','chrg_percent','charging']
        
        self.num_sessions = 0
        
        if os.path.exists(settings.s['filename']):
            self.num_sessions = self.readCsv()
            self.num_sessions += 1
        else:
            self.write_header()

        # List for writing info to history file
        self.history_data = []
        
        self.measured_Ah = 0
        self.measured_Wh = 0

        # Number of readings taken, increments every second
        self.readings = 0
        
        # Percentage of battery when tracking begins
        self.starting_percent = s_probe.sProbe.chargeRemaining
        
        # mWh reading when tracking begins
        self.starting_cap = s_probe.sProbe.capRemaining

        self.start_state = s_probe.sProbe.charging

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
    

    def track_norm(self):
        '''
            Method to track current mAh, must update every second for accurate reading
            Runs only when conditions are met
            Intended for automatic tracking in background (not used yet)
        '''
        # If charge percent changes by 5
        if (s_probe.sProbe.charging - self.starting_percent) > 2:
            self.readings += 1

            self.get_readings()

            # Write to history file every 10 seconds
            if self.readings == 10:
                # write to file
                self.write_history()
                self.readings = 0


    def track_man(self):
        '''
            Manually run from s_probe to get readings and write to file every 10 seconds
        '''
        if self.start_state != s_probe.sProbe.charging:
            self.num_sessions += 1
            self.start_state = s_probe.sProbe.chargerate
        self.readings += 1
        self.get_readings()
        if self.readings == 10:
            # 1KB per 10s
            self.write_csv()
            self.readings = 0
        

    '''
        Seperate function to populate the history_data dict, order matters with csv
    '''
    def get_readings(self):
        full_cap = s_probe.sProbe.fullChargeCap
        est_chrg = s_probe.sProbe.chargeRemaining
        rem_cap = s_probe.sProbe.capRemaining

        # How much Wh was gained / lost
        if s_probe.sProbe.charging:
            cap_diff = (rem_cap - self.starting_cap)
        else:
            cap_diff = (self.starting_cap - rem_cap)

        self.measured_Ah += s_probe.sProbe.amps * (1/3600)
        self.measured_Wh += s_probe.sProbe.watts * (1/3600)
        
        self.history_data.append([self.num_sessions, datetime.today().strftime('%Y-%m-%d|%H:%M:%S'), s_probe.sProbe.health,
                                  full_cap, self.measured_Ah, self.measured_Wh, round((rem_cap / s_probe.sProbe.voltage), 3),
                                  rem_cap, cap_diff, s_probe.sProbe.voltage, s_probe.sProbe.amps, s_probe.sProbe.watts, est_chrg, s_probe.sProbe.charging])
        

    def write_history(self):
        '''
            Write session list to history.json file as JSON (not used)
        '''
        with open(self.filename, 'w') as f:
            jsonobj = json.dump(self.sessions, f, indent=4)


    def write_header(self):
        '''
            Writes only the header to the history file
        '''
        with open(settings.s['filename'] ,'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(self.headers)


    def write_csv(self):
        '''
            Write header
        '''
        with open(settings.s['filename'], newline='', mode='a') as f:
            w = csv.writer(f)
            for h in self.history_data:
                w.writerow(h)
        self.history_data = []

        
    def clear_history(self):
        '''
            Delete history file
        '''
        os.remove(settings.s['filename'])
