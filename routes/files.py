import os
from __main__ import app, morph
from modules.db import BOOKS_FOLDER
from modules.file_parser import parse_file


@app.route('/file/<filename>')
def get_file(filename):
    path = os.path.join(BOOKS_FOLDER, filename)
    text = parse_file(path)
    #text = parse_file(filename)
    return text