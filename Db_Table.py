import sqlite3


class DbTable:

    def __init__(self, db_path_string):
        self.connection = sqlite3.connect(db_path_string)
        self.db_cursor = self.connection.cursor()

        self.db_cursor.execute('''SELECT count(name) FROM sqlite_master WHERE type='table' AND name='circolari' ''')
        if self.db_cursor.fetchone()[0] == 0:  # create table if not already created
            self.db_cursor.execute("CREATE TABLE circolari(name, date, hash, text, number)")

    def close_connection(self):  # close and save
        self.connection.commit()
        self.connection.close()

    def contains_hash(self, hash_):  # check if the file with this hash is already parsed
        db_hash_col = self.db_cursor.execute("SELECT hash FROM circolari").fetchall()
        db_hashes = [value[0] for value in db_hash_col]

        return hash_ in db_hashes

    def add_row(self, name, date, hash_, text, number):
        self.db_cursor.execute("INSERT INTO circolari VALUES (?,?,?,?,?)",
                               (name, date, hash_, text, number,))
