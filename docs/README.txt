
我们这个项目结构就是这样的，manage.py管理是整个tigereye项目，同样tests也是测试tigereye项目。
如果我们同时写了一个后台项目，我们可以实现用户用的后台，和我们自己管理后台分离。
电影 (movie)
    id  (mid)
    名称  (name)
    语言  （language）
    字幕  (subtitle)
    上映日期  (show_date)
    版本（2D/3D/4D）  (vision)
    模式（胶片/数字）  (model)
    屏幕尺寸  (screen_size)
    简介  (introduction)
    状态  (status)

影院  (cinema)
    id  (cid)
    名称  (name)
    地址  (address)
    影厅数量  (halls)
    手续费  (handle_fee)
    购买数量限制  (buy_limit)
    状态  (status)

影厅 (hall)
    id  (hid)
    影院id  (cid)
    名称  (name)
    屏幕类型  (screen_type)
    音效  (auto_type)
    座位数量  (seats_num)
    状态  (status)

排期
    id  (pid)
    电影id  (mid)
    影院id  (cid)
    影厅id  (hid)
    价格类型  (price_type)
    原价  (price)
    售价  (market_price)
    最低价  (lowest_price)
    开始时间  (start_time)
    时常  (duration)
    创建时间  (create_time)
    最后更新时间  (update_time)
    状态  （status）

座位
    id  (sid)
    影院id  (cid)
    影厅id  (hid)
    座位类型  (seat_type)
    是否是情侣座  (love_seats)
    x坐标  (x)
    y坐标  (y)
    排（A/第1排） (row)
    列（Abcd/第几列）  (column)
    区域  (area)
    状态  (status)

"""


排期座位
    id  (psid)
    订单号  (orderno)
    影院id  (cid)
    影厅id  (hid)
    座位id  (sid)
    排期id  (pid)
    座位类型  (seat_type)
    是否情侣座  (love_seats)
    x坐标  (x)
    y坐标  (y)
    排（A/第1排）  (row)
    列（Abcd/第几列）  (column)
    区域  (area)
    状态  (status)
    锁定时间  (lock_time)
    创建时间  (created_time)


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