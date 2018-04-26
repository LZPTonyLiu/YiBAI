from flask import jsonify, request
from flask_classy import FlaskView

from tigereye.models.cinerma import Cinema
from tigereye.models.hall import Hall
from tigereye.api import ApiView
from tigereye.helper.code import Code
from tigereye.extensions.validator import Validator
from tigereye.models.movie import Movie
from tigereye.models.play import Play

# 我们一开始是继承FlaskView，但是我们要去掉jsonify
class CinemaView(ApiView):
    # 改成all名字，为了保持我们接口的风格
    def all(self):
        cinemas = Cinema.query.all()

        return cinemas

    @Validator(cid=int)
    def get(self):
        # 客户端发送过来请求，获取cid,不可以用request.params（），要用request.args['cid']
        # 在浏览器报错后，可以在浏览器报错行位置输入PIN码，来调试程序
        cid = request.args['cid']
        # 我们在查询数据库模型内容的时候，我们要使用xxx.query.get_or_404(cid)
        # 我们可以去 python manage.py shell 去里面调试，比如添加数据库数据
        cinema = Cinema.query.get_or_404(cid)
        if not cinema:

            return Code.cinema_does_not_exist,request.args
        return cinema

    @Validator(cid=int)
    def halls(self):
        cid = request.params['cid']
        cinema = Cinema.get(cid)
        if not cinema:
            # 同时返回多个参数的时候，就相当于返回一个元组，这里面的这些
            return Code.cinema_does_not_exist,request.args
        # 查询数据库中的hall表，我们把一个电影下面的所有影厅都查询出来
        cinema.halls = Hall.query.filter_by(cid = cid).all()
        return cinema


    @Validator(cid=int)
    def plays(self):
        # 这里的request.params其实是自定义装饰器里面的给request自定义的
        # 正常情况下都是用，request.args['cid']来获取
        cid = request.params['cid']
        cinema = Cinema.get(cid)
        if not cinema:
            # 返回多个参数就是组成了一个元组
            return Code.cinema_does_not_exist, request.args
        # 获取cinema里面的所有排期
        cinema.plays = Play.query.filter_by(cid=cid).all()
        # 对所有的排期进行遍历
        for  play in cinema.plays:
            # 把排期每个排期的电影获取到
            play.movie = Movie.get(play.mid)
        #     这里的return 还没又交给框架处理，还是我们自定义插件在处理
        return cinema.plays





