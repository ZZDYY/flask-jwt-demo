# -*- coding: utf-8 -*-
# @Time    : 2020/8/13 10:43
# @Author  : CMJ
# @File    : __init__.py.py
# @Software: PyCharm
from flask import Blueprint
main = Blueprint('main', __name__)

from . import auth