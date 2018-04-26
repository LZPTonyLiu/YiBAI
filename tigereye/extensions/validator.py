import functools

from flask import request, jsonify

from tigereye.helper.code import Code


class Validator(object):

    def __init__(self,**parameter_template):
        self.pt = parameter_template

    # 这个f，其实就是我们要装饰的目标方法
    def __call__(self, f):

        @functools.wraps(f)    #
        def decorated_function(*args,**kwargs):
            try:
                # 我们自定义的params
                request.params = {}
                for k, v in self.pt.items():
                    request.params[k] = v(request.values[k])
            #         下面是捕捉任意错误
            except Exception:
                # 返回一个错误信息
                response = jsonify(
                    rc = Code.required_parameter_missing.value,
                    msg = Code.required_parameter_missing.name,
                    data={'require_param': k}
                )
                response.status_code = 400
                return response
            # 这个是我们要装饰的方法f
            return f(*args,**kwargs)
        return decorated_function


# 我们自定义个异常,继承系统的Exception
class ValidationError(Exception):
    def __init__(self,message,values):
        super().__init__(message)
        # 这个是我们自己的信息
        self.values = values

# 如果输入的是多个参数的话，我们定义这个函数来把他们转换成一个列表
def multi_int(values,sperator=','):
    return [int(i) for i in values.split(sperator)]

#maiduoci
def comlex_int(values,sperator='-'):
    '''1-200-5000'''
    # 分割字符串
    digits = values.split(sperator)
    result = []
    #
    for digit in digits:
        # isdigit()判断要给字符串是否是一个数字,字符串必须是纯的数字.
        if not digit.isdigit():
            # values是message,前面字符串是value
            raise ValidationError('comlex int error: %s' % values,values)
        # 我们把每个数字转化成一个整数传回给result列表,并且返回它
        result.append(int(digit))
    return result

# 我们这样就是在买多张票的时候,我们传入参数的一种格式
def multi_comlex_int(values, sperator=','):
    '''1-200-5000,2-200-5000'''
    return [comlex_int(i) for i in values.split(sperator)]




    # def validate2(func):
    #     def validate3(*args,dict1 = {}):
    #
    #         if args in dict1:
    #             return func()
    #         else:
    #             return func(args)



# 面试算法
# list1 = [{'mm':2},{'mm':1},{'mm':4},{'mm':3},{'mm':3}]
#
# K = 0
# for i in list1:
#     changdu = len(list1) + 1
#     K += 1
#     for j in list1[K:changdu]:
#         if i['mm']<j['mm']:
#             print('%d不是最大' %i['mm'])
#             break


a = [12,-12,13,78]


for i in a:
    b = 0-i
    if b in a:
        print()


