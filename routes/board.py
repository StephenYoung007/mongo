from flask import (
    render_template,
    request,
    redirect,
    session,
    url_for,
    Blueprint,
    make_response,
    abort,
)

from models.board import Board
from routes import *


main = Blueprint('board', __name__)


@main.route('/admin')
def index():
    return render_template('board/admin_index.html')


@main.route('/add', methods=['POST'])
def add():
    u = current_user()
    if u.username != 'admin':
        return redirect(url_for('index.index'))
    else:
        form = request.form
        Board.new(form)
        return redirect(url_for('.index'))
