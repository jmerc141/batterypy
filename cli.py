import s_probe, time, os, pynput, shutil

'''
    Adding this for slow computers
'''

going = True

def run():
    global going

    if os.name == 'nt':
        os.system('cls')
        # For old terminals to interpret ANSI codes
        import colorama
        colorama.init()
        s_probe.sProbe.activate()
        s_probe.sProbe.th.start()
    # for Mac and Linux (posix)
    else:
        
        #os.system('clear')
        s_probe.sProbe.activate_l()
        s_probe.sProbe.th.start()

    RED = '\033[38;5;57m'
    END  ='\033[0m'

    with pynput.keyboard.Listener(on_press=quit) as listener:
        while(going):
            term_w = shutil.get_terminal_size().columns - 30
            if term_w < 20:
                print('Not enough columns')
            else:
                try:
                    #print('\033[H', end='')
                    v_bar = int((s_probe.sProbe.voltage / term_w) * 100)
                    a_bar = int((s_probe.sProbe.amps / term_w) * 100)
                    w_bar = int((s_probe.sProbe.watts / term_w) * 100) if s_probe.sProbe.watts < term_w else term_w
                    # Percents
                    h_bar = int((s_probe.sProbe.health / 100) * term_w)
                    chrg  = int((s_probe.sProbe.chargeRemaining / 100) * term_w)

                    prnt_str = f'''\033[HVolts :{s_probe.sProbe.voltage:6.3f} [{RED}{v_bar * '█'}{(term_w - v_bar) * '░'}{END}]
Amps  :{s_probe.sProbe.amps:6.3f} [{a_bar * '█'}{(term_w - a_bar) * '░'}]
Watts :{s_probe.sProbe.watts:6.3f} [{w_bar * '█'}{(term_w - w_bar) * '░'}]
Health:{s_probe.sProbe.health:5.1f}% [{h_bar * '█'}{(term_w - h_bar) * '░'}]({s_probe.sProbe.fullChargeCap}mah)
Charge:{s_probe.sProbe.chargeRemaining:5.1f}% [{chrg * '█'}{(term_w - chrg) * '░'}]'''
                    
                    print(prnt_str, end='')

                    time.sleep(1)
                except KeyboardInterrupt as k:
                    # Ctrl+c quit
                    going = False

        if going:
            listener.join()

    print('\nclosing...')
    s_probe.sProbe.on_close()


def quit(k):
    try:
        if k.char == 'q':
            #print('here')
            global going
            going = False
            return False
    except AttributeError as a:
        # Non character key pressed
        pass
    
    