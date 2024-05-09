'''
Decide to add 'all' button to internal to show v, a, and w
'''
import gui, multiprocessing, sys

if __name__ == '__main__':
    # Necessary for windows multiprocessing and pyinstaller
    if sys.platform.startswith('win'):
        multiprocessing.freeze_support()
        
    app = gui.App('azure', 'dark')
    app.run()
