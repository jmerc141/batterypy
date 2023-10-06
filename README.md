# batterypy
GUI for battery information (windows and linux)

## Requirements
```
Use pip or package manager to install:
wmi matplotlib tkinter
```
## Build:
### Windows:
```
pyinstaller --onefile --windowed --icon=.\res\battery.ico --add-data "res/*;res" main.py
```
### Linux:
```
pyinstaller --onefile --windowed --add-data "res/*:res" main.py
```
