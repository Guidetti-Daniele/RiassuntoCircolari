import argparse
import json
from flask import Flask, render_template, request
from Sqlite_db import SqliteDB

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

not_to_add = ["1#", "2#", "3#", "4#", "5#", "##"]

all_class = "Tutte le classi"
all_classes_db = "##"
all_dest = "Tutti"
circ_type = {
    circolari_name: "Circolari",
    comunicazioni_name: "Comunicazioni"
}


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


@app.route("/get-destin", methods=["GET"])
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

    dest_list = list(destin_set)

    dest_list.append("#separator#")
    dest_list.append(all_dest)

    return json.dumps(dest_list)


@app.route("/get-types", methods=["GET"])
def get_types():
    return json.dumps(list(circ_type.values()))


@app.route("/get-class", methods=["GET"])
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

    class_set = set()

    for x in all_circ + all_com:
        for y in x:
            if y not in not_to_add:
                class_set.add(y)

    class_list = list(class_set)

    class_list = sorted(class_list, key=sort_key)

    class_list_separated = []

    for i in range(len(class_list)):
        class_list_separated.append(class_list[i])

        if i < len(class_list) - 1 and class_list[i][1:] != class_list[i + 1][1:]:
            class_list_separated.append("#separator#")

    class_list_separated.append("#separator#")
    class_list_separated.append(all_class)

    return json.dumps(class_list_separated)


def get_key(data, value):
    for num, (key, x) in enumerate(data.items()):
        if x == value:
            return key, num
    return None, None


@app.route("/get-circ", methods=["GET"])
def get_circ():
    global connection_string
    database = SqliteDB(connection_string)
    init_db(database)

    # data = json.loads(request.args.get('data', ''))
    # dest = data['dest']
    # class_ = data['class']
    # type_ = data['type']

    dest = request.args.get('dest', '')
    class_ = request.args.get('class', '')
    type_ = request.args.get('type', '')

    table_name, num = get_key(circ_type, type_)
    if not table_name:
        print(f"Table not in list")
        return "[]"

    rows_to_get = list(circolari_rows.keys())[:-1] if num == 0 else list(comunicazioni_rows.keys())[:-1]
    rows = database.get_all_rows(table_name, rows_to_get)

    result_rows = []

    for row in rows:
        row_dest_list = json.loads(row[4 if num == 0 else 3])
        row_class_list = json.loads(row[5 if num == 0 else 4])

        in_classes = False
        for value in row_class_list:
            if ('#' in value) and (class_[0] in value):
                in_classes = True
                break

        if ((dest in row_dest_list) or (dest == all_dest)) and (
                (class_ in row_class_list) or (class_ == all_class) or (
                all_classes_db in row_class_list) or in_classes):
            result_rows.append(row)

    sorted_result = sorted(result_rows, key=lambda x: x[3 if num == 0 else 2])
    return_rows = [[x[0], f"{x[1]} - {x[2]}" if num == 0 else x[1]] for x in sorted_result]

    return json.dumps(return_rows)


@app.route("/get-text", methods=["GET"])
def get_text():
    global connection_string
    database = SqliteDB(connection_string)
    init_db(database)

    hash_ = request.args.get('hash', '')
    type_ = request.args.get('type', '')

    table_name, num = get_key(circ_type, type_)
    if not table_name:
        print(f"Table not in list")
        return "[]"

    text_row_name = list(circolari_rows.keys())[-1] if num == 0 else list(comunicazioni_rows.keys())[-1]
    hash_row_name = list(circolari_rows.keys())[0] if num == 0 else list(comunicazioni_rows.keys())[0]
    text = database.get_data_at_id(table_name, hash_row_name, hash_, text_row_name)

    print(json.dumps(text))

    return json.dumps(text)


if __name__ == "__main__":
    arg_parse = argparse.ArgumentParser()
    # Path to the SQLite DB
    arg_parse.add_argument("-db_connection_string", dest="conn_str", required=True)
    args = arg_parse.parse_args()
    connection_string = args.conn_str

    app.run(host="0.0.0.0", port=8080, threaded=True, debug=True)
