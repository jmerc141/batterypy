# main.py
import gui, probe, time, multiprocessing, sys

if __name__ == '__main__':
    # Necessary for windows multiprocessing
    if sys.platform.startswith('win'):
        multiprocessing.freeze_support()
    app = gui.App()
    app.mainloop()
