from enum import Enum, unique
from random import randint

from sqlalchemy import text
from sqlalchemy.sql import func
from tigereye.models import db,Model
from tigereye.helper import tetime


@unique
class OrderStatus(Enum):
    """已锁座"""
    locked = 1
    """解锁"""
    unlocked = 2
    """自动解锁(超过一定时间未操作被系统自动解锁)"""
    auto_unlocked = 3
    """已支付"""
    paid = 4
    """已出票"""
    printed = 5
    """退款"""
    refund = 6

'''
订单  (order)
    id  (oid)
    影院id  (cid)
    影厅id
    电影id
    排期id  (pid)
    取票码  (orderno)
    票数  (tickets_num)
    金额  (amount)
    支付时间  (paid_time)
    取票时间  (printed_time)
    退款时间  (refund_time)
    订单创建时间  (created_time)
    最后更新时间  (updated_time)
    状态  (status)
'''


class Order(db.Model,Model):
    # 这个就是一个特殊字段，定义在数据库里面的名字
    __tablename__ = 'orders'
    # 订单ID,我们自己的订单号
    oid = db.Column(db.String(32), primary_key=True)
    #销售方订单号
    sell_order_no = db.Column(db.String(32), index=True)
    cid = db.Column(db.Integer)
    pid = db.Column(db.Integer)
    sid = db.Column(db.String(32))
    
    ticket_flag = db.Column(db.String(64))
    
    ticket_num = db.Column(db.Integer)
    amount = db.Column(db.Integer)

    paid_time = db.Column(db.DateTime)
    print_time = db.Column(db.DateTime)
    refund_time = db.Column(db.DateTime)
    created_time = db.Column(db.DateTime,server_default=text('CURRENT_TIMESTAMP'))
    updated_time = db.Column(db.DateTime,onupdate=func.now())
    status = db.Column(db.Integer,default=0,nullable=False,index=True)


    # 生成订单方法
    @classmethod
    def create(cls,cid,pid,sid):
        order = cls()
        # tetime 是生成现在时间，在helper里面，随机六位数，加上排期
        order.oid = '%s%s%s' % (tetime.now(),randint(100000,999999),pid)
        order.cid = cid
        order.pid = pid

        if type(sid) == list:
            # 我们这样得到的是一个字符串,但是数据库里面的字段我们应该定义字段为varchar(32)
            order.sid = ','.join(str(i) for i in sid)
        else:
            order.sid = sid
        return order


    @classmethod
    def getby_orderno(cls,orderno):
        return Order.query.filter_by(sell_order_no=orderno).first()





    def gen_ticket_flag(self):
        # 随机生成八位的取票码
        # 这事对象的方法,我们把这个付给它的一个字段,字符串类型
        self.ticket_flag =  ''.join([str(randint(1000,9999)) for i in range(8)])



    def validate(self, ticket_flag):
        # 我们把这个单独写成一个方法,就是为了扩展,API逻辑我们已经不用改了
        #
        return self.ticket_flag == ticket_flag

    # 通过取票码来获取订单

    def getby_ticket_flag(self,ticket_flag):
        return Order.query.filter_by(ticket_flag = ticket_flag).first()
