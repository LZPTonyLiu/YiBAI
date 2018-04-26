from flask_sqlalchemy import SQLAlchemy
from flask import json as _json

db = SQLAlchemy()


# 我们在shell使用时候，我们不用db.session
class Model(object):
    # 代码里面不用
    @classmethod
    def get(cls,primary_key):
        return cls.query.get(primary_key)

    def put(self):
        db.session.add(self)

    @classmethod
    def commit(cls):
        db.session.commit()

    @classmethod            #变成类方法，的原因是可以一次提交多个实例对象，减少IO操作
    def rollback(cls):
        db.session.rollback()


    def delete(self):
        db.session.delete(self)


    def save(self):
        try:
            self.put()
            self.commit()

        except Exception:
            self.rollback()
            raise

    def __json__(self):
        # 获取模型所有的字段
        keys = vars(self).keys()
        data = {}
        print(keys)
        for key in keys:
            # 过滤掉所有的 私有字段
            if not key.startswith('_'):
                # getattr  获取对象的属性 相当于self.key，有时候后面的方法是动态的，是变量
                # setattr 设置对象的时候用法，setattr(self,'json_encoder', JSONEncoder)
                data[key] = getattr(self,key)
        return data

# 这个其实就是复写了flask里面的JsonEncoder
class JSONEncoder(_json.JSONEncoder):

    def default(self,o):
        if isinstance(o,db.Model):
            return o.__json__()
        return _json.JSONEncoder.default(self,o)

