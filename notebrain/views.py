
from flask.ext.mako import render_template

from notebrain import app


@app.route('/')
def homepage():
    return render_template('homepage.html')
