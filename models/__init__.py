# import json
import time
from pymongo import MongoClient

stephen = MongoClient()


def time_stamp():
    return int(time.time())


# Model 是一个 ORM（object relation mapper）
# 好处就是不需要关心存储数据的细节，直接使用即可
def next_id(name):
    query = {
        'name': name,
    }
    update = {
        '$inc': {
            'seq': 1,
        }
    }
    kwargs = {
        'query': query,
        'update': update,
        'upsert': True,
        'new': True,
    }
    doc = stephen.db['data_id']
    new_id = doc.find_and_modify(**kwargs).get('seq')


class Model(object):
    '''
    contains all of the public attribute
    '''
    __fields__ = [
        '_id',
        ('id', int, -1),
        ('type', str, ''),
        ('deleted', bool, False),
        ('created_time', int, 0),
        ('updated_time', int, 0),
    ]
    """
    Model 是所有 model 的基类
    @classmethod 是一个套路用法
    例如
    user = User()
    user.db_path() 返回 User.txt
    """


    @classmethod
    def _find(cls, **kwargs):
        name = cls.__name__
        flag_sort = '__sort'
        sort = kwargs.pop(flag_sort, None)
        ds = stephen.db[name].find(kwargs)
        if sort is not None:
            ds = ds.sort(sort)
        l = [cls._new_with_bson(d) for d in ds]
        return l


    @classmethod
    def has(cls, **kwargs):
        return cls.find_one(**kwargs) is not None


    def mongos(self, name):
        return stephen.db[name]._find()


    @classmethod
    def all(cls):
        return cls._find()


    @classmethod
    def find_raw(cls, **kwargs):
        name = cls.__name__
        ds = stephen.db[name]._find(kwargs)
        l = [d for d in ds]
        return l


    @classmethod
    def _clean_field(cls, source, target):
        ms = cls._find()
        for m in ms:
            v = getattr(m, source)
            setattr(m, target, v)
            m.save()

    @classmethod
    def find_all(cls, **kwargs):
        return cls._find(**kwargs)

    @classmethod
    def find_by(cls, **kwargs):
        return cls.find_one(**kwargs)

    @classmethod
    def find(cls, id):
        return cls.find_by(id=id)

    @classmethod
    def get(cls, id):
        return cls.find_by(id=id)


    def delete(self):
        name = self.__class__.__name__
        query = {
            'id': self.id,
        }
        values = {
            'deleted': True,
        }
        stephen.db[name].update_one(query, values)



    def __repr__(self):
        """
        __repr__ 是一个魔法方法
        简单来说, 它的作用是得到类的 字符串表达 形式
        比如 print(u) 实际上是 print(u.__repr__())
        """
        classname = self.__class__.__name__
        properties = ['{}: ({})'.format(k, v) for k, v in self.__dict__.items()]
        s = '\n'.join(properties)
        return '< {}\n{} \n>\n'.format(classname, s)


    @classmethod
    def new(cls, form=None, **kwargs):
        name = cls.__name__
        m = cls()
        fields = m.__fields__.copy()
        fields.remove('_id')
        if form is None:
            form = {}

        for f in fields:
            k, t, v = f
            if k in form:
                setattr(m, k, form[k])
            else:
                setattr(m, k, v)
        for k, v in kwargs.items():
            if hasattr(m, k):
                setattr(m, k, v)
            else:
                raise KeyError

        m.id = next_id(name)
        ts = time_stamp()
        m.created_time = ts
        m.updated_time = ts
        m.type = name.lower()
        m.save()
        return m

    def save(self):
        models = self.all()
        if self.id is None:
            if len(models) == 0:
                self.id = 1
            else:
                m = models[-1]
                self.id = m.id + 1
            models.append(self)
        else:
            index = -1
            for i, m in enumerate(models):
                if m.id == self.id:
                    index = i
                    break
            models[index] = self
        l = [m.__dict__ for m in models]
        name = self.__class__.__name__
        stephen.db[name].save(self.__dict__)

    @classmethod
    def _new_with_bson(cls, bson):
        m = cls()
        fields = m.__fields__.copy()
        fields.remove('_id')
        for f in fields:
            k, t, v = f
            if k in bson:
                setattr(m, k, bson[k])
            else:
                setattr(m, k, v)
        setattr(m, '_id', bson['_id'])
        m.type = cls.__name__.lower()
        return m

    @classmethod
    def find_one(cls, **kwargs):
        l = cls._find(**kwargs)
        if len(l) > 0:
            return l[0]
        else:
            return None


    @classmethod
    def upsert(cls, query_form, update_form, hard=False):
        ms = cls.find_one(**query_form)
        if ms is None:
            query_form.update(**update_form)
            ms = cls.new(query_form)
        else:
            ms.update(update_form, hard=hard)
        return ms

    def update(self, form, hard=False):
        for k, v in form.items():
            if hard or hasattr(self, k):
                setattr(self, k, v)
        self.save()


    def json(self):
        _dict = self.__dict__
        d = {k: v for k, v in _dict.items() if k not in self.black_list()}
        return d


    def black_list(self):
        b = [
            '_id',
        ]
        return b


    def data_count(self, cls):
        name = cls.__name__
        fk = '{}_id'.format((self.__class__.__name__.lower()))
        query = {
            fk: self.id,
        }
        count = stephen.db[name]._find(query).count()
        return count
