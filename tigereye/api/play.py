from flask import request

from tigereye.api import ApiView
from tigereye.extensions.validator import Validator
from tigereye.models.seat import PlaySeat, SeatType


class PlayView(ApiView):

    @Validator(pid = int)
    def seats(self):
        pid = request.params['pid']
        return PlaySeat.query.filter(
            PlaySeat.pid == pid,
            # 这个过道是不能有椅子的，程序里为了构建二维矩阵，我们当road.value = 0就不能售卖
            PlaySeat.seat_type != SeatType.road.value
        ).all()

