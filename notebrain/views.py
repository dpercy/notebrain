
from flask import g, redirect, request, url_for
from flask.ext.mako import render_template
from werkzeug.exceptions import NotFound

from notebrain import app

from .models import Note
from .util import UUIDConverter

app.url_map.converters['uuid'] = UUIDConverter


@app.route('/')
def homepage():
    return render_template('homepage.html')



@app.route('/notes/new')
@app.route('/notes/<uuid:id>')
def note_view(id=None):
    if id is None:
        note = Note(id = None)
    else:
        note = Note.objects.get_or_404(
            owner = g.user,
            id = id,
        )
    return render_template('note_view.html', note=note)

@app.route('/save_note', methods=['POST'])
def note_save():
    if request.form['id']:
        note = Note.objects.get_or_404(
            owner = g.user,
            id = request.form['id'],
        )
    else:
        note = Note(owner=g.user)

    note.html = request.form['html']
    note.save()
    return redirect(url_for('note_view', id=n.id))
