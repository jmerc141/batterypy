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
pyinstaller --clean --onefile --windowed --icon=.\res\battery.ico --add-data "res/*;res" --name=batterypy main.py
```
### Linux:
```
pyinstaller --clean --onefile --windowed --add-data "res/*:res" --name=batterypy main.py
```
