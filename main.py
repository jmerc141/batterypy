import multiprocessing, sys

if __name__ == '__main__':
    # Necessary for windows multiprocessing and pyinstaller
    if sys.platform.startswith('win'):
        multiprocessing.freeze_support()
    
    if len(sys.argv) > 1 and sys.argv[1] == 'cli':
        import cli
        cli.run()
    else:
        import gui
        app = gui.App('azure', 'dark')
        app.run()
