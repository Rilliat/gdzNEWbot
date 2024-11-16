from . import config

import sqlite3


class Database:
    def __init__(self):
        self.conn = sqlite3.connect(config.database_name)
        self.cursor = self.conn.cursor()

    def initialize(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS tokens (
                    id    INTEGER   PRIMARY KEY 
                                    AUTOINCREMENT,
                    token TEXT      UNIQUE NOT NULL,
                    valid INTEGER   NOT NULL
                                    DEFAULT (1),
                    used  INTEGER   NOT NULL
                                    DEFAULT (0) 
        );
        ''')
        self.conn.commit()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id         INTEGER NOT NULL
                                    UNIQUE,
            access_token_id TEXT    UNIQUE
                                    REFERENCES tokens(id),
            valid           INTEGER DEFAULT 1,
            vip             INTEGER DEFAULT 0,
            eljur_token     TEXT    UNIQUE
        );''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS callback (
            id          INTEGER PRIMARY KEY 
                                AUTOINCREMENT,
            user_id     INTEGER NOT NULL,
            callback    INTEGER NOT NULL
        );''')
        self.conn.commit()


    def add_user(self, user_id: int):
        self.cursor.execute('''INSERT INTO users (user_id) VALUES (?)''',
                            (user_id,))
        self.conn.commit()

    def remove_user(self, user_id: int):
        self.cursor.execute('''DELETE FROM users WHERE user_id = ?''',
                            (user_id,))
        self.conn.commit()

    def add_access_token_to_user(self, user_id: int, access_token: str):
        self.cursor.execute('''UPDATE users SET access_token_id=(SELECT id FROM tokens WHERE token='?') 
                                   WHERE user_id=?''',
                            (access_token, user_id,))
        self.cursor.execute('''UPDATE tokens SET used=1 WHERE token=?''',
                            (access_token,))
        self.conn.commit()

    def set_valid_user(self, user_id: int, valid: bool):
        self.cursor.execute('''UPDATE users SET valid=? WHERE user_id=?''',
                            (valid, user_id,))
        self.conn.commit()

    def set_vip_user(self, user_id: int, vip: bool):
        self.cursor.execute('''UPDATE users SET vip=? WHERE user_id=?''',
                            (vip, user_id,))
        self.conn.commit()

    def check_access(self, user_id: int) -> str:
        self.cursor.execute('''SELECT access_token_id FROM users WHERE user_id=?''',
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

    def fetch_vip_users(self) -> tuple[int]:
        self.cursor.execute('''SELECT user_id FROM users WHERE valid=1 AND vip=1 AND eljur_token IS NOT NULL''')
        try:
            return self.cursor.fetchall()[0]
        except IndexError:
            return (0,)

    def add_token(self, token: str):
        self.cursor.execute('''INSERT INTO tokens (token) VALUES (?)''',
                            (token,))
        self.conn.commit()

    def set_valid_token(self, token: str, valid: bool):
        self.cursor.execute('''UPDATE OR IGNORE tokens SET valid=? WHERE token=?''',
                            (valid, token,))
        self.conn.commit()

