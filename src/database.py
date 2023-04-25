import sqlite3
import os

from .colors import Col


class Database:
    def __init__(self):
        self.__create_db_folder()
        self.conn = sqlite3.connect('db/ffwrap.db')
        self.cur = self.conn.cursor()
        self.__create_table()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close_connection()

    def __create_db_folder(self):
        if not os.path.isdir('db'):
            os.mkdir('db')

    def __create_table(self):
        self.cur.execute(
            f"CREATE TABLE IF NOT EXISTS renders (id INTEGER PRIMARY KEY, command TEXT, inputs TEXT, outputs TEXT, total_time INTEGER, exit_code INTEGER, duplicated_frames INTEGER, dropped_frames INTEGER, start_time DATETIME, end_time DATETIME)")
        self.conn.commit()

    def __format_entries(self, entries: list[tuple]) -> str:
        formatted_entries = []
        for e in entries:
            formatted_entries.append('\n'.join([
                f'ID: {e[0]}',
                f'  FFmpeg command: "{Col.blue}{e[1]}{Col.endc}"',
                f'  Inputs: {e[2].split(":::")}',
                f'  Outputs: {e[3].split(":::")}',
                f'  Total time: {Col.green if e[4] else Col.fail}{e[4]}{"s" if e[4] else ""}{Col.endc} (start: {e[8]}, end: {e[9]})',
                f'  Exit code: {Col.blue if e[5] == 0 else Col.fail}{e[5]}{Col.endc}' +
                (f' (dup: {e[6]}, drop: {e[7]})' if e[6] or e[7] else '')
            ]))
        return '\n\n'.join(formatted_entries)

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

    def init_before_render(
            self,
            command: str,
            inputs: str,
            outputs: str,
            start_time: str,
    ) -> int | None:
        self.cur.execute(
            f"INSERT INTO renders (command, inputs, outputs, start_time) VALUES (?, ?, ?, ?)",
            (command, inputs, outputs, start_time)
        )
        self.conn.commit()
        return self.cur.lastrowid

    def update_after_render(self, id: int, total_time: int, end_time: str, exit_code: int, duplicated_frames: int, dropped_frames: int):
        self.cur.execute(
            f"UPDATE renders SET total_time=?, end_time=?, exit_code=?, duplicated_frames=?, dropped_frames=? WHERE id=?",
            (total_time, end_time, exit_code, duplicated_frames, dropped_frames, id)
        )
        self.conn.commit()

    def get_all(self):
        self.cur.execute("SELECT * FROM renders")
        return self.__format_entries(self.cur.fetchall())

    def find_by_input(self, i: str):
        self.cur.execute(
            "SELECT * FROM renders WHERE inputs LIKE ?", (f'%{i}%',))
        return self.__format_entries(self.cur.fetchall())

    def find_by_output(self, o: str):
        self.cur.execute(
            "SELECT * FROM renders WHERE outputs LIKE ?", (f'%{o}%',))
        return self.__format_entries(self.cur.fetchall())
