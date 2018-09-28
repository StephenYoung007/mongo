from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
)


from models.todo import Todo

main = Blueprint('todo', __name__)

@main.route('/')
def index():
    todo_list = Todo.all()
    return render_template('todo_index.html', todos=todo_list)

@main.route('/add', methods=['POST', 'GET'])
def add():
    if request.method == 'GET':
        return redirect(url_for('todo.index'))
    form = request.form
    t = Todo.new(form)
    t.save()
    return redirect(url_for('todo.index'))

@main.route('/delete/<todo_id>/')
def delete(todo_id):
    t = Todo.find_one(id=int(todo_id))
    print(t.id)
    t.delete()
    return redirect(url_for('.index'))
