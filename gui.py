import sys, time
import tkinter as tk
from tkinter import ttk
import probe

sys.path.append(".")

'''
wmi seems to update every 3 seconds
'''


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        # Probe object reference
        self.p = probe.Probe()
        # creating tkinter window
        self.title('BatteryInfo')
        self.geometry('800x700')

        # initialize tree view
        self.tree = ttk.Treeview(self, columns=('val', 'max'), height=20)
        self.tree.insert('', 'end', 'system', text='System Name', values=(self.p.win.systemname, ''), open=True)
        self.tree.insert('system', 0, 'name', text='Name', values=(self.p.win.name, ''))
        self.tree.insert('system', 'end', text='Status', values=(self.p.win.status, ''))
        self.tree.insert('system', 'end', 'chargepercent', text='Charge Percent',
                         values=(str(self.p.win.estimatedchargeremaining) + ' %', ''))
        self.tree.insert('system', 'end', 'timerem', text='Time Remaining',
                         values=(str(self.p.hours) + 'h ' + str(self.p.minutes) + 'm ', ''))
        if self.p.charging:
            self.tree.insert('power', 'end', 'chargepower', text='Charge Power',
                             values=(str(self.p.chargerate) + ' W', ''))
            self.tree.insert('timerem', 'end', 'rechargetime', text='Max Recharge Time',
                             values=(str(self.p.rehours) + 'h ' + str(self.p.remins) + 'm', ''))
            self.tree.insert('timerem', 'end', 'ttf', text='Time to Full Charge', values=(str(self.p.ttfhours) + 'h ' + str(self.p.ttfmins) + 'm', ''))

        self.tree.insert('system', 'end', 'power', text='Power', open=True)
        self.tree.insert('power', 'end', 'dpower', text='Discharge Power',
                         values=(str(self.p.dischargerate) + ' W', ''))
        self.tree.insert('power', 'end', 'amps', text='Amperage', values=(str(self.p.amps) + ' A', ''))

        self.tree.insert('system', 'end', 'v', text='Voltage', open=True)
        self.tree.insert('v', 'end', 'voltnow', text='Voltage', values=(str(self.p.voltage) + ' V', ''))
        self.tree.insert('v', 'end', 'desvolt', text='Design Voltage',
                         values=(str(int(self.p.win.designvoltage) / 1000) + ' V', ''))

        self.tree.insert('system', 'end', 'capacity', text='Capacity', open=True)
        self.tree.insert('capacity', 'end', 'descap', text='Design Capacity', values=(str(self.p.descap) + ' Wh', ''))
        self.tree.insert('capacity', 'end', 'fullcap', text='Full Charge Capacity',
                         values=(str(self.p.fullcap) + ' Wh', ''))
        self.tree.insert('capacity', 'end', 'bathealth', text='Battery Health',
                         values=(str(self.p.bathealth) + ' %', ''))

        # extra info
        self.tree.insert('system', 'end', 'info', text='Extra Info', open=True)
        self.tree.insert('info', 'end', text='Cycle Count', values=(self.p.cyclecount, ''))
        self.tree.insert('info', 'end', text='Temperature', values=(self.p.temp, ''))
        self.tree.insert('info', 'end', 'caption', text='Caption', values=(self.p.win.caption, ''))
        self.tree.insert('info', 'end', 'desc', text='Description', values=(self.p.win.description, ''))
        self.tree.insert('info', 'end', 'avail', text='Availability', values=(self.p.avail, ''))
        self.tree.insert('info', 'end', 'batstat', text='Battery Status', values=(self.p.batstat, ''))
        self.tree.insert('info', 'end', 'chem', text='Chemistry', values=(self.p.chem, ''))
        self.tree.insert('info', 'end', text='Error Description', values=(self.p.win.ErrorDescription, ''))
        self.tree.insert('info', 'end', text='Power Management Capabilities', values=(self.p.pmc, ''))

        # column headings
        self.tree.heading('#0', text='Property', anchor=tk.CENTER)
        self.tree.column('#0', width=200, stretch=tk.YES)

        self.tree.heading('0', text='Value')
        self.tree.column('0', width=150)

        self.tree.heading('1', text='Max')
        self.tree.column('1', width=150)

        self.tree.pack(fill=tk.BOTH, side=tk.LEFT, padx=10, pady=10)

        btn = tk.Button(self, text='Start', command=self.retree)
        btn.pack(side=tk.LEFT)

        self.pb = ttk.Progressbar(self, orient='horizontal', mode='determinate', length=100)
        self.pb.pack(side=tk.LEFT)

    def retree(self):
        # overwrites values in the treeview, use only dynamic values
        self.pb['value'] += 10
        self.p.refresh()  # refreshes instance and updates variables
        self.tree.set('dpower', 'val', str(self.p.dischargerate) + ' W')
        self.tree.set('timerem', 'val', str(str(self.p.hours) + 'h ' + str(self.p.minutes) + 'm'))
        self.tree.set('batstat', 'val', self.p.batstat)
        self.tree.set('voltnow', 'val', str(self.p.voltage) + ' V')
        self.tree.set('avail', 'val', self.p.avail)
        self.tree.set('amps', 'val', str(self.p.amps) + ' A')
        if self.p.charging:
            self.tree.set('chargepower', 'val', str(self.p.chargerate) + ' W')
            self.tree.set('ttf', 'val', str(str(self.p.ttfhours) + 'h ' + str(self.p.ttfmins) + 'm'))
            self.tree.set('rechargetime', 'val', str(str(self.p.rehours) + 'h ' + str(self.p.remins) + 'm'))
        self.tree.set('chargepercent', 'val', str(self.p.win.estimatedchargeremaining) + ' %')
        # full charge cap?
        # error description


if __name__ == '__main__':
    app = App()
    app.mainloop()
