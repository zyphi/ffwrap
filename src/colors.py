import platform


class Col:
    default = ''
    header = ''
    blue = ''
    cyan = ''
    green = ''
    yellow = ''
    warn = ''
    fail = ''
    bold = ''
    underline = ''
    endc = ''


is_win = platform.system() == 'Windows'
if is_win:
    try:
        from colorama import init, Fore
        init()

        Col.default = Fore.RESET
        Col.header = Fore.LIGHTMAGENTA_EX
        Col.blue = Fore.LIGHTBLUE_EX
        Col.cyan = Fore.LIGHTCYAN_EX
        Col.green = Fore.LIGHTGREEN_EX
        Col.yellow = Fore.LIGHTYELLOW_EX
        Col.warn = Fore.LIGHTMAGENTA_EX
        Col.fail = Fore.LIGHTRED_EX
        Col.endc = Fore.RESET
    except:
        print('colorama not installed, using default colors')

else:
    Col.default = '\033[39m'
    Col.header = '\033[95m'
    Col.blue = '\033[94m'
    Col.cyan = '\033[96m'
    Col.green = '\033[92m'
    Col.yellow = '\033[93m'
    Col.warn = '\033[35m'
    Col.fail = '\033[91m'
    Col.bold = '\033[1m'
    Col.underline = '\033[4m'
    Col.endc = '\033[0m'
