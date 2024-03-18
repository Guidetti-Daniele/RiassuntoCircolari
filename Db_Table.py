import sqlite3


class DbTable:

    def __init__(self, db_path_string):
        self.connection = sqlite3.connect(db_path_string)
        self.db_cursor = self.connection.cursor()

    def init_table(self, table_name, columns, types):
        self.db_cursor.execute(f"SELECT count(name) FROM sqlite_master WHERE type='table' AND name='{table_name}' ")

        if self.db_cursor.fetchone()[0] == 0:  # create table if not already created
            columns_with_types = [f"{column} {type_}" for column, type_ in zip(columns, types)]

            create_table_query = f"CREATE TABLE {table_name}({', '.join(columns_with_types)})"
            self.db_cursor.execute(create_table_query)

    def close_connection(self):  # close and save
        self.connection.commit()
        self.connection.close()

    def contains(self, value, col_name, table_name):  # check if the file with this hash is already parsed
        db_col = self.db_cursor.execute(f"SELECT {col_name} FROM {table_name}").fetchall()
        db_values = [value[0] for value in db_col]

        return value in db_values

    def add_row(self, table_name, values):
        self.db_cursor.execute(f"INSERT INTO {table_name} VALUES ({','.join('?' for _ in values)})",
                               values)
