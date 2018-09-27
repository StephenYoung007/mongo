from models import Model
import time


class Board(Model):
    __fields__ = Model.__fields__ + [
        ('title', str, '')
    ]