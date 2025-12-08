# coding:utf-8
# -----------------------------------------------------------------------------
# 系统的可调整，可配置的信息
# -----------------------------------------------------------------------------

import os


# 基于 setting.py的当前绝对路径，反推出项目的绝对路径
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 项目绝对目录

APP_DIR = os.path.dirname(os.path.abspath(__file__))           # APP的绝对目录

DEBUG = True

LANGUAGE = 'zh-cn'

