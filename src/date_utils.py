from datetime import datetime, timedelta
from .custom_types import DateResult


def format_query_date(date: str) -> DateResult:
    try:
        if date == 't':
            return True, datetime.now().strftime('%Y-%m-%d 00:00:00')
        if date == 'y':
            return True, (datetime.now() -
                          timedelta(days=1)).strftime('%Y-%m-%d 00:00:00')
        if date == 'n':
            return True, datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        _ = int(date)
        __ = date[7]
        return True, f'{date[:4]}-{date[4:6]}-{date[6:8]} 00:00:00'
    except:
        return False, ''
