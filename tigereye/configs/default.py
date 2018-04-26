import os
class DefalutConfig(object):

    # os.path.dirname取出当前文件的name,../..再往上两级，这是相对目录。两个目录顺序注意
    # 根据os.path.abspath取到绝对路径
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__),'../..'))

    DEBUG = True
    # mysql的地址
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:lzp190917@localhost/tigereye'
    # 防止出警告信息的
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SQLALCHEMY_ECHO = True


    # 我们设置一下日志的目录配置路径，然后创建logs目录
    LOG_DIR = os.path.join(BASE_DIR,'logs')

