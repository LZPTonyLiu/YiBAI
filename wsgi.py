#
from tigereye import create_app
# 对外隐藏了create_app方法实现，别人不知道我们create_app在那写的
from tigereye.configs.production import ProductionConfig

application = create_app(config=ProductionConfig)
#
# 通过gunicorn运行命令，使用application会默认识别到它
#     gunicorn wsgi:application
# 也可以指定进程数量，来充分利用多进程版本

# ps ax |grep gunicon |grep -v grep|cut -d ' ' -f1|xargs kill
#  grep -v grep 过滤掉grep, 以空格切割开，f1取第一部分，xargs,把前面查到的结果传递给kill命令
# ./stop命令
# which gunicorn 找到位置
# cat start.sh
# gunicon -w2 -D -b 127.0.0.1:5000 wsgi:application
# chomd -R 777 /tigereye
# ab       'url'



