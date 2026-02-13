from flask import render_template, redirect, url_for, request

from modules.db import get_words
from __main__ import app


@app.route('/search/', methods=['POST'])
def search():
    query = request.form['query']
    result, word_number, lemma_number  = get_words(query)
    return render_template('search.html',
                           query=query, words=result,
                           word_number=word_number, lemma_number=lemma_number,
                           result_number=len(result))