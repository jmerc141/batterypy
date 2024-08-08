'''
Get linear regression line for predicted battery health
and capacity loss (percentage) per month/year
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

        if os.path.exists('history.dat'):
            print('history')
        else:
            print('new')
        
        
        self.history_data = {
            'date': '',
            'health_percent': 0,
            'measured_mAh': 0,
            'actual_mAh': 0
        }

        self.history_data['date'] = datetime.today().strftime('%Y-%m-%d')
        self.history_data['health_percent'] = self.probe.bathealth
        
        self.measured_mAh = 0
        self.readings = 0
        self.starting_percent = self.probe.est_chrg
    

    '''
        Method to track current mAh, must update every second for accurate reading
    '''
    def track_mAh(self):
        if (self.probe.est_chrg - self.starting_percent) > 5:
            self.readings += 1
            self.measured_mAh += self.probe.amps * (1/3600)
            self.history_data['actual_mAh'] = self.probe.full_cap
            self.history_data['measured_mAh'] = self.measured_mAh
            jsonobj = json.dumps(self.history_data, indent=4)
            with open('hitory.dat', 'w') as out:
                out.write(jsonobj)
            


    

