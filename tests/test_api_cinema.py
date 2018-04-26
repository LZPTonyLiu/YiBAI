from flask import json

from tigereye.helper.code import Code
# .helper 是相对导入
from .helper import FlaskTestCase
# 继承helper里面的类
class TestApiCinema(FlaskTestCase):

    # 我们跑接口的命令是 进入到工程目录下，执行
    # python -m unittest tests/test_api_cinema.py
    # 我们接口方法,名字要呀一样
    def test_cinema_all(self):
        # 这是返回所有的影院
        # response = self.app.get('/cinema/all/')
        # 断言等于 状态吗必须是200
        # self.assertEquals(response.status_code,200)
        # self.assertEquals()
        # 我们更改过JSONEncoder，可以直接loads
        # data = json.loads(response.data)
        # 导入 Code,断言这个rc码必须等于成功
        # self.assertEquals(data['rc'],Code.succ.value)
        # 我们把上面代码直接在helper集成一个方法
        self.get_succ_json('/cinema/all/')

    def test_cinema_halls(self):
        #
        self.assert_get('/cinema/all', 400)
        data = self.get_succ_json('/cinema/all', cid = 1)
        # 这个不应该是空的
        self.assertIsNone(data['data'])

#     我们可以定义不已test方法，这种方法可以被以test方法调用

