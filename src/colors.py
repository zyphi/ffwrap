import platform

is_win = platform.system() == 'Windows'


class Col:
    default = '\033[39m' if not is_win else ''
    header = '\033[95m' if not is_win else ''
    blue = '\033[94m' if not is_win else ''
    cyan = '\033[96m' if not is_win else ''
    green = '\033[92m' if not is_win else ''
    yellow = '\033[93m' if not is_win else ''
    warn = '\033[35m' if not is_win else ''
    fail = '\033[91m' if not is_win else ''
    bold = '\033[1m' if not is_win else ''
    underline = '\033[4m' if not is_win else ''
    endc = '\033[0m' if not is_win else ''
