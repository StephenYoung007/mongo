from models import Model
import time

class Reply(Model):
    __fields__ = Model.__fields__ + [
        ('content', str, ''),
        ('topic_id', int, -1),
        ('user_id', int, -1),
        ('receiver_id', int, -1)
    ]


    def user(self):
        from .user import User
        u = User.find(self.user_id)
        return u

    def set_user_id(self, user_id, form):
        self.user_id = user_id
        self.topic_id = int(form.get('topic_id', -1))
        self.save()