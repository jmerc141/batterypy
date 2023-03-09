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
        self.geometry('600x700')
        frame = ttk.Frame(self)

        frame['padding'] = (5, 10, 5, 10)
        frame['borderwidth'] = 5
        # frame['relief'] = 'sunken'

        frame.pack(anchor='w')

        label = tk.Label(frame, text='Text here')
        label.pack(anchor='w')

        # stringvars
        # self.strtimerem = tk.StringVar(value=(self.p.runtime))
        # self.strtimerem.trace('w', callback=self.retree)
        chem = ''

        # initialize tree view
        self.tree = ttk.Treeview(frame, columns=('val', 'max'), height=20)
        self.tree.insert('', 'end', 'system', text='System Name', values=(self.p.win.systemname, ''), open=True)
        self.tree.insert('system', 0, 'name', text='Name', values=(self.p.win.name, ''))
        self.tree.insert('system', 1, 'cap', text='Caption', values=(self.p.win.caption, ''))
        self.tree.insert('system', 2, 'desc', text='Description', values=(self.p.win.description, ''))
        self.tree.insert('system', 3, 'avail', text='Availability', values=(self.p.win.availability, ''))
        self.tree.insert('system', 4, 'batstat', text='Battery Status', values=(self.p.win.batterystatus, ''))

        if self.p.win.chemistry == 1:
            chem = 'Other'
        elif self.p.win.chemistry == 2:
            chem = 'Unknown'
        elif self.p.win.chemistry == 3:
            chem = 'Lead Acid'
        elif self.p.win.chemistry == 4:
            chem = 'Nickel Cadmium'
        elif self.p.win.chemistry == 5:
            chem = 'Nickel Metal Hydride'
        elif self.p.win.chemistry == 6:
            chem = 'Lithium-ion'
        elif self.p.win.chemistry == 7:
            chem = 'Zinc air'
        elif self.p.win.chemistry == 8:
            chem = 'Lithium Polymer'

        self.tree.insert('system', 5, 'chem', text='Chemistry', values=(chem, ''))
        self.tree.insert('system', 6, 'timerem', text='Time Remaining', values=(str(self.p.hours)
                                                                                + 'h ' + str(self.p.minutes) + 'm ', ''))
        self.tree.insert('system', 8, 'v', text='Voltage', open=True)
        self.tree.insert('v', 'end', 'voltnow', text='Voltage', values=(self.p.voltage, ''))
        self.tree.insert('v', 'end', 'desvolt', text='Design Voltage', values=(self.p.win.designvoltage, ''))
        self.tree.insert('system', 9, 'dpower', text='Discharge Power', values=(str(self.p.dischargerate) + ' W', ''))

        self.tree.heading('#0', text='first')
        self.tree.column('#0', width=200)

        self.tree.heading('0', text='Value')
        self.tree.column('0', width=150)

        self.tree.heading('1', text='Max')
        self.tree.column('1', width=150)

        self.tree.pack()

        btn = tk.Button(self, text='Start', command=self.retree)
        btn.pack()

        self.pb = ttk.Progressbar(self, orient='horizontal', mode='determinate', length=100)
        self.pb.pack()


    def retree(self):
        # only dynamic values
        self.pb['value'] += 10
        self.p.refresh()
        self.tree.set('dpower', 'val', str(self.p.dischargerate) + ' W')
        self.tree.set('timerem', 'val', str(str(self.p.hours) + 'h ' + str(self.p.minutes) + 'm '))
        self.tree.set('batstat', 'val', self.p.win.batterystatus)
        self.tree.set('voltnow', 'val', self.p.voltage)


if __name__ == '__main__':
    app = App()
    app.mainloop()
