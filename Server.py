from flask import Flask, render_template, request, redirect
from PDF_Parsing import parse_pdf
from Db_Table import DbTable
from datetime import datetime
import tempfile
import os
import hashlib

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])  # when a file is uploaded
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)  # reload page
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)  # reload page
    if file:
        temp_file = tempfile.NamedTemporaryFile(delete=False)  # make a temp file to store the PDF
        temp_file_path = temp_file.name

        file.save(temp_file_path)

        file_hash = hashlib.sha256()

        with open(temp_file_path, 'rb') as f:
            while True:
                data = f.read(65536)  # read file in 64kb parts
                if not data:
                    break
                file_hash.update(data)

        date = datetime.now().strftime("%Y-%m-%d %H:%M")
        hash_string = file_hash.hexdigest()

        database = DbTable(os.environ[db_path_variable])

        if not database.contains_hash(hash_string):  # parse and add file to db if not already parsed
            parsed_text = parse_pdf(temp_file_path, "Tabella")
            database.add_row(file.filename, date, hash_string, parsed_text)

        database.close_connection()  # save and close db

        temp_file.close()
        os.remove(temp_file_path)

        return 'file parsed'


db_path_variable = 'DB_PATH'

if __name__ == '__main__':
    app.run(debug=False, host="0.0.0.0")
