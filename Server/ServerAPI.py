import json
import hashlib
from flask import Blueprint, request
from Sqlite_db import SqliteDB
from Parameters import parameters

api = Blueprint('api', __name__)


@api.route('/get_missing_values', methods=['GET'])
def missing_values():
    data = request.get_json()
    key = data.get('key')
    hashes = data.get('hashes')

    if not key or not hashes:
        return json.dumps({'message': 'Bad request'}), 400

    key_hash = hashlib.sha256(key.encode('UTF-8')).hexdigest()
    if key_hash != parameters.db_api_key_hash:
        return json.dumps({'message': 'Authentication failed'}), 401

    try:

        database = SqliteDB(parameters.connection_string)

        database.init_table(parameters.circolari_name, parameters.circolari_rows)
        database.init_table(parameters.comunicazioni_name, parameters.comunicazioni_rows)

        missing_files = database.get_missing_values(hashes, list(parameters.circolari_rows.keys())[0],
                                                    parameters.circolari_name,
                                                    parameters.comunicazioni_name)

        database.close_connection()

    except Exception as e:
        return json.dumps({'message': f'Error {str(e)}'}), 500

    response = {
        'message': 'OK',
        'data': missing_files
    }

    return json.dumps(response), 200


def add_element(row_data, table_name):
    database = SqliteDB(parameters.connection_string)

    database.init_table(parameters.circolari_name, parameters.circolari_rows)
    database.init_table(parameters.comunicazioni_name, parameters.comunicazioni_rows)

    database.add_row(table_name, row_data)

    database.close_connection()


@api.route('/add_circ', methods=['PUT'])
def add_circ():
    data = request.get_json()
    key = data.get('key')
    row_data = data.get('data')

    if not key or not row_data:
        return json.dumps({'message': 'Bad request'}), 400

    key_hash = hashlib.sha256(key.encode('UTF-8')).hexdigest()
    if key_hash != parameters.db_api_key_hash:
        return json.dumps({'message': 'Authentication failed'}), 401

    try:
        add_element(row_data, parameters.circolari_name)
    except Exception as e:
        return json.dumps({'message': f'Error {str(e)}'}), 500

    return json.dumps({'message': 'OK'}), 200


@api.route('/add_comm', methods=['PUT'])
def add_comm():
    data = request.get_json()
    key = data.get('key')
    row_data = data.get('data')

    if not key or not row_data:
        return json.dumps({'message': 'Bad request'}), 400

    key_hash = hashlib.sha256(key.encode('UTF-8')).hexdigest()
    if key_hash != parameters.db_api_key_hash:
        return json.dumps({'message': 'Authentication failed'}), 401

    try:
        add_element(row_data, parameters.comunicazioni_name)
    except Exception as e:
        return json.dumps({'message': f'Error {str(e)}'}), 500

    return json.dumps({'message': 'OK'}), 200


def get_all_hashes(table_name, table_rows):
    database = SqliteDB(parameters.connection_string)

    database.init_table(parameters.circolari_name, parameters.circolari_rows)
    database.init_table(parameters.comunicazioni_name, parameters.comunicazioni_rows)

    data = database.get_all_id(table_name, list(table_rows.keys())[0])

    database.close_connection()

    return data


@api.route('/get_circ_hashes', methods=['GET'])
def get_circ_hashes():
    data = request.get_json()
    key = data.get('key')

    if not key:
        return json.dumps({'message': 'Bad request'}), 400

    key_hash = hashlib.sha256(key.encode('UTF-8')).hexdigest()
    if key_hash != parameters.db_api_key_hash:
        return json.dumps({'message': 'Authentication failed'}), 401

    try:
        data = get_all_hashes(parameters.circolari_name, parameters.circolari_rows)
    except Exception as e:
        return json.dumps({'message': f'Error {str(e)}'}), 500

    response = {
        'message': 'OK',
        'data': data
    }

    return json.dumps(response), 200


@api.route('/get_comm_hashes', methods=['GET'])
def get_comm_hashes():
    data = request.get_json()
    key = data.get('key')

    if not key:
        return json.dumps({'message': 'Bad request'}), 400

    key_hash = hashlib.sha256(key.encode('UTF-8')).hexdigest()
    if key_hash != parameters.db_api_key_hash:
        return json.dumps({'message': 'Authentication failed'}), 401

    try:
        data = get_all_hashes(parameters.comunicazioni_name, parameters.comunicazioni_rows)
    except Exception as e:
        return json.dumps({'message': f'Error {str(e)}'}), 500

    response = {
        'message': 'OK',
        'data': data
    }

    return json.dumps(response), 200


def delete_row(table_name, table_rows, hash_):
    database = SqliteDB(parameters.connection_string)

    database.init_table(parameters.circolari_name, parameters.circolari_rows)
    database.init_table(parameters.comunicazioni_name, parameters.comunicazioni_rows)

    database.remove_row(table_name, list(table_rows.keys())[0], hash_)

    database.close_connection()


@api.route('/delete_circ', methods=['DELETE'])
def delete_circ():
    data = request.get_json()
    key = data.get('key')
    hash_to_delete = data.get('hash')

    if not key or not hash_to_delete:
        return json.dumps({'message': 'Bad request'}), 400

    key_hash = hashlib.sha256(key.encode('UTF-8')).hexdigest()
    if key_hash != parameters.db_api_key_hash:
        return json.dumps({'message': 'Authentication failed'}), 401

    try:
        delete_row(parameters.circolari_name, parameters.circolari_rows, hash_to_delete)
    except Exception as e:
        return json.dumps({'message': f'Error {str(e)}'}), 500

    return json.dumps({'message': 'OK'}), 200


@api.route('/delete_comm', methods=['DELETE'])
def delete_comm():
    data = request.get_json()
    key = data.get('key')
    hash_to_delete = data.get('hash')

    if not key or not hash_to_delete:
        return json.dumps({'message': 'Bad request'}), 400

    key_hash = hashlib.sha256(key.encode('UTF-8')).hexdigest()
    if key_hash != parameters.db_api_key_hash:
        return json.dumps({'message': 'Authentication failed'}), 401

    try:
        delete_row(parameters.comunicazioni_name, parameters.comunicazioni_rows, hash_to_delete)
    except Exception as e:
        return json.dumps({'message': f'Error {str(e)}'}), 500

    return json.dumps({'message': 'OK'}), 200
