from flask import (
    render_template,
    request,
    redirect,
    session,
    url_for,
    Blueprint,
    make_response,
    send_from_directory,
)

from models.user import User
from routes import *
import os
from models.file import File
from config import user_file_directory, data_file_directory


main = Blueprint('drive', __name__)


@main.route('/')
def index():
    # u = current_user()
    fs = File.all()
    return render_template('/drive/index.html', fs=fs)


@main.route('/upload', methods=["POST"])
def file_upload():
    u = current_user()
    if u is None:
        redirect(url_for(".profile"))

    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)

    filename = file.filename
    file.save(os.path.join(data_file_directory, filename))
    f = File.new()
    f.filename = filename
    f.user_id = u.id
    f.type = filename.split('.')[-1]
    f.save()
    return redirect(url_for('.index'))


@main.route('/all', methods=['Post'])
def all_file():
    return redirect(url_for('.index'))


@main.route('/my', methods=['Post'])
def my_file():
    u = current_user()
    fs = File.find_all(user_id = u.id)
    return render_template('/drive/index.html', fs=fs)