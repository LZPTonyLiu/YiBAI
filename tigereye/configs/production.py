# 正常的配置，configs里面有三个配置
# 灰度环境，就是和线上的环境基本上一模一样，只是用户比较少。
#   通过灰度环境，来逐渐逐渐上线，小规模上线。

from tigereye.configs.default import DefalutConfig


# PRD 产品环境
# STG服务器，就是和上线的环境一波一样的环境
# 灰度环境，让一部分用户来参与进来测试环境，就是生产环境
# 测试产品策略，看看新版本活跃度有没有更新
class ProductionConfig(DefalutConfig):
    DEBUG = False
    #
    JSON_SORT_KEYS = False
    #
    JSON_PRETTY_REGULAR = False
    SQLALCHEMY_ECHO = False
    # 以上 达到 上线基本配置，有利于性能方面的的东西
    # 线上启动不通过runserver，通过uWSGI 或者 WSGI
    #通过 gunicorn wsgi就可以运行起来
    # import sys
    #  print(sys.path)
    # 每个邮箱的smtp地址
    EMAIL_HOST = 'smtp.exmail.qq.com'
    EMAIL_PORT = 465

    # EMAIL_HOST_USER = SERVER_EMAIL = DEFAULT_FROM_EMAIL = 'test1@iguye.com'

    EMAIL_HOST_USER = 'test1@iguye.com'
    EMAIL_HOST_PASSWORD = 'P67844QUssW3'
    #
    EMAIL_USE_SSL = True
    # 写自己邮箱，这是接受邮件的
    ADMINS = ['839173890@qq.com']


    # 持续集成


    #flake8
    #jenkins



    #ab