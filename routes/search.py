from flask import render_template, redirect, url_for, request

from modules.db import get_words
from __main__ import app

from modules.frequency_analyzer import analyze_pos_frequency, split_dict


@app.route('/search/', methods=['POST'])
def search():
    query = request.form['query']
    result, word_number, lemma_number  = get_words(query)
    frequency = analyze_pos_frequency(result)
    freq1, freq2 = split_dict(frequency)
    return render_template('search.html',
                           query=query, words=result,
                           word_number=word_number, lemma_number=lemma_number,
                           result_number=len(result),
                           freq1=freq1, freq2=freq2)