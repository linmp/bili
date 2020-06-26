from . import db


"""
python3 manage.py db init
python3 manage.py db migrate -m "message"
python3 manage.py db upgrade
python3 manage.py db downgrade
"""


# 用户表
class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)  # 主键
    username = db.Column(db.String(64), nullable=False, unique=True)  # 账户
    password = db.Column(db.String(64), nullable=False)  # 密码
    phone = db.Column(db.String(11))  # 手机号 可以为空
    address = db.Column(db.String(11))  # 地址


# 管理员表
class Admin(db.Model):
    __tablename__ = "admin"
    id = db.Column(db.Integer, primary_key=True)  # 主键
    username = db.Column(db.String(64), nullable=False, unique=True)  # 账户
    password = db.Column(db.String(64), nullable=False)  # 密码
    power = db.Column(db.Enum("管理员", "超级管理员"), nullable=False, default="管理员")  # 权限
    phone = db.Column(db.String(11))  # 手机号 可以为空
    address = db.Column(db.String(11))  # 地址

