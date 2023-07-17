# main.py
import gui, probe, time
import threading

if __name__ == '__main__':
    app = gui.App()
    p = probe.Probe()
    #a = threading.Thread(target=p.refresh)
    #a.start()
    app.mainloop()
