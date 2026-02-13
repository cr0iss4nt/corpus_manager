import os

import pymorphy3
from flask import Flask

from modules.db import init_db

init_db()
morph = pymorphy3.MorphAnalyzer()

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

import routes.index
import routes.database
import routes.search
import routes.info


if __name__ == '__main__':
    app.run(debug=True)