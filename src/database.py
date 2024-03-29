import sqlite3
import os
from pathlib import Path

from .date_utils import format_query_date

from .colors import Col


class Database:
    def __init__(self):
        self.db_folder = os.path.join(
            Path(__file__).parents[1],
            'db'
        )
        self.__create_db_folder(self.db_folder)
        self.conn = sqlite3.connect(
            os.path.join(
                self.db_folder,
                'ffwrap.db'
            )
        )
        self.cur = self.conn.cursor()
        self.__create_table()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close_connection()

    def __create_db_folder(self, db_folder):
        if not os.path.isdir(db_folder):
            os.mkdir(db_folder)

    def __create_table(self):
        self.cur.execute(
            f"CREATE TABLE IF NOT EXISTS renders (id INTEGER PRIMARY KEY, command TEXT, inputs TEXT, outputs TEXT, total_time INTEGER, exit_code INTEGER, duplicated_frames INTEGER, dropped_frames INTEGER, start_time DATETIME, end_time DATETIME, message TEXT, custom_id TEXT)")
        self.conn.commit()

    def __format_entries(self, entries: list[tuple], summary: bool = False) -> str:
        if not entries:
            return f'{Col.fail}No entries found{Col.endc}'
        formatted_entries = []

        for e in entries:
            messcol = Col.yellow if e[10] == 'INCOMPLETE' else Col.blue if e[10] == 'SUCCESS' else Col.fail
            inputs = [i for i in e[2].split(':::') if i != '']
            outputs = [o for o in e[3].split(':::') if o != '']
            formatted_entries.append('\n'.join([
                f'{Col.underline}ID: {e[0]}{Col.endc}',
                f'  FFmpeg command: "{Col.bold}{Col.blue}{e[1]}{Col.endc}"',
                f'  Inputs: {Col.warn if len(inputs) == 0 else Col.default}{inputs}{Col.endc}',
                f'  Outputs: {Col.warn if len(outputs) == 0 else Col.default}{outputs}{Col.endc}',
                f'  Total time: {Col.green if e[4] or e[4] == 0 else Col.fail}{e[4]}{"s" if e[4] or e[4] == 0 else ""}{Col.endc} (start: {e[8]}, end: {e[9]})',
                f'  Exit code: {Col.cyan if e[5] == 0 else Col.fail}{e[5]}{Col.endc}' +
                (f' {Col.yellow}(dup: {e[6]}, drop: {e[7]}){Col.endc}' if e[6]
                 or e[7] else ''),
                f'  Result: {messcol}{e[10]}{Col.endc}' if e[10] else '',
                f'  Custom ID: {Col.cyan}{e[11]}{Col.endc}' if e[11] else ''
            ]))
        total_success = len(
            [e for e in entries if e[10] == 'SUCCESS'])
        total_failed = len(
            [e for e in entries if e[10] == 'FAILED'])
        total_incomplete = len(
            [e for e in entries if e[10] == 'INCOMPLETE'])

        total_entries_label = 'Total entries found:'
        formatted_entries = '\n\n'.join(
            formatted_entries + [f'{Col.underline}{Col.cyan}{total_entries_label}{" " * (25 - len(total_entries_label))}{len(formatted_entries)}{Col.endc}'])

        if summary:
            total_success_label = 'Total successful:'
            total_failed_label = 'Total failed:'
            total_incomplete_label = 'Total incomplete:'
            formatted_entries += f'\n\n{Col.green}{total_success_label}{" " * (25 - len(total_success_label))}{total_success}{Col.endc}\n{Col.fail}{total_failed_label}{" " * (25 - len(total_failed_label))}{total_failed}{Col.endc}\n{Col.yellow}{total_incomplete_label}{" " * (25 - len(total_incomplete_label))}{total_incomplete}{Col.endc}\n{Col.underline}{" " * 30}{Col.endc}\n'

        return formatted_entries

    def reset_table(self):
        confirm = input(
            f'{Col.warn}Are you sure you want to reset the database? [y/N]{Col.endc} ')
        if confirm.lower() != 'y':
            print(f'{Col.fail}Aborting{Col.endc}')
            return
        self.cur.execute(f"DROP TABLE renders")
        self.__create_table()
        print(f'{Col.green}Database reset{Col.endc}')

    def close_connection(self):
        self.conn.close()

    def initialize_entry(
            self,
            command: str,
            inputs: str,
            outputs: str,
            start_time: str,
            custom_id: str
    ) -> int | None:
        self.cur.execute(
            f"INSERT INTO renders (command, inputs, outputs, start_time, message, custom_id) VALUES (?, ?, ?, ?, ?, ?)",
            (command, inputs, outputs, start_time, 'INCOMPLETE', custom_id)
        )
        self.conn.commit()
        return self.cur.lastrowid

    def update(
            self,
            id: int,
            total_time: int,
            end_time: str,
            exit_code: int,
            duplicated_frames: int,
            dropped_frames: int,
            message: str
    ) -> None:
        self.cur.execute(
            f"UPDATE renders SET total_time=?, end_time=?, exit_code=?, duplicated_frames=?, dropped_frames=?, message=? WHERE id=?",
            (total_time, end_time, exit_code,
             duplicated_frames, dropped_frames, message, id)
        )
        self.conn.commit()

    def find_by_io(self, i: str, o: str, after: str, before: str) -> str:
        result_a, a = format_query_date(after)
        result_b, b = format_query_date(before)

        if not result_a:
            print(
                f'{Col.fail}Invalid date format for "-a". Using default value{Col.endc}')
        if not result_b:
            print(
                f'{Col.fail}Invalid date format for "-b". Using default value{Col.endc}')

        self.cur.execute(
            "SELECT * FROM renders WHERE inputs LIKE ? AND outputs LIKE ? AND start_time >= ? AND start_time <= ?",
            (
                f'%{i}%',
                f'%{o}%',
                a if result_a else "1964-01-01 00:00:00",
                b if result_b else "2964-01-01 00:00:00"
            )
        )

        return self.__format_entries(self.cur.fetchall())

    def find_by_message(self, message: str, after: str, before: str):
        result_a, a = format_query_date(after)
        result_b, b = format_query_date(before)

        if not result_a:
            print(
                f'{Col.fail}Invalid date format for "-a". Using default value{Col.endc}')
        if not result_b:
            print(
                f'{Col.fail}Invalid date format for "-b". Using default value{Col.endc}')

        self.cur.execute(
            "SELECT * FROM renders WHERE message LIKE ? AND start_time >= ? AND start_time <= ?",
            (
                f'%{message}%',
                a if result_a else "1964-01-01 00:00:00",
                b if result_b else "2964-01-01 00:00:00"
            )
        )
        return self.__format_entries(self.cur.fetchall())

    def find_by_dd(self, after: str, before: str):
        result_a, a = format_query_date(after)
        result_b, b = format_query_date(before)

        if not result_a:
            print(
                f'{Col.fail}Invalid date format for "-a". Using default value{Col.endc}')
        if not result_b:
            print(
                f'{Col.fail}Invalid date format for "-b". Using default value{Col.endc}')

        self.cur.execute(
            "SELECT * FROM renders WHERE (duplicated_frames > 0 OR dropped_frames > 0) AND start_time >= ? AND start_time <= ?",
            (
                a if result_a else "1964-01-01 00:00:00",
                b if result_b else "2964-01-01 00:00:00"
            )
        )
        return self.__format_entries(self.cur.fetchall())

    def find_by_custom_id(self, custom_id: str):
        self.cur.execute(
            "SELECT * FROM renders WHERE custom_id LIKE '%' || ? || '%'",
            (custom_id,)
        )

        return self.__format_entries(self.cur.fetchall(), summary=True)
