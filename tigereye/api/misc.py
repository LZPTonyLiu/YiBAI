from flask import current_app, request
from flask_classy import FlaskView, route

class MiscView(FlaskView):
    route_base = '/'

    def index(self):
        return self.check()
    @route('')
    def check(self):
        # 有人访问check 会自动打印访问者的，地址
        current_app.logger.info('check from %s' % request. remote_addr)

        return 'I am OK'

    def error(self):
        1/0
