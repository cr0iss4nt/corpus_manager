from flask import render_template, request

from modules.db import get_words, get_word_features
from __main__ import app

from modules.frequency_analyzer import analyze_pos_frequency, split_dict

PAGE_LIMIT = 100

@app.route('/search/', methods=['POST'])
def search():
    query = request.form['query']
    page = int(request.form['page'])
    words, word_number, lemma_number, result_number  = get_words(query)
    word_features = get_word_features(query)
    frequency = analyze_pos_frequency(words)
    freq1, freq2 = split_dict(frequency)

    first_id = PAGE_LIMIT * (page - 1)
    last_id = first_id + PAGE_LIMIT

    max_page = len(words) // PAGE_LIMIT + 1

    return render_template('search.html',
                           query=query, words=words[first_id:last_id], word_features=word_features[first_id:last_id],
                           word_number=word_number, lemma_number=lemma_number,
                           result_number=result_number, page=page, max_page=max_page,
                           freq1=freq1, freq2=freq2)