import functools

import time
from flask import request, Response, make_response, jsonify, current_app
from flask_classy import FlaskView
from tigereye.helper.code import Code

# 我们自己写aipview
class ApiView(FlaskView):
    # 使用钩子函数来测试接口的响应时间
    def before_request(self):
        self.request_start_time = time.time()
    def after_request(self):
        current_app.logger.info('%s response time: %s' %(request))
    #     ——————————————————————————————————


    # 重写方法，这个方法是一个装饰器，装饰的是我们再view里面写的方法比如 get index play hosts
    @classmethod
    def make_proxy_method(cls, name):
        """Creates a proxy function that can be used by Flasks routing. The
        proxy instantiates the FlaskView subclass and calls the appropriate
        method.

        :param name: the name of the method to create a proxy for
        """

        i = cls()
        view = getattr(i, name)

        if cls.decorators:
            for decorator in cls.decorators:
                view = decorator(view)

        @functools.wraps(view)
        def proxy(**forgettable_view_args):
            # Always use the global request object's view_args, because they
            # can be modified by intervening function before an endpoint or
            # wrapper gets called. This matches Flask's behavior.
            del forgettable_view_args

            if hasattr(i, "before_request"):
                response = i.before_request(name, **request.view_args)
                if response is not None:
                    return response

            before_view_name = "before_" + name
            if hasattr(i, before_view_name):
                before_view = getattr(i, before_view_name)
                response = before_view(**request.view_args)
                if response is not None:
                    return response

            # 这里的view就是我们要装饰的方法，这里还不算一种response类型。
            response = view(**request.view_args)



            #判断是否是一个Response对象
            if not isinstance(response,Response):
                # 如果不是，则先获取它的类型
                response_type = type(response)
                #如果是tuple类型
                if  response_type == tuple and len(response)> 1:
                    # 不成功的话，我们走这里，我们api里面返回的两个参数就是请求失败
                    rc,_data = response
                    #     加上我们的自己APi接口的信息
                    #  jsonify源码逻辑是先dumps然后再makeresponse
                    # return jsonify(rc = rc.value,msg = rc.name,data = _data)
                    response =  jsonify(rc=rc.value, msg=rc.name, data=_data)
                else:
                    # 这些Code.succ.name 都是再helper里面定义一个继承eum类的方法
                    # 写死的代码，出现rc = 1 就是硬编码
                    # 其实即使我们再view里面调用的jsonify 统一到这里了。我们就不用再每个方法里加了
                    # return jsonify(rc=Code.succ.value,msg=Code.succ.name,data = response)
                    response =  jsonify(rc=Code.succ.value,msg=Code.succ.name,data = response)

            # if not isinstance(response, Response):
            #     response = make_response(response)

            after_view_name = "after_" + name
            if hasattr(i, after_view_name):
                after_view = getattr(i, after_view_name)
                response = after_view(response)

            if hasattr(i, "after_request"):
                response = i.after_request(name, response)

            return response

        return proxy
