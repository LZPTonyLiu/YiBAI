from logging.handlers import SMTPHandler

from flask import Flask
import logging

from flask_classy import FlaskView

from tigereye.models import db, JSONEncoder
from logging import FileHandler, Formatter
import os


# 创建app,导入到manage.py里面
# def create_app(debug=True):
# 我们把参数改了成 config = None
def create_app(config = None):
    app = Flask(__name__)
    # app.debug = debug
    # 从这个后面这个类里读取配置，我们创建configs包，我们这样可以实现配置隔离
    app.config.from_object('tigereye.configs.default.DefalutConfig')
    # 改了传入参数的 config
    app.config.from_object(config)

    # 我们把app的json_encoder 指向了我们自己定义的JSONEncoder，如果不定义的话指向flask
    app.json_encoder = JSONEncoder

    # 不是在debug模式下
    if not app.debug:
        # 我们把日志级别设置成INFO
        app.logger.setLevel(logging.INFO)
        # SMTPHandler这也是logging里面的一个东西
        mail_handler = SMTPHandler(
            app.config['EMAIL_HOST'],
            app.config['SERVER_EMAIL'],
            # app.config['EMAIL_PORT'],
            app.config['ADMINS'],
            # 邮件的主题
            'TIGEREYE ALERT',
            # 这个是验证信息，是要给元组
            credentials = (
                app.config['EMAIL_HOST_USER'],
                app.config['EMAIL_HOST_PASSWORD']
            )
        )
        # 设置日志级别，我们要把日志级别设置高一点，只有报错的时候才给我们发邮件
        mail_handler.setLevel(logging.ERROR)
        # 设置形式，三个引号的字符串来定义
        mail_handler.setFormatter(Formatter('''
        Message Type: %(levelname)s
        Location:     %(pathname)s: %(lineno)d
        Module:       %(module)s
        Function:     %(funcName)s
        Time:         %(asctime)s
        
        Message:
        
        
        %(message)s
        '''))
        # 加入到app.logger里面去
        app.logger.addHandler(mail_handler)



        # os,path.config 所有的日志都会走到 app.log里面
        file_handler = FileHandler(os.path.join(app.config['LOG_DIR'],'app.log'))
        file_handler.setLevel(logging.INFO)
        # 这个是个formatter对象，
        file_handler.setFormatter(Formatter(
            # 时间，级别，内容
            '%(asctime)s %(levelname)s : %(message)s'
        ))
        # 再创建对象的时候，他就会把日志打印到相应文件中去,app.log
        app.logger.addHandler(file_handler)

    # 这句话其实就是读取 我们app里面config配置
    db.init_app(app)

    # 这就是把所有的AIP的接口直接全部注册到app里面
    configure_views(app)
    app.logger.info('create_app_text')
    return app



def configure_views(app):
    from tigereye.api.movie import MovieView
    from tigereye.api.cinema import CinemaView
    from tigereye.api.misc import MiscView
    from tigereye.api.hall import HallView
    from tigereye.api.play import PlayView
    from tigereye.api.seat import SeatView
    from tigereye.api.order import OrderView

    # 获取configure_views函数下面作用域里面所有的导入类
    for view in locals().values():
        print(type(view))
        print(type)
        print(type(app))
        # issubclass是判断前面的参数是不是后面参数的子类
        # type是所有类的超类，可以用type来动态创建类
        if type(view) == type and issubclass(view, FlaskView):
            view.register(app)
    # MiscView.register(app)
    # CinemaView.register(app)
    # MovieView.register(app)

#
# @app.route('/check/')
# def hello_world():
#     return 'Hello World!'


# if __name__ == '__main__':
#     app.run()
