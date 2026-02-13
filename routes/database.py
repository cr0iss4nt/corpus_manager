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

"""
@app.route('/add-word', methods=['POST'])
def add_word():
    word = request.form['word']
    db.add_word(word, morph)
    return redirect(url_for('index'))

@app.route('/edit/<word>')
def edit(word):
    return render_template('edit_word.html', word=word)

@app.route('/edit-word', methods=['POST'])
def edit_word():
    word = request.form['word']
    base = request.form['base']
    ending = request.form['ending']
    db.edit_word(word, base, ending)
    return redirect(url_for('index'))

@app.route('/delete-word/<word>')
def delete_word(word):
    db.delete_word(word)
    return redirect(url_for('index'))

@app.route('/import', methods=['GET', 'POST'])
def fill():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file uploaded', 400

        file = request.files['file']

        if file.filename == '':
            return 'No file selected', 400

        allowed_extensions = ['.txt', '.rtf']
        file_ext = os.path.splitext(file.filename)[1].lower()
        if file_ext not in allowed_extensions:
            return 'Invalid file type. Only .txt and .rtf files are allowed.', 400

        try:
            temp_filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(temp_filename)

            text = parse_file(temp_filename)
            db.add_words_from_text(text, morph)

            if os.path.exists(temp_filename):
                os.remove(temp_filename)

            return redirect(url_for('index'))

        except Exception as e:
            if os.path.exists(temp_filename):
                os.remove(temp_filename)
            app.logger.error(f'Error processing file: {str(e)}')
            return f'Error processing file: {str(e)}', 500

    return redirect(url_for('index'))
"""

@app.route('/export')
def export_dictionary():
    try:
        content = db.db_to_text()

        from datetime import datetime
        filename = f'dictionary_{datetime.today().strftime("%Y%m%d%H%M%S")}.txt'

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