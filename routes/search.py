from flask import render_template, request

from modules.db import get_words, get_word_features, PAGE_LIMIT
from __main__ import app

from modules.frequency_analyzer import analyze_pos_frequency

@app.route('/search/', methods=['POST'])
def search():
    query = request.form['query']
    page = int(request.form['page'])
    words, word_number, lemma_number, result_number, pages_number = get_words(query)
    word_features = get_word_features(words)
    frequency = analyze_pos_frequency(words)
    frequency_middle = (len(frequency)+1)//2
    freq1, freq2 = frequency[:frequency_middle], frequency[frequency_middle:]

    words_start = PAGE_LIMIT * (page-1)
    words_end = words_start + PAGE_LIMIT

    return render_template('search.html',
                           query=query, words=words[words_start:words_end],
                           word_features=word_features[words_start:words_end],
                           word_number=word_number, lemma_number=lemma_number,
                           result_number=result_number, page=page, max_page=pages_number,
                           freq1=freq1, freq2=freq2)