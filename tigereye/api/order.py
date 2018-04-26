from datetime import datetime

from flask import request

from tigereye.api import ApiView
from tigereye.extensions.validator import Validator, multi_int, multi_comlex_int
from tigereye.helper.code import Code
from tigereye.models.movie import Movie
from tigereye.models.order import Order, OrderStatus
from tigereye.models.seat import PlaySeat, SeatType
from flask_classy import route
from tigereye.models.play import Play


class OrderView(ApiView):

    # 退票的方法
    # 设置路径,url和方法名字不一样,请求方式POST
    @route('/refund/',methods = ['POST'])
    @Validator(orderno=str, ticket_flag = str, sid = multi_int)
    def refund_ticket(self):
        orderno = request.params['orderno']
        ticket_flag = request.params['ticket_flag']
        seats = request.params['sid']

        order = Order.getby_orderno(orderno)
        if not order:
            return Code.order_does_not_exist, {'orderno':orderno}
        # 如果已经去取过票了,我们就不能退票了
        if order.status == OrderStatus.printed.value:
            return Code.ticket_printed_already,{}
        # 必须是已经付过钱的才能退票
        if order.status != OrderStatus.paid.value:
            return Code.order_not_paid_yet, {}
        # 取票码错误,也不能退票
        if not order.validate(ticket_flag):
            return Code.ticket_flag_error,{'ticket_flag': ticket_flag}
        #
        refund_num = PlaySeat.refund(orderno,order.pid,seats)
        # 如果没有这需要退票的订单,退票失败
        if not refund_num:
            return Code.ticket_refund_failed, {}
        order.status = OrderStatus.refund.value
        order.refund_time = datetime.now()
        order.save()
        # refund_num 是退票的数量.
        return {'refund_num': refund_num}

    @route('/ticket/print/', methods=['POST'])
    @Validator(orderno=str, ticket_flag=str, sid=multi_int)
    def print_ticket(self):
        orderno = request.params['orderno']
        ticket_flag = request.params['ticket_flag']
        seats = request.params['sid']
        # 根据订单号来获取订单
        order = Order.getby_orderno(orderno)
        if not order:
            return Code.order_does_not_exist, {'orderno': orderno}
        if order.status == OrderStatus.printed.value:
            return Code.ticket_printed_already, {}
        if order.status != OrderStatus.paid.value:
            return Code.order_not_paid_yet, {}
        if not order.validate(ticket_flag):
            return Code.ticket_flag_error, {'ticket_flag': ticket_flag}

        printed_num = PlaySeat.print_tickets(order.sell_order_no,order.pid,seats)

        if not printed_num:
            return Code.ticket_refund_failed.value,{}
        # Emum这种类就是.vlaue和,key方法
        order.status = OrderStatus.printed.value
        # 我们就是记录取票的时间,防止赖账
        order.print_time = datetime.now()
        order.save()
        return {'printed_num':printed_num}

    @route('/ticket/info/')
    @Validator(orderno = str)
    def ticket_info(self):
        orderno = request.params['orderno']
        order = Order.getby_orderno(orderno)
        if not order:
            return Code.order_does_not_exist,{'orderno': orderno}
        order.play = Play.get(order.pid)

        order.movie = Movie.get(order.play.mid)
        order.tickets = PlaySeat.getby_orderno(orderno)
        return order






