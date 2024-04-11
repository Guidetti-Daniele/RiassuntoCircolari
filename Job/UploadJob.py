from Sqlite_db import SqliteDB
from PDF_Parsing import parse_pdf
from openai import OpenAI
import argparse
import os
import time
import json
import hashlib


def get_hashes(path, exclude):
    hashes = []
    added_hashes = []

    for file in os.listdir(path):
        name = os.fsdecode(file)
        if name != exclude:
            filepath = os.path.join(path, name)

            file_hash = hashlib.sha256()

            with open(filepath, 'rb') as f:
                while True:
                    data = f.read(65536)  # read file in 64kb parts
                    if not data:
                        break
                    file_hash.update(data)

            hash_ = file_hash.hexdigest()

            if hash_ not in added_hashes:
                hashes.append((filepath, hash_))
                added_hashes.append(hash_)

    return hashes


def read_prefix_file(prefix_file_path):
    return_text = {}

    with open(prefix_file_path, 'r', encoding="utf-8") as file:
        file_lines = file.readlines()
        key_word = None

        for line in file_lines:

            if line.startswith('#'):
                key_word = line.strip()
                return_text[key_word] = ""
            else:
                return_text[key_word] += line

    return return_text


def llm(client, model, prefix, query):
    completion = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system",
             "content": prefix},
            {"role": "user", "content": query}
        ]
    )

    return completion.choices[0].message.content


def main():
    arg_parse = argparse.ArgumentParser()

    # Path to the folder containing all the files
    arg_parse.add_argument("-folder_path", dest="folder_path", required=True)
    # Path to the SQLite DB
    arg_parse.add_argument("-db_connection_string", dest="conn_str", required=True)
    # Name for the prefix file located in the files folder
    arg_parse.add_argument("-prefix_file_name", dest="prefix_file", required=True)

    # OpenAI API key
    arg_parse.add_argument("-api_key", dest="api_key", required=True)
    # OpenAI LLM model
    arg_parse.add_argument("-openai_model", dest="model", required=True)

    args = arg_parse.parse_args()

    folder_path = args.folder_path
    prefix_file = args.prefix_file  # this file contains the LLM prefix

    filenames = [os.fsdecode(file) for file in os.listdir(folder_path)]
    if prefix_file not in filenames:  # check the prefix file
        raise FileNotFoundError("Prefix file missing")

    llm_client = OpenAI(api_key=args.api_key)
    model = args.model

    prefix = read_prefix_file(os.path.join(folder_path, prefix_file))

    try:
        llm_prefix = prefix['#PREFIX']
        json_prefix = prefix['#JSON_PREFIX']
        text_prefix = prefix['#TEXT_PREFIX']
    except KeyError as e:
        raise KeyError(f"Check for the keyword {str(e)} in the prefix file")

    database = SqliteDB(args.conn_str)

    circolari_name = "circolari"
    circolari_rows = {
        "hash": "TEXT PRIMARY KEY",
        "numero": "INTEGER",
        "nome": "TEXT",
        "data": "DATE",
        "destinatari": "TEXT",
        "classi": "TEXT",
        "riassunto": "TEXT"
    }
    comunicazioni_name = "comunicazioni"
    comunicazioni_rows = {
        "hash": "TEXT PRIMARY KEY",
        "nome": "TEXT",
        "data": "DATE",
        "destinatari": "TEXT",
        "classi": "TEXT",
        "riassunto": "TEXT"
    }

    database.init_table(circolari_name, circolari_rows)
    database.init_table(comunicazioni_name, comunicazioni_rows)

    file_hashes = get_hashes(folder_path, prefix_file)
    missing_files = database.get_missing_values(file_hashes, "hash", circolari_name, comunicazioni_name)

    for (path, hash_) in missing_files:
        parsed_text = parse_pdf(path, "Tabella")

        date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(os.path.getmtime(path)))

        data = llm(llm_client, model, llm_prefix, f"{json_prefix}\n{parsed_text}")
        data = data.replace('json', '').replace('```', '')  # Sometimes the LLM uses Markdown

        json_data = json.loads(data)

        num = json_data['Numero']
        name = json_data['Nome']
        destin = json_data['Destinatari']
        classi = json_data['Classi']
        text = llm(llm_client, model, llm_prefix, f"{text_prefix}\n{parsed_text}")

        if num > 0:  # CIRCOLARI
            database.add_row(circolari_name, [hash_, num, name, date, json.dumps(destin), json.dumps(classi), text])
        else:  # COMUNICAZIONI
            database.add_row(comunicazioni_name, [hash_, name, date, json.dumps(destin), json.dumps(classi), text])

    hashes = [hash_ for (_, hash_) in file_hashes]

    # CIRCOLARI
    for circ_hash in database.get_all_id(circolari_name, list(circolari_rows.keys())[0]):
        if circ_hash not in hashes:
            database.remove_row(circolari_name, list(circolari_rows.keys())[0], circ_hash)

    # COMUNICAZIONI
    for com_hash in database.get_all_id(comunicazioni_name, list(comunicazioni_rows.keys())[0]):
        if com_hash not in hashes:
            database.remove_row(comunicazioni_name, list(circolari_rows.keys())[0], com_hash)

    database.close_connection()


if __name__ == "__main__":
    main()
