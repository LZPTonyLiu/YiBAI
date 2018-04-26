from flask import json

from tigereye.helper.code import Code
from tigereye.models.seat import SeatStatus
from .helper import FlaskTestCase

# 这是我们传的参数
pid = 1
sid_list = [1,2]

sid = ','.join([str(i) for i in sid_list])
price = 5000
orderno = 'test-%s-%s'  %(pid,sid)

# python -m unittest tests/test_api_seat.py  运行
class TestApiSeat(FlaskTestCase):
    def test_seat_num (self):

        locked_seats_num = len(sid_list)
        rv = self.get_succ_json('/seat/lock/',method='POST',
                            orderno = orderno,
                            pid = pid,
                            sid = sid,
                            price = price)
    #     这个锁座长度 必须等于作为列表长度
        self.assertEquals(rv['data']['locked_seats_num'], locked_seats_num)
        # 作为锁定成功，数据写入数据库
        rv = self.get_succ_json('/play/seats',pid = pid)
        succ_count = 0

        for seat in rv['data']:
            # 如果

            if seat['orderno'] == orderno:
                # 断言如果作为状态等于锁定后的CODE，成功
                self.assertEquals(seat['status'],SeatStatus.locked.value)
                #
                succ_count += 1
        self.assertEquals(succ_count, locked_seats_num)

        # 确定重复锁定会失败
        rv = self.get_json(
            '/seat/lock/',
            method='POST',
            orderno = orderno,
            pid = pid,
            sid = sid,
            price = price
        )
        self.assertEquals(rv['rc'],Code.seat_lock_failed.value)



    #测试驱动开发
    # pip show flask-classy
    # pip install -U flask-class  更新