from __main__ import app

from flask import render_template

from modules import db

@app.route('/abnormal-words')
def get_abnormal_words():
    abnormal_words = db.get_abnormal_words()
    return render_template('abnormal_words.html', words=abnormal_words,
                           result_number=len(abnormal_words))