from datetime import timedelta


def format_timedelta(td: timedelta) -> str:
    return str(td).split('.')[0]
