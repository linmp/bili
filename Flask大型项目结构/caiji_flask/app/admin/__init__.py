from flask import Blueprint

# 创建蓝图对象
admin = Blueprint("admin", __name__)

from . import api