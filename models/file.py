from models import Model

class File(Model):
    __fields__ = Model.__fields__ + [
        ('filename', str, ''),
        ('user_id', int, ''),
        ('type', str, ''),
    ]
