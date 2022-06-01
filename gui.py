import sys, time
import tkinter as tk
from tkinter.ttk import *
sys.path.append(".")
from batt import battInfo

'''
wmi seems to update every 3 seconds
'''

# creating tkinter window
root = tk.Tk()
root.title('BatteryInfo')
root.geometry('200x200')
frame = Frame(root)
rightText = Frame(root)
leftText = Frame(root)

frame['padding'] = (5,10,5,10)
frame['borderwidth'] = 5
frame['relief'] = 'sunken'

mybatts = battInfo()
mybatts.create()

bats = tk.StringVar(root)
bats.set('empty')

frame.pack()

label = tk.Label(frame, text='Text here')

height = 5
width = 2
x = 0
for i in range(height): #Rows
    for j in range(width): #Columns
        if(x==0):
            b = tk.Label(frame, text="sample", bg='blue')
            x=1
            #print(x)
        else:
            b = Label(frame, text="sample")
            x=0
        b.grid(row=i, column=j)
'''
def find_grid(frame, row, column):
    for children in frame.children.values():
        info = children.grid_info()
        print(info)
        #note that rows and column numbers are stored as string                                                                         
        if info['row'] == str(row) and info['column'] == str(column):
            return children
    return None

find_grid(frame, i+1, j).get()
'''

def adj():
    mybatts.update(1)
    print(mybatts.val[1].getter('DesignVoltage'))



Button(root, text = 'Start', command = adj).pack(pady=10)

# infinite loop
tk.mainloop()