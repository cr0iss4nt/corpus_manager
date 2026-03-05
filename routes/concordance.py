from flask import render_template, request

from modules.db import get_concordance
from __main__ import app



@app.route('/concordance/', methods=['POST'])
def search_inclusions():
    query = request.form['concordance_query']
    search_query = request.form['query']
    concordance = get_concordance(query)
    return render_template('concordance.html',
                           concordance_query=query, query = search_query, concordance=concordance)