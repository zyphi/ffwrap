import argparse
from src.database import Database

VERSION = '1.0.1'

parser = argparse.ArgumentParser(
    prog='ffquery',
    description='find stuff in ffwrap\'s database'
)

parser.add_argument(
    '-R',
    help='reset database',
    action='store_true'
)

parser.add_argument(
    '-S',
    help='show successful entries',
    action='store_true'
)

parser.add_argument(
    '-F',
    help='show failed entries',
    action='store_true'
)

parser.add_argument(
    '-I',
    help='show incomplete entries',
    action='store_true'
)

parser.add_argument(
    '-a',
    type=str,
    help='show entries after date, excluded (YYYYMMDD). Special cases: "t" = today, "y" = yesterday, "n" = now.',
    default=19640101,
    metavar=''
)

parser.add_argument(
    '-b',
    type=str,
    help='show entries before date, included (YYYYMMDD). Special cases: "t" = today, "y" = yesterday, "n" = now.',
    default=29640101,
    metavar=''
)

parser.add_argument(
    '-i',
    type=str,
    help='find entries by input file (case insensitive)',
    default='',
    metavar=''
)

parser.add_argument(
    '-o',
    type=str,
    help='find entries by output file (case insensitive)',
    default='',
    metavar=''
)

parser.add_argument(
    '-dd',
    help='find entries with duplicated or dropped frames',
    action='store_true'
)

parser.add_argument(
    '-v',
    action='version',
    version=f'ffquery {VERSION}',
    help='print version number and exit'
)

parser.add_argument(
    '-ö',
    help='find entries by custom id',
    default='',
    metavar=''
)

if __name__ == '__main__':
    args = parser.parse_args()

    with Database() as db:
        if args.R:
            db.reset_table()
        elif args.S:
            print(db.find_by_message('SUCCESS', str(args.a), str(args.b)))
        elif args.F:
            print(db.find_by_message('FAILED', str(args.a), str(args.b)))
        elif args.I:
            print(db.find_by_message('INCOMPLETE', str(args.a), str(args.b)))
        elif args.dd:
            print(db.find_by_dd(
                str(args.a),
                str(args.b)
            ))
        elif args.ö:
            print(db.find_by_custom_id(
                str(args.ö)
            ))
        else:
            print(db.find_by_io(
                args.i,
                args.o,
                str(args.a),
                str(args.b)
            ))
