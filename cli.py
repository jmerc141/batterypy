import s_probe, time

'''
    Adding this for slow computers

█ 	Full block
U+2589 	▉ 	Left seven eighths block
U+258A 	▊ 	Left three quarters block
U+258B 	▋ 	Left five eighths block
U+258C 	▌ 	Left half block
U+258D 	▍ 	Left three eighths block
U+258E 	▎ 	Left one quarter block
U+258F 	▏ 
'''

going = True

def run():
    global going
    sp = s_probe.sProbe()
    sp.th.start()
    while(going):
        try:
            print(f'{sp.amps}')
            time.sleep(1)
        except KeyboardInterrupt as k:

            print('here')
            going = False
    print('closing')
    sp.on_close()

