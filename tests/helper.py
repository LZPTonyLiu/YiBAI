from unittest import TestCase
from urllib.parse import urlencode

from flask import json
import tigereye
from tigereye.configs.test import Testconfig
from tigereye.helper.code import Code

# 使用unittest自动化测试,测试我们自己的测试用力
class FlaskTestCase(TestCase):
    # 注意U是大写的,做一些测试的准备工作，
    # 我们执行所有的测试用力时候，都要继承TestCase,它规定调用任何调用test方法开头之前，都会先执行setUp，这样不同的方法会又测试数据隔离
    def setUp(self):
        # 使用我们 自己的tigereye导入进来
        # Testconfig 是从configs里导入进来的,用我们自己的Testconfig定义的配置来运行
        # create_app（）方法在 app.py，
        app = tigereye.create_app(Testconfig)
        # 把日志给关了，代码里面所有的logger.info  logger.
        app.logger.disabled = True
        # 这个test_client是flask自己的方法，创建测试客户端
        # 这个有点类似scrapy shell
        # 这个 不用启动服务就能帮我们启动服务,不走网络IO，方便测试我们的代码起作用了
        self.app = app.test_client()
        # 注意这事app,不是self.app，在app_context()里面初始化测试数据
        with app.app_context():
            # 这里从 createdb方法里面的东西拷贝过来
            # 从这里导入db
            from tigereye.models import db
            from tigereye.models.cinerma import Cinema
            from tigereye.models.hall import Hall
            from tigereye.models.movie import Movie
            from tigereye.models.seat import Seat, PlaySeat
            from tigereye.models.play import Play
            from tigereye.models.order import Order
            db.create_all()
            # 生成测试数据,数据随便输入
            # 测试数据
            # 这样执行会快很多，因为不用往数据库里存，没有更多的IO操作
            Cinema.create_test_data(cinema_num=1,hall_num=3,play_num=3)
            # movie不用管
            Movie.create_test_data()

    # uri就是我们要请求的域名后面斜杠的那部分，我们默认给assertcode 200，最后传一堆参数进来。这个方法我们的请求方法
    def assert_get(self,uri, assertcode=200, method = 'GET', **params):
        if method == 'POST':
            # self.app 是一个test.client()
            rv = self.app.post(uri,data=params)
        else:
            # 其实这里逻辑并不是严谨，else:实际上还包含了其他请求，但是我们认为这里全是get请求
            if params:
                # urlencode 把params编码，当成一个url访问
                rv = self.app.get('%s?%s' % (uri,urlencode(params)))
            else:
                rv = self.app.get(uri)
        #         断言 rvstatus_code必须等于assertcode
        self.assertEquals(rv.status_code, assertcode)
        return rv

    def get200(self,uri, method = 'GET', **params):
        return self.assert_get(uri,200,method,**params)

    # 这个它返回的事JSON数据
    def get_json(self,uri,method = 'GET', **params):
        rv = self.get200(uri,method,**params)
        return json.loads(rv.data)


    def get_succ_json(self,uri,method = 'GET',**params):
        #
        data = self.get_json(uri,method,**params)
        #断言 rc一定是 succ.value 为0
        self.assertEquals(data['rc'],Code.succ.value)
        return data

    # Django best prastics
#     drupal 用Django写的一个大的CMS
