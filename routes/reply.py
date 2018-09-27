from flask import (
    render_template,
    request,
    redirect,
    session,
    url_for,
    Blueprint,
    make_response,
)


from routes import *

from models.reply import Reply


main = Blueprint('reply', __name__)

@main.route('/add', methods=['POST', 'GET'])
def add():
    form = request.form
    u = current_user()
    print(form)
    m = Reply.new(form)
    m.set_user_id(u.id, form)
    return redirect(url_for('topic.detail', id = m.topic_id))
