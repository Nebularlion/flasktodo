from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session
)
from werkzeug.exceptions import abort

from flasktodo.auth import login_required
from flasktodo.db import get_db

bp = Blueprint('todolist', __name__)

@bp.route('/')
def index():

    user_id = session.get('user_id')
    db = get_db()
    todos = db.execute(
        ' SELECT t.id, todotitle, tododescription, created, author_id, username '
        ' FROM todo t JOIN user u ON t.author_id = u.id '
        ' WHERE t.author_id = ?'
        ' ORDER BY created DESC',
        (user_id,)
    ).fetchall()
    return render_template('todolist/index.html', todos = todos)


def get_todo(id, check_author = True):

    todo = get_db().execute(
        'SELECT t.id, todotitle, tododescription, created, author_id, username'
        ' FROM todo t JOIN user u ON t.author_id = u.id'
        ' WHERE t.id = ?',
        (id,)
    ).fetchone()

    return todo

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create_todo():
    if request.method == 'POST':
        todotitle = request.form['todotitle']
        tododescription = request.form['tododescription']
        error = None

        if not todotitle:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO todo (todotitle, tododescription, author_id)'
                ' VALUES (?, ?, ?)',
                (todotitle, tododescription, g.user['id'])
            )
            db.commit()
            return redirect(url_for('todolist.index'))

    return render_template('todolist/create.html')


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update_todo(id):
    todo = get_todo(id)

    if request.method == 'POST':
        todotitle = request.form['todotitle']
        todotext = request.form['tododescription']
        error = None

        if not title:
            error = 'Title is empty'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE todo SET todotitle = ?, tododescription = ? WHERE id = ?',
                (todotitle, tododescription, id)
            )
            db.commit()
            return redirect(url_for('todolist.index'))

    return render_template('todolist/update.html', todo=todo)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete_todo(id):
    get_todo(id)
    db = get_db()
    db.execute('DELETE FROM todo WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('todolist.index'))
