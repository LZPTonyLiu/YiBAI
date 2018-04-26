from flask import jsonify, request
from flask_classy import FlaskView

from tigereye.models.cinerma import Cinema
from tigereye.models.hall import Hall
from tigereye.models.seat import Seat
from tigereye.helper.code import Code

from tigereye.api import ApiView
from tigereye.helper.code import Code

class HallView(ApiView):

    def seats(self):

        # 获取影厅的id
        hid = request.args.get('hid')
        # 取出影厅
        hall = Hall.get(hid)
        if not hall:
            return Code.hall_seats_does_not_exist,request.args
        # 获取这个影厅下的所有座位
        hall.seats = Seat.query.filter_by(hid = hid).all()
        return hall
    # 每次写完一个API我们都要去app.py去注册，但是这样太麻烦，我们就要顶一个方法
    # configure_view(app)

