from flask import Flask, render_template
from Sqlite_db import SqliteDB
import argparse
import json

circolari_name = "circolari"
circolari_rows = {
    "hash": "TEXT PRIMARY KEY",
    "numero": "INTEGER",
    "nome": "TEXT",
    "data": "DATE",
    "destinatari": "TEXT",
    "classi": "TEXT",
    "riassunto": "TEXT",
}
comunicazioni_name = "comunicazioni"
comunicazioni_rows = {
    "hash": "TEXT PRIMARY KEY",
    "nome": "TEXT",
    "data": "DATE",
    "destinatari": "TEXT",
    "classi": "TEXT",
    "riassunto": "TEXT",
}

not_to_add = ["1#", "2#", "3#", "4#", "5#", "Tutte le classi"]


def init_db(database):
    database.init_table(circolari_name, circolari_rows)
    database.init_table(comunicazioni_name, comunicazioni_rows)


def sort_key(x):
    return x[1:] + x[0]


app = Flask(__name__)
connection_string = None


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/get-destin")
def get_destin():
    global connection_string
    database = SqliteDB(connection_string)
    init_db(database)

    all_circ = [
        json.loads(x)
        for x in database.get_all_id(circolari_name, list(circolari_rows.keys())[4])
    ]
    all_com = [
        json.loads(x)
        for x in database.get_all_id(
            comunicazioni_name, list(comunicazioni_rows.keys())[3]
        )
    ]

    destin_set = set()

    for x in all_circ + all_com:
        destin_set.update(x)

    return json.dumps(list(destin_set))


@app.route("/get-class")
def get_class():
    global connection_string
    database = SqliteDB(connection_string)
    init_db(database)

    all_circ = [
        json.loads(x)
        for x in database.get_all_id(circolari_name, list(circolari_rows.keys())[5])
    ]
    all_com = [
        json.loads(x)
        for x in database.get_all_id(
            comunicazioni_name, list(comunicazioni_rows.keys())[4]
        )
    ]

    destin_set = set()

    for x in all_circ + all_com:
        for y in x:
            if y not in not_to_add:
                destin_set.add(y)

    destin_list = list(destin_set)

    destin_list = sorted(destin_list, key=sort_key)

    destin_list_separated = []

    for i in range(len(destin_list)):
        destin_list_separated.append(destin_list[i])

        if i < len(destin_list) - 1 and destin_list[i][1:] != destin_list[i + 1][1:]:
            destin_list_separated.append("#separator#")

    destin_list_separated.append("#separator#")
    destin_list_separated.append("Tutte le classi")

    return json.dumps(destin_list_separated)


if __name__ == "__main__":
    arg_parse = argparse.ArgumentParser()
    # Path to the SQLite DB
    arg_parse.add_argument("-db_connection_string", dest="conn_str", required=True)
    args = arg_parse.parse_args()
    connection_string = args.conn_str

    app.run(host="0.0.0.0", port=8080, threaded=True, debug=True)
