from flask_script import Manager, Server, Shell
from tigereye.app import create_app
from tigereye.models import db

app = create_app()

# 将app进行封装成manager
manager = Manager(app)


# 传入shell里面所有的命令，
def _make_context():
    from tigereye.models.cinerma import Cinema
    from tigereye.models.hall import Hall
    from tigereye.models.movie import Movie
    from tigereye.models.seat import Seat,PlaySeat
    from tigereye.models.play import Play
    from tigereye.models.order import Order
    from tigereye.helper.code import Code
    # locals()是取到上面的所有导入模型，locals返回的是要给字典，上面导入进来的db,app，都是再globals里面，加入之后就可以app,db加入
    locals().update((globals()))
    # 返回一个字典，**可以把变量变成一个字典，如果只串locals可能会有些不安全
    # 用dict(**locals())可以更安全，防止下面的 Shell里面修改locals
    return locals()

manager.add_command('runserver',Server('127.0.0.1',port = 5000))
# 加入这个命令，我们可以在manage.py简化代码，不用再重复写 db.session.add dbsession.commit
# 通过shell源码我们发现，我们要手动传入make_context
manager.add_command('shell',Shell(make_context=_make_context))


@manager.command
def createdb():
    from tigereye.models.cinerma import Cinema
    from tigereye.models.hall import Hall
    from tigereye.models.movie import Movie
    from tigereye.models.seat import Seat, PlaySeat
    from tigereye.models.play import Play
    from tigereye.models.order import Order
    # 这也是db里面的一个方法create_all
    db.create_all()

@manager.command
def dropdb():
    from tigereye.models.cinerma import Cinema
    from tigereye.models.hall import Hall
    from tigereye.models.movie import Movie
    from tigereye.models.seat import Seat, PlaySeat
    from tigereye.models.play import Play
    from tigereye.models.order import Order
    # drop_all这个是通过sql这个包从数据库里删除表
    db.drop_all()

@manager.command
def testdata():
    from tigereye.models.cinerma import Cinema
    from tigereye.models.movie import Movie
    # Cinema.create_test_data()
    Movie.create_test_data()
@manager.command
def init():
    dropdb()
    createdb()
    testdata()



class A(object):
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(A,cls).__new__(cls,*args,**kwargs)
        return cls._instance



if __name__ == '__main__':
    # 可以直接运行
    manager.run()













