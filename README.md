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
pyinstaller --onedir --windowed --add-data "res/*;res" main.py
```
### Linux:
```
pyinstaller -F -w --add-data "res/*:res" main.py
```
