from tigereye.configs.default import DefalutConfig


# 这是我们测试的时候的配置
# 继承DefalutConfig
class Testconfig(DefalutConfig):
    # 我们正在测试
    TESTTING = True
    # 这个可以提高新嗯那个,这样就不会按照字母去对key排序
    JSON_SORT_KEYS = False
    # 不要打印没用信息
    SQLALCHEMY_ECHO = False
    # sqlite 什么也不写,就是数据保存在内存里面,不保存在磁盘里,完成测试数据也没了
    SQLALCHEMY_DATABASE_URI = 'sqlite://'