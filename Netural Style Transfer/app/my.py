# coding:utf-8

import os

from . import settings as Setting                 # 系统设置变量
from .res import consts as Const                  # 系统常量信息
from .res.strings import String as String         # 系统字符串资源
from .res.fonts import Font                       # 系统字体资源
from .res.colors import Color

session = dict()

def img(img_name):
    """ 传入文件名，返回完整的图片路径 """
    return os.path.join(Setting.APP_DIR, "res\\images\\", img_name)
