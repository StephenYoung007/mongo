from models import Model
from models.user import User
import time


class Topic(Model):
    __fields__ = Model.__fields__ + [
        ('title', str, ''),
        ('views', int, 0),
        ('content', str, ''),
        ('user_id', '', -1),
        ('board_id', '', -1)
    ]

    @classmethod
    def get(cls, id):
        m = cls.find_by(id = id)
        m.views += 1
        m.save()
        return m


    def replies(self):
        from .reply import Reply
        ms = Reply.find_all(topic_id = self.id)
        return ms


    def reply_delete(self):
        ms = self.replies()
        for m in ms:
            m.delete()


    def board(self):
        from .board import Board
        m = Board.find(id=self.user_id)

    def user(self):
        u = User.find(id=self.user_id)


