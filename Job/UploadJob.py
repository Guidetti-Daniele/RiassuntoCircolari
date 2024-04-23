from Server_db_API import ServerDbAPI
from openai import OpenAI
from PyPDF2 import PdfReader
import argparse
import os
import datetime
import json
import hashlib


def parse_pdf(file_path):
    reader = PdfReader(file_path)

    all_text = ''
    for page in reader.pages:
        all_text += page.extract_text()

    return all_text


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
    # Base URL for the DB API, for example http://127.0.0.1:8080
    arg_parse.add_argument("-base_url", dest="api_url", required=True)
    # Key for the DB API
    arg_parse.add_argument("-db_api_key", dest="db_api_key", required=True)
    # Name for the prefix file located in the files folder
    arg_parse.add_argument("-prefix_file_name", dest="prefix_file", required=True)

    # OpenAI API key
    arg_parse.add_argument("-api_key", dest="api_key", required=True)
    # OpenAI LLM model
    arg_parse.add_argument("-openai_model", dest="model", required=True)

    # OpenAI Input pricing per million tokens - to calculate cost of every processed document - not required
    arg_parse.add_argument("-model_pricing_input", dest="model_pricing_input", required=False)
    # OpenAI Output pricing per million tokens - to calculate cost of every processed document - not required
    arg_parse.add_argument("-model_pricing_output", dest="model_pricing_output", required=False)

    args = arg_parse.parse_args()

    pricing_input = args.model_pricing_input
    pricing_output = args.model_pricing_output

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

    database = ServerDbAPI(args.api_url, args.db_api_key)

    file_hashes = get_hashes(folder_path, prefix_file)
    missing_files = database.get_missing_values(file_hashes)

    for (path, hash_) in missing_files:
        parsed_text = parse_pdf(path)

        # date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(os.path.getmtime(path)))
        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        try:
            json_query = f"{json_prefix}\n{parsed_text}"

            data_1 = llm(llm_client, model, llm_prefix, json_query)
            data = data_1.replace('json', '').replace('```', '')  # Sometimes the LLM uses Markdown

            json_data = json.loads(data)

            num = json_data['Numero']
            name = json_data['Nome']
            destin = json_data['Destinatari']
            classi = json_data['Classi']

            text_query = f"{text_prefix}\n{parsed_text}"

            text = llm(llm_client, model, llm_prefix, text_query)

            if num > 0:  # CIRCOLARI
                database.add_circ(hash_, num, name, date, json.dumps(destin), json.dumps(classi), text)
            else:  # COMUNICAZIONI
                database.add_comm(hash_, name, date, json.dumps(destin), json.dumps(classi), text)

            if pricing_input and pricing_output:  # Calculate cost per document
                input_price = (len(json_query) + len(text_query)) * (float(pricing_input) / 1000000)
                output_price = (len(data_1) + len(text)) * (float(pricing_output) / 1000000)

                print(f"{num} - {name} - {input_price + output_price}$")
            else:
                print(f"{num} - {name}")
        except Exception as e:
            print(e)

    hashes = [hash_ for (_, hash_) in file_hashes]

    # CIRCOLARI
    for circ_hash in database.get_circ_hashes():
        if circ_hash not in hashes:
            database.delete_circ(circ_hash)

    # COMUNICAZIONI
    for com_hash in database.get_comm_hashes():
        if com_hash not in hashes:
            database.delete_comm(com_hash)


if __name__ == "__main__":
    main()
