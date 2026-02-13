from flask import render_template

from __main__ import app


@app.route('/info')
def info():
    return render_template('info.html')