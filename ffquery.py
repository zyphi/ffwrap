import argparse
from src.database import Database


if __name__ == '__main__':
    with Database() as db:
        db.reset_table()
