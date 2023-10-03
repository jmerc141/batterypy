# batterypy
GUI for battery information from wmi (only on windows)

Requires wmi module
(pip install wmi)

Build:
windows:
  pyinstaller --onedir --windowed --add-data "res/*;res" main.py
linux:
  pyinstaller -F -w --add-data "res/*:res" main.py
