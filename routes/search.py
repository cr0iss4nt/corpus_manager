from flask import render_template, request

from modules.db import get_words, get_word_features, PAGE_LIMIT
from __main__ import app

from modules.frequency_analyzer import analyze_pos_frequency

@app.route('/search/', methods=['POST'])
def search():
    query = request.form['query']
    page = int(request.form['page'])
    words, word_number, lemma_number, result_number = get_words(query, page)
    word_features = get_word_features(query, page)
    frequency = analyze_pos_frequency(query)
    frequency_middle = (len(frequency)+1)//2
    freq1, freq2 = frequency[:frequency_middle], frequency[frequency_middle:]

    max_page = result_number // PAGE_LIMIT + 1

    return render_template('search.html',
                           query=query, words=words, word_features=word_features,
                           word_number=word_number, lemma_number=lemma_number,
                           result_number=result_number, page=page, max_page=max_page,
                           freq1=freq1, freq2=freq2)