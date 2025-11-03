import s_probe, time, keyboard, os

'''
    Adding this for slow computers
'''

going = True

def run():
    global going

    sp = s_probe.sProbe()
    sp.th.start()

    keyboard.on_press_key('q', quit)

    if os.name == 'nt':
        os.system('cls')
    # for Mac and Linux (posix)
    else:
        os.system('clear')

    while(going):
        term_w = os.get_terminal_size().columns - 30
        if term_w < 20:
            print('Not enough columns')
        else:
            try:
                print('\033[H', end='')
                v_bar = int((sp.voltage / term_w) * 100)
                a_bar = int((sp.amps / term_w) * 100)
                w_bar = int((sp.watts / term_w) * 100)
                h_bar = int((sp.get_health() / 100) * term_w)
                chrg  = int((sp.win32bat['EstimatedChargeRemaining'] / 100) * term_w)
                prnt_str = f'''Volts :{sp.voltage:6.3f} [{v_bar * '█'}{(term_w - v_bar) * '░'}]
Amps  :{sp.amps:6.3f} [{a_bar * '█'}{(term_w - a_bar) * '░'}]
Watts :{sp.watts:6.3f} [{w_bar * '█'}{(term_w - w_bar) * '░'}]
Health:{sp.get_health():5.2f}% [{h_bar * '█'}{(term_w - h_bar) * '░'}]({sp.msbatt['BatteryFullChargedCapacity']['FullChargedCapacity']}mah)
Charge:{sp.win32bat['EstimatedChargeRemaining']}%   [{chrg * '█'}{(term_w - chrg) * '░'}]'''
                print(prnt_str, end='')
                time.sleep(1)
            except KeyboardInterrupt as k:
                # Ctrl+c quit
                going = False
    print('\nclosing...')
    sp.on_close()


def quit(k):
    global going
    going = False
    
    