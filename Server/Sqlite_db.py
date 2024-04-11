import sqlite3


class SqliteDB:

    def __init__(self, db_path_string):
        self.connection = sqlite3.connect(db_path_string)
        self.db_cursor = self.connection.cursor()

    def init_table(self, table_name, values):
        self.db_cursor.execute(f"SELECT count(name) FROM sqlite_master WHERE type='table' AND name='{table_name}' ")

        if self.db_cursor.fetchone()[0] == 0:  # create table if not already created
            columns_with_types = [f"{column} {type_}" for column, type_ in values.items()]

            create_table_query = f"CREATE TABLE {table_name}({', '.join(columns_with_types)})"
            self.db_cursor.execute(create_table_query)

    def close_connection(self):  # close and save
        self.connection.commit()
        self.connection.close()

    def get_missing_values(self, values, col_name, table_name, table2_name):
        db_col = self.db_cursor.execute(f"SELECT {col_name} FROM {table_name}").fetchall()
        db_values = [value[0] for value in db_col]
        db_col2 = self.db_cursor.execute(f"SELECT {col_name} FROM {table2_name}").fetchall()
        for value in db_col2:
            db_values.append(value[0])

        missing_values = []
        added_values = []

        for (val1, val2) in values:
            if (val2 not in db_values) and (val2 not in added_values):
                missing_values.append((val1, val2))
                added_values.append(val2)

        return missing_values

    def get_all_id(self, table_name, id_name):
        id_ = []

        self.db_cursor.execute(f"SELECT {id_name} FROM {table_name}")

        rows = self.db_cursor.fetchall()
        for row in rows:
            id_.append(row[0])

        return id_

    def add_row(self, table_name, values):
        self.db_cursor.execute(f"INSERT INTO {table_name} VALUES ({','.join('?' for _ in values)})",
                               values)

    def remove_row(self, table_name, id_name, id_value):
        self.db_cursor.execute(f"DELETE FROM {table_name} WHERE {id_name} = ?", (id_value,))
