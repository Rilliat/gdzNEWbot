from . import config

import sqlite3


class Database:
    def __init__(self):
        self.conn = sqlite3.connect(config.database_name)
        self.cursor = self.conn.cursor()

    def initialize(self):
        self.cursor.execute('''CREATE TABLE users (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id      INTEGER NOT NULL
                                 UNIQUE,
            access_token TEXT    UNIQUE,
            valid        INTEGER DEFAULT 1,
            vip          INTEGER DEFAULT 0,
            eljur_token  TEXT    UNIQUE
        );''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS callback (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id     INTEGER NOT NULL,
            callback    INTEGER NOT NULL
        );''')
        self.conn.commit()


    def add_user(self, user_id: int):
        self.cursor.execute('''INSERT INTO users (user_id) VALUES (?)''',
                            (user_id,))
        self.conn.commit()

    def add_access_token_to_user(self, user_id: int, access_token: str):
        self.cursor.execute('''UPDATE users SET access_token='?' WHERE user_id=?''',
                            (access_token, user_id,))
        self.conn.commit()

    def set_valid(self, user_id: int, valid: bool):
        self.cursor.execute('''UPDATE users SET valid=? WHERE user_id=?''',
                            (valid, user_id,))
        self.conn.commit()

    def set_vip(self, user_id: int, vip: bool):
        self.cursor.execute('''UPDATE users SET vip=? WHERE user_id=?''',
                            (vip, user_id,))
        self.conn.commit()

    def add_callback(self, user_id: int, callback: int):
        self.cursor.execute('''INSERT INTO callback (user_id, callback) VALUES (?, ?)''',
                            (user_id, callback,))
        self.conn.commit()

    def check_access(self, user_id: int) -> str:
        self.cursor.execute('''SELECT access_token FROM users WHERE user_id=?''',
                            (user_id,))
        return self.cursor.fetchone()[0]

    def check_callback(self, user_id: int = None) -> float:
        if user_id is None:
            self.cursor.execute('''SELECT AVG(callback) FROM callback''')
        else:
            self.cursor.execute('''SELECT AVG(callback) FROM callback WHERE user_id=?''',
                                (user_id,))
        return self.cursor.fetchone()[0]

    def check_users(self, valid: bool = None, vip: bool = None) -> int:
        if valid:
            self.cursor.execute('''SELECT COUNT(*) FROM users WHERE valid=1''')
        elif vip:
            self.cursor.execute('''SELECT COUNT(*) FROM users WHERE vip=1''')
        else:
            self.cursor.execute('''SELECT COUNT(*) FROM users''')
        return self.cursor.fetchone()[0]

    def insert_callback(self, user_id: int, callback: int):
        self.cursor.execute('''INSERT INTO callback (user_id, callback) VALUES (?, ?)''',
                            (user_id, callback,))
        self.conn.commit()

    def insert_eljur_token(self, user_id: int, eljur_token: str):
        self.cursor.execute('''UPDATE users set eljur_token=? WHERE user_id=?''',
                            (eljur_token, user_id,))
        self.conn.commit()

    def fetch_eljur_token(self, user_id: int) -> str:
        self.cursor.execute('''SELECT eljur_token FROM users WHERE user_id=?''',
                            (user_id,))
        result = self.cursor.fetchone()
        return result[0]
