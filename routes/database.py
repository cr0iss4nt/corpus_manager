import os
from io import BytesIO

from flask import redirect, url_for, render_template, request, send_file

from modules import db
from modules.db import clear_db
from modules.file_parser import parse_file
from __main__ import app, morph


@app.route('/clear')
def clear():
    clear_db()
    return redirect(url_for('index'))

@app.route('/export', methods=['POST'])
def export_corpus():
    try:
        query = request.form['query']
        words, _, _ = db.get_words(query)
        content = db.db_to_text(words)

        from datetime import datetime
        filename = f'corpus_{datetime.today().strftime("%Y%m%d%H%M%S")}.txt'

        file_data = BytesIO(content.encode('utf-8'))

        return send_file(
            file_data,
            as_attachment=True,
            download_name=filename,
            mimetype='text/plain'
        )

    except Exception as e:
        print(f"Export error: {e}")
        return "Error during export", 500

@app.route('/build', methods=['GET'])
def build():
    db.build_corpus(morph)
    return redirect(url_for('index'))