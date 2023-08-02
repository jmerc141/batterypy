# batterypy
Get battery information from wmi (only on windows)

Requires wmi module
(pip install wmi)

Build:
pyinstaller --onedir --windowed --add-data "res/*;res" main.py