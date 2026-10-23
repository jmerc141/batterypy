# batterypy
GUI for battery information (windows and linux)

## Requirements
```
Use pip or package manager to install requirements.txt
On linux make sure python-tk and idle3 are installed (apt)
```
## Build:
### Windows:
```
python -m PyInstaller --clean --onefile --windowed --icon=.\res\battery.ico --add-data "res/*;res" --name=batterypy --collect-data TKinterModernThemes main.py
```
### Linux:
```
python -m PyInstaller --clean --onefile --windowed --add-data "res/*:res" --name=batterypy --collect-data TKinterModernThemes main.py
```
(If using conda may need "conda install -c conda-forge libpython")
(Fonts may need "conda install -c conda-forge "tk=*=xft_*"")