import s_probe, time, os, pynput, shutil

'''
    Adding this for slow computers
    TODO: fix newline for linux
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

    # On termnials that support 256 colors
    RED  = '\033[38;5;160m'
    DRED = '\033[38;5;52m'
    BLU  = '\033[38;5;21m'
    DBLU = '\033[38;5;17m'
    YEL  = '\033[38;5;220m'
    DYEL = '\033[38;5;3m'
    PURP = '\033[38;5;91m'
    DPUR = '\033[38;5;53m'
    GREY = '\033[38;5;230m'
    DGRY = '\033[38;5;235m'
    END  = '\033[0m'

    with pynput.keyboard.Listener(on_press=quit) as listener:
        maxv = 0
        maxa = 0
        maxw = 0
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
                    
                    '''
                    Add static data before (fullchargecap, chemistry, etc...)
                    '''

                    prnt_str = f'''\033[HName:                   {s_probe.sProbe.deviceName} {s_probe.sProbe.serial_num}
Manufacturer:           {s_probe.sProbe.manufName}
Chemistry:              {s_probe.sProbe.chemistry}
Last measured capacity: {s_probe.sProbe.fullChargeCap}mWh
Cycle count:            {s_probe.sProbe.cycleCount}
Status:                 {s_probe.sProbe.statusString}
{GREY}C{END}harge:{s_probe.sProbe.chargeRemaining:5.1f}% [{GREY}{chrg * '█'}{DGRY}{(term_w - chrg) * '█'}{END}]
{RED}V{END}olts :{s_probe.sProbe.voltage:6.3f} [{RED}{v_bar * '█'}{DRED}{(term_w - v_bar) * '█'}{END}] {maxv}
{BLU}A{END}mps  :{s_probe.sProbe.amps:6.3f} [{BLU}{a_bar * '█'}{DBLU}{(term_w - a_bar) * '█'}{END}] {maxa}
{YEL}W{END}atts :{s_probe.sProbe.watts:6.3f} [{YEL}{w_bar * '█'}{DYEL}{(term_w - w_bar) * '█'}{END}] {maxw}
{PURP}H{END}ealth:{s_probe.sProbe.health:5.1f}% [{PURP}{h_bar * '█'}{DPUR}{(term_w - h_bar) * '█'}{END}] {'' if s_probe.sProbe.health > 80 else '< 80% BAD!'}'''
                    
                    print(prnt_str, end='')
                    
                    if maxv < s_probe.sProbe.voltage:
                        maxv = s_probe.sProbe.voltage
                    if maxa < s_probe.sProbe.amps:
                        maxa = s_probe.sProbe.amps
                    if maxw < s_probe.sProbe.watts:
                        maxw = s_probe.sProbe.watts

                    time.sleep(1)
                except KeyboardInterrupt as k:
                    # Ctrl+c quit
                    going = False

        if going:
            listener.join()

    print('\nclosing...')
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')
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
    
    