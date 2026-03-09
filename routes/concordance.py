from flask import render_template, request

from modules.db import get_concordance
from __main__ import app



@app.route('/concordance/', methods=['POST'])
def search_inclusions():
    query = request.form['concordance_query']
    book = request.form['book']
    search_query = request.form['query']
    page = request.form['page']
    is_search = int(request.form['is_search'])
    concordance = get_concordance(query, book)
    return render_template('concordance.html',
                           concordance_query=query, query=search_query,
                           book=book, concordance=concordance, page=page,
                           is_search=is_search)