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

from models.topic import Topic
from models.user import User
from models.board import Board

from routes import *


main = Blueprint('topic', __name__)

import uuid
csrf_tokens = []


@main.route('/')
def index():
    ms = Topic.all()
    token = str(uuid.uuid4())
    csrf_tokens.append(token)
    return render_template('/topic/index.html', ms=ms, token=token)


@main.route('/new', methods=['GET'])
def new():
    bs = Board.all()
    u = current_user()
    if u is None:
        return redirect(url_for('index.index'))
    else:
        return render_template('/topic/new.html', bs=bs)

@main.route('/add', methods=['POST'])
def add():
    form = request.form
    u = current_user()
    Topic.new(form, user_id = u.id)
    return redirect(url_for('.index'))

@main.route('/delete', methods=['GET'])
def delete():
    u = current_user()
    user_id = u.id
    id = int(request.args.get('topic_id', -1))
    t = Topic.find(id)
    author_id = t.user_id
    if user_id == author_id:
        token = request.args.get('token', '')
        if token in csrf_tokens:
            Topic.delete(id)
            t.reply_delete()
            csrf_tokens.remove(token)
            return redirect(url_for('.index'))
        else:
            abort(403)
    else:
        return redirect(url_for('index.index'))


@main.route('/detail/<int:id>')
def detail(id):
    m = Topic.get(id)
    user_id = m.user_id
    u = User.get(user_id)
    b = Board.find(int(m.board_id))
    return render_template('/topic/detail.html', topic=m, user=u, board_title=b.title)
