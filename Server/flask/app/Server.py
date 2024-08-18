from app.Parameters import parameters
import json
from flask import Flask, render_template, request
from app.ServerAPI import api
from app.Sqlite_db import SqliteDB


app = Flask(__name__)
app.register_blueprint(api)


def init_db(database):
    database.init_table(parameters.circolari_name, parameters.circolari_rows)
    database.init_table(parameters.comunicazioni_name, parameters.comunicazioni_rows)


def sort_key(x):
    return x[1:] + x[0]


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/get-destin", methods=["GET"])
def get_destin():
    database = SqliteDB(parameters.connection_string)
    init_db(database)

    all_circ = [
        json.loads(x)
        for x in database.get_all_id(
            parameters.circolari_name, list(parameters.circolari_rows.keys())[4]
        )
    ]
    all_com = [
        json.loads(x)
        for x in database.get_all_id(
            parameters.comunicazioni_name, list(parameters.comunicazioni_rows.keys())[3]
        )
    ]

    destin_set = set()

    for x in all_circ + all_com:
        destin_set.update(x)

    dest_list = list(destin_set)

    dest_list.append(parameters.all_dest)

    database.close_connection()

    return json.dumps(dest_list)


@app.route("/get-types", methods=["GET"])
def get_types():
    return json.dumps(list(parameters.circ_type.values()))


@app.route("/get-class", methods=["GET"])
def get_class():
    database = SqliteDB(parameters.connection_string)
    init_db(database)

    all_circ = [
        json.loads(x)
        for x in database.get_all_id(
            parameters.circolari_name, list(parameters.circolari_rows.keys())[5]
        )
    ]
    all_com = [
        json.loads(x)
        for x in database.get_all_id(
            parameters.comunicazioni_name, list(parameters.comunicazioni_rows.keys())[4]
        )
    ]

    class_set = set()

    for x in all_circ + all_com:
        for y in x:
            if y not in parameters.not_to_add:
                class_set.add(y)

    class_list = list(class_set)

    class_list = sorted(class_list, key=sort_key)

    class_list_separated = []

    for i in range(len(class_list)):
        class_list_separated.append(class_list[i])

    class_list_separated.append(parameters.all_class)

    database.close_connection()

    return json.dumps(class_list_separated)


def get_key(data, value):
    for num, (key, x) in enumerate(data.items()):
        if x == value:
            return key, num
    return None, None


@app.route("/get-circ", methods=["GET"])
def get_circ():
    database = SqliteDB(parameters.connection_string)
    init_db(database)

    # data = json.loads(request.args.get('data', ''))
    # dest = data['dest']
    # class_ = data['class']
    # type_ = data['type']

    dest = request.args.get("dest", "")
    class_ = request.args.get("class", "")
    type_ = request.args.get("type", "")

    table_name, num = get_key(parameters.circ_type, type_)
    if not table_name:
        print(f"Table not in list")
        return "[]"

    rows_to_get = (
        list(parameters.circolari_rows.keys())[:-1]
        if num == 0
        else list(parameters.comunicazioni_rows.keys())[:-1]
    )
    rows = database.get_all_rows(table_name, rows_to_get)

    result_rows = []

    for row in rows:
        row_dest_list = json.loads(row[4 if num == 0 else 3])
        row_class_list = json.loads(row[5 if num == 0 else 4])

        in_classes = False
        for value in row_class_list:
            if (("#" in value) and (class_[0] in value)) or (
                (len(value) < 3 or len(class_) < 3) and value[:2] == class_[:2]
            ):
                in_classes = True
                break

        if ((dest in row_dest_list) or (dest == parameters.all_dest)) and (
            (class_ in row_class_list)
            or (class_ == parameters.all_class)
            or (parameters.all_classes_db in row_class_list)
            or in_classes
        ):
            result_rows.append(row)

    sorted_result = sorted(
        result_rows, key=lambda x: x[3 if num == 0 else 2], reverse=True
    )
    return_rows = [
        [x[0], f"{x[1]} - {x[2]}" if num == 0 else x[1]] for x in sorted_result
    ]

    database.close_connection()

    return json.dumps(return_rows)


@app.route("/get-text", methods=["GET"])
def get_text():
    database = SqliteDB(parameters.connection_string)
    init_db(database)

    hash_ = request.args.get("hash", "")
    type_ = request.args.get("type", "")

    table_name, num = get_key(parameters.circ_type, type_)
    if not table_name:
        print(f"Table not in list")
        return "[]"

    text_row_name = (
        list(parameters.circolari_rows.keys())[-1]
        if num == 0
        else list(parameters.comunicazioni_rows.keys())[-1]
    )
    hash_row_name = (
        list(parameters.circolari_rows.keys())[0]
        if num == 0
        else list(parameters.comunicazioni_rows.keys())[0]
    )
    text = database.get_data_at_id(table_name, hash_row_name, hash_, text_row_name)

    database.close_connection()

    return json.dumps(text)
