import datetime
import hashlib
import json
import os
import traceback
import logging

from PyPDF2 import PdfReader
from openai import OpenAI

from Server_db_API import ServerDbAPI


def parse_pdf(file_path):
    reader = PdfReader(file_path)

    all_text = ''
    for page in reader.pages:
        all_text += page.extract_text()

    return all_text


def get_hashes(path, extension):
    hashes = []
    added_hashes = []

    for file in os.listdir(path):
        name = os.fsdecode(file)
        if name.lower().endswith(extension):
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
    with open("files/config.json", "r") as config_file:
        config = json.load(config_file)

    logger = logging.getLogger(__name__)
    logging.basicConfig(filename='files/log.txt',
                        encoding='utf-8',
                        filemode='a',
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        datefmt='%H:%M:%S',
                        level=logging.INFO)

    try:
        job_config = config["config"]
        llm_config = config["llm_prefix"]

        folder_path = job_config["folder_path"]
        api_url = job_config["api_url"]
        db_api_key = job_config["db_api_key"]
        api_key = job_config["api_key"]
        model = job_config["model"]
        pricing_input = job_config.get("model_pricing_input", None)
        pricing_output = job_config.get("model_pricing_output", None)

        llm_prefix = llm_config["prefix"]
        json_prefix = llm_config["json_prefix"]
        text_prefix = llm_config["text_prefix"]
    except Exception as ex:
        logger.error(traceback.format_exc())
        raise ex

    try:
        llm_client = OpenAI(api_key=api_key)
        database = ServerDbAPI(api_url, db_api_key)

        file_hashes = get_hashes(folder_path, ".pdf")
        missing_files = database.get_missing_values(file_hashes)
    except Exception as ex:
        logger.error(traceback.format_exc())
        raise ex

    for (path, hash_) in missing_files:
        try:
            parsed_text = parse_pdf(path)

            # date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(os.path.getmtime(path)))
            date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            json_query = f"{json_prefix}\n{parsed_text}"

            data_1 = llm(llm_client, model, llm_prefix, json_query)
            data = data_1.replace('json', '').replace('```', '')  # Sometimes the LLM uses Markdown

            print(data)

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

                logger.info(f"{num} - {name} - {input_price + output_price}$")
                print(f"{num} - {name} - {input_price + output_price}$")
            else:
                logger.info(f"{num} - {name}")
                print(f"{num} - {name}")
        except:
            logger.error(traceback.format_exc())

    hashes = [hash_ for (_, hash_) in file_hashes]

    try:
        # CIRCOLARI
        for circ_hash in database.get_circ_hashes():
            if circ_hash not in hashes:
                database.delete_circ(circ_hash)
    except:
        logger.error(traceback.format_exc())

    try:
        # COMUNICAZIONI
        for com_hash in database.get_comm_hashes():
            if com_hash not in hashes:
                database.delete_comm(com_hash)
    except:
        logger.error(traceback.format_exc())


if __name__ == "__main__":
    main()
