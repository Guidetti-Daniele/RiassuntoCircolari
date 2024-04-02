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

    arg_parse.add_argument("-folder_path", dest="folder_path", required=True)
    arg_parse.add_argument("-db_connection_string", dest="conn_str", required=True)
    arg_parse.add_argument("-prefix_file_name", dest="prefix_file", required=True)

    arg_parse.add_argument("-api_key", dest="api_key", required=True)
    arg_parse.add_argument("-openai_model", dest="model", required=True)

    args = arg_parse.parse_args()

    folder_path = args.folder_path
    prefix_file = args.prefix_file  # this file contains the LLM prefix

    filenames = [os.fsdecode(file) for file in os.listdir(folder_path)]
    if prefix_file not in filenames:  # verify that is the correct folder
        raise "Not correct directory - make a file named .circolari containing the prefix for the LLM"

    llm_client = OpenAI(api_key=args.api_key)
    model = args.model
    with open(os.path.join(folder_path, prefix_file), 'r') as file:
        llm_prefix = file.read()

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

        data = llm(llm_client, model, llm_prefix, f"""JSON
        Dati richiesti:
        Numero (Numero della circolare, se non specificato è -1),
        Nome (Nome della circolare),
        Destinatari (rispondi usando alcune tra queste parole come lista: "Studenti", "Docenti", "Genitori", "Personale"),
        Classi (Le classi che riguardano la circolare come lista, se tutte rispondi con ["Tutte le classi"], se la sezione non viene specificata rispondi con "n#" , dove n è il numero della classe)
        
        {parsed_text}
        """).replace('json', '').replace('```', '')

        json_data = json.loads(data)

        num = json_data['Numero']
        name = json_data['Nome']
        destin = json_data['Destinatari']
        classi = json_data['Classi']
        text = llm(llm_client, model, llm_prefix, f"""
        TEXT

        {parsed_text}
        """)

        if num > 0:
            database.add_row(circolari_name, [hash_, num, name, date, str(destin), str(classi), text])
        else:
            database.add_row(comunicazioni_name, [hash_, name, date, str(destin), str(classi), text])

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
