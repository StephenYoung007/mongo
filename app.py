from flask import Flask

import config

app = Flask(__name__)

app.secret_key = config.secret_key


from routes.index import main as index_routes
app.register_blueprint(index_routes)
from routes.topic import main as topic_routes
app.register_blueprint(topic_routes, url_prefix='/topic')
from routes.todo import main as todo_routes
app.register_blueprint(todo_routes, url_prefix='/todo')
from routes.reply import main as reply_routes
app.register_blueprint(reply_routes, url_prefix='/reply')
from routes.board import main as board_routes
app.register_blueprint(board_routes, url_prefix='/board')
from routes.mail import main as mail_routes
app.register_blueprint(mail_routes, url_prefix='/mail')
from routes.drive import main as drive_routes
app.register_blueprint(drive_routes, url_prefix='/drive')


if __name__ == '__main__':
    config = dict(
        debug=True,
        host='0.0.0.0',
        port=2000,
    )
    app.run(**config)