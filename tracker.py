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
                   'rem_Ah','rem_Wh','cap_diff','voltage','amps','watts','chrg_percent']
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

        # Dict for writing info to history file
        self.history_data = []
        
        self.measured_Ah = 0
        self.measured_Wh = 0

        # Number of readings taken, increments every second
        self.readings = 0
        
        # Percentage of battery when tracking begins
        self.starting_percent = self.probe.est_chrg
        
        # mWh reading when tracking begins
        self.starting_cap = self.probe.rem_cap

        self.start_state = s_probe.sProbe.charging

        self.tmp_data = []
    

    def readJson(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as r:
                self.sessions = json.load(r)
                self.num_sessions = len(self.sessions)
        else:
            # List of charging sessions, holds history_data
            self.sessions = []

            # Total number of sessions
            self.num_sessions = 0


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
        if self.start_state != self.probe.charging:
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
        '''
        self.history_data['session_num'] = self.num_sessions

        self.history_data['curtime'] = datetime.today().strftime('%Y-%m-%d|%H:%M:%S')
        
        # This probably wont change in a single session
        self.history_data['health_percent'] = round(self.probe.bathealth, 3)
        
        # Last measured full charged battery capacity
        self.history_data['probes_full_Wh'] = self.probe.full_cap / 1000
        
        # Get mAh every second
        self.measured_Ah += self.probe.amps * (1/3600)
        self.history_data['measured_Ah'] = self.measured_Ah

        # Manually measure mWh used or charged
        self.measured_Wh += self.probe.watts * (1/3600)
        self.history_data['measured_Wh'] = self.measured_Wh

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
            self.history_data['cap_diff'] = (self.starting_cap - (-self.probe.rem_cap)) / 1000

        self.history_data['voltage'] = self.probe.voltage

        self.history_data['amps'] = self.probe.amps

        self.history_data['watts'] = self.probe.watts

        self.history_data['chrg_percent'] = self.probe.est_chrg
        '''

        self.measured_Ah += self.probe.amps * (1/3600)
        self.measured_Wh += self.probe.watts * (1/3600)

        # The difference between the remaining cap of the system and the starting 
        # cap when tracking started in Wh
        # Essentially how many Wh were spent / gained
        if self.probe.charging:
            self.cap_diff = (self.probe.rem_cap - self.starting_cap) / 1000
        else:
            self.cap_diff = (self.starting_cap - (-self.probe.rem_cap)) / 1000
        
        self.history_data.append([self.num_sessions, datetime.today().strftime('%Y-%m-%d|%H:%M:%S'), round(self.probe.bathealth, 3),
                                  self.probe.full_cap / 1000, self.measured_Ah, self.measured_Wh, round((self.probe.rem_cap / self.probe.voltage) / 1000, 3),
                                  self.probe.rem_cap / 1000, self.cap_diff, self.probe.voltage, self.probe.amps, self.probe.watts, self.probe.est_chrg])
        
        #self.tmp_data.append(self.history_data)

        # Reset dict
        #self.history_data = []


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
