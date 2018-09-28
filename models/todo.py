import time
from models import Model


# 针对我们的数据 TODO
# 我们要做 4 件事情
"""
C create 创建数据
R read 读取数据
U update 更新数据
D delete 删除数据

Todo.new() 来创建一个 todo
"""
class Todo(Model):
    __fields__ = Model.__fields__ + [
        ('todo_content', str, ''),
    ]



    # @classmethod
    # def update(cls, id, form):
    #     t = cls.find(id)
    #     valid_names = [
    #         'title',
    #         'completed'
    #     ]
    #     for key in form:
    #         if key in valid_names:
    #             setattr(t, key, form[key])
    #     t.save()
    #     return t

    @classmethod
    def complete(cls, id, completed=True):
        """
        Todo.complete(1)
        Todo.complete(2, False)
        """
        t = cls.find(id)
        t.completed = completed
        t.save()
        return t

