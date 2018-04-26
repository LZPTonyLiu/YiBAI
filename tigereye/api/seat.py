from datetime import datetime

from flask import request

from tigereye.api import ApiView
from tigereye.extensions.validator import Validator, multi_int, multi_comlex_int
from tigereye.helper.code import Code
from tigereye.models.order import Order, OrderStatus
from tigereye.models.seat import PlaySeat, SeatType
from flask_classy import route
from tigereye.models.play import Play

class SeatView(ApiView):

    @Validator(pid=int,sid=multi_int,price=int,orderno=str)
    @route('/lock/',methods=['POST'])
    # 这个接口就是我们选座位的时候，我们选择好座位数量和位置后支付的功能
    def lock(self):
        pid = request.params['pid']
        sid = request.params['sid']
        price = request.params['price']
        # 这销售方的订单号，不是我们自己的订单号
        orderno = request.params['orderno']
        play = Play.get(pid)
        # 如果没有这个排期的话，报错
        if not play:
            return Code.play_does_not_exist,request.params
        # 如果售出的价格低于最低价格的话，我们也要报错，电影院私自更改价格
        if price <play.lowest_price:
            return Code.prcice_less_than_the_lowest_price,request.params

        #
        locked_seats_num = PlaySeat.lock(orderno,pid,sid)
        # 如果我们没有锁定成功锁定任何座位，报错
        if not locked_seats_num:
            return Code.seat_lock_failed,{}
        # 创建订单，create 是Order的类方法
        order = Order.create(play.cid, pid, sid)
        # 销售方的订单号
        order.sell_order_no = orderno
        # 这个方法是lock,所以订单的状态是锁定状态
        order.status = OrderStatus.locked.value
        # 座位的个数
        order.tickets_num = locked_seats_num
        order.save()





        return {'locked_seats_num': locked_seats_num}
        # return PlaySeat.query.filter(
        #     PlaySeat.pid == pid,
        #     PlaySeat.seat_type != SeatType.road.value
        # ).all()

    @Validator(pid=int,sid=multi_int,orderno=str)
    @route('/unlock/',methods=['POST'])
    def unlock(self):
        pid = request.params['pid']

        sid = request.params['sid']
        orderno = request.params['orderno']
        play = Play.get(pid)
        if not play:
            return Code.play_does_not_exist, request.params


        # 去order的类里顶一个个
        # 那些销售的电影院是不能拿到我们的这个订单ID的，他们发过来的是他们自己的订单ID
        order = Order.getby_orderno(orderno)
        # 就是这个订单不存在
        if not order:
            return Code.order_does_not_exist, request.params
        # 解锁
        unlock_seats_num = PlaySeat.unlock(orderno, pid, sid)
        # 如果没有返回错误
        if not unlock_seats_num:
            return Code.seat_lock_failed,{}
        order.status = OrderStatus.unlocked.value
        # 这里取消锁座位只是，把销售方的ID给清除掉，然后把座位的status给改掉
        #
        order.save()

        return {'unlock_seats_num': unlock_seats_num}


    # multi_comlex_init
    @Validator(seats=multi_comlex_int, orderno=str)
    @route('/buy/', methods=['POST'])
    def buy(self):
        seats = request.params['seats']
        orderno = request.params['orderno']
        # order = Order.getby_orderno(orderno)
        order = Order.getby_orderno(orderno)
        if not order:
            return Code.order_does_not_exist,request.params

        # 订单的状态只有在锁定的时候,才能下单.
        if order.status != OrderStatus.locked.value:
            return Code.order_status_error,{'orderno':orderno,
                                            'status':order.status,}
        # 获取到order的销售方的订单
        order.sell_order_no = request.params['orderno']
        # 获取order的金额
        order.amount = order.amount or 0
        sid_list = []
        #
        for sid,handle_fee,price in seats:
            # 获取到所有座位
            sid_list.append(sid)
            # 计算订单的总金额
            order.amount += handle_fee +price
        #
        bought_seats_num = PlaySeat.buy(orderno, order.pid, sid_list)
        # 购买失败
        if not  bought_seats_num:
            return Code.seat_buy_failed, {}

        # 票的张数就是座位的个数
        order.tickets_num = len(seats)
        # 下单时间
        order.paid_time = datetime.now()
        # 将status鞭策和国内支付过后的状态
        order.status = OrderStatus.paid.value
        # 生成一个取票码,我们如何生成一个二维码
        order.gen_ticket_flag()
        # 保存
        order.save()
        return {
            'bought_seats_num': bought_seats_num,
            'ticket_flag': order.ticket_flag,
        }










