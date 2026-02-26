from flask import render_template, request

from modules.db import get_words, get_word_features
from __main__ import app

from modules.frequency_analyzer import analyze_pos_frequency, split_dict


@app.route('/search/', methods=['POST'])
def search():
    query = request.form['query']
    words, word_number, lemma_number, result_number  = get_words(query)
    word_features = get_word_features(query)
    frequency = analyze_pos_frequency(words)
    freq1, freq2 = split_dict(frequency)
    return render_template('search.html',
                           query=query, words=words, word_features=word_features,
                           word_number=word_number, lemma_number=lemma_number,
                           result_number=result_number,
                           freq1=freq1, freq2=freq2)