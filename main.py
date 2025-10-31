'''
Decide to add 'all' button to internal to show v, a, and w
'''
import multiprocessing, sys, gui, cli

if __name__ == '__main__':
    # Necessary for windows multiprocessing and pyinstaller
    if sys.platform.startswith('win'):
        multiprocessing.freeze_support()
    
    if len(sys.argv) > 1 and sys.argv[1] == 'cli':
        cli.run()
    else:    
        app = gui.App('azure', 'dark')
        app.run()
