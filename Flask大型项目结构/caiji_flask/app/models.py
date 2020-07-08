from . import db
from datetime import datetime

"""
python3 manage.py db init # 第一次需要运行
python3 manage.py db migrate -m "message"
python3 manage.py db upgrade
python3 manage.py db downgrade
"""

"""
管理员

    登录 /admin/login
    检查登陆状态 /admin/session
    登出 /admin/logout
    发送公告 /admin/bulletin/board
    获取登录日志 /admin/login/log
    获取操作日志 /admin/operate/log
    添加管理员 /admin/ manager
    删除管理员 /admin/ manager
    新增标签 /tag
    删除标签 /tag
    屏蔽用户 /user/status
    删除评论 /comment
    统计浏览量 /views/numbers
    查看所有用户略情 /all/user/int:page
    查看所有的反馈信息 /feedback/int:page"
    发博总数 /blog/numbers
    注册用户量 /register/numbers
    发表博客 /blog/article
    修改博客状态 /blog/article/status

...
用户

    发送注册验证码 /main/sms
    注册 /main/register
    登录 /main/login
    登录状态 /main/session
    登出 /main/session
    修改密码 /main/password
    发送找回密码验证码 /main/reset/password/sms
    找回密码 /main/password
    获取个人信息 /main/user/profile/<user_id>
    设置用户的头像 /main/user/avatar
    修改用户的用户名 /main/user/username
    评论 /main/comment
    删自己评论 /main/comment
    收藏博客 /main/blog/collect
    取消收藏博客 /main/blog/collect
    反馈 /main/message
    搜索 /main/blog/search/int:page
    获取博客详情 /main /blog/article/detail/int:blog_id

"""


# 管理员表
class Admin(db.Model):
    __tablename__ = "admin"
    id = db.Column(db.Integer, primary_key=True)  # id号(独一无二的)
    username = db.Column(db.String(64), nullable=False, unique=True)  # 账号用户名
    password = db.Column(db.String(64), nullable=False)  # 密码
    avatar = db.Column(db.String(256), nullable=False)  # 头像
    phone = db.Column(db.String(11), unique=True, nullable=False)  # 手机号
    # 枚举 只能存的是枚举里面设置的内容 不是设置的规定的内容的话 是会报错的
    power = db.Column(db.Enum("超级管理员", "普通管理员"), nullable=False, default="普通管理员")  # 管理员权限
    status = db.Column(db.Boolean, nullable=False, default=True)  # 真假代表正常异常状态
    # index 设置的是什么 设置的是索引 索引就是帮助你更快地找到对应的数据
    create_time = db.Column(db.DateTime, index=True, default=datetime.now)  # 创建时间
    # onupdate 自动更新 每一次 增删查改这个表都会 自动更新一下时间
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)  # 最近一次登录时间
    # 认领 关联
    boards = db.relationship("Board", backref="admin")  # 关联公告表
    my_login_log = db.relationship("AdminLoginLog", backref="admin")  # 关联登录日志表
    my_operate_log = db.relationship("AdminOperateLog", backref="admin")  # 关联操作日志表
    my_blog = db.relationship("Blog", backref="admin")  # 关联博客表
    message_get = db.relationship("Message", backref="admin")  # 关联反馈表 收到的反馈


# 公告表
class Board(db.Model):
    __tablename__ = "board"
    id = db.Column(db.Integer, primary_key=True)  # id号(独一无二的)
    title = db.Column(db.String(64), nullable=False)  # 标题
    content = db.Column(db.Text, nullable=False)  # 内容 Text存很多数据
    status = db.Column(db.Boolean, nullable=False, default=True)  # 真假代表展示、不展示状态
    # index 设置的是什么 设置的是索引 索引就是帮助你更快地找到对应的数据
    create_time = db.Column(db.DateTime, index=True, default=datetime.now)  # 创建时间
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))  # 所属管理员


# 管理员的登录日志表
class AdminLoginLog(db.Model):
    __tablename__ = "admin_login_log"
    id = db.Column(db.Integer, primary_key=True)  # id号(独一无二的)
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))  # 所属管理员
    ip = db.Column(db.String(64), nullable=False)  # 登录的ip
    # index 设置的是什么 设置的是索引 索引就是帮助你更快地找到对应的数据
    create_time = db.Column(db.DateTime, index=True, default=datetime.now)  # 创建时间


# 管理员的操作日志表
class AdminOperateLog(db.Model):
    __tablename__ = "admin_operate_log"
    id = db.Column(db.Integer, primary_key=True)  # id号(独一无二的)
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))  # 所属管理员
    ip = db.Column(db.String(64), nullable=False)  # 操作的ip
    detail = db.Column(db.String(128), nullable=False)  # 操作详情
    # index 设置的是什么 设置的是索引 索引就是帮助你更快地找到对应的数据
    create_time = db.Column(db.DateTime, index=True, default=datetime.now)  # 创建时间


# 标签表
class Tag(db.Model):
    __tablename__ = "tag"
    id = db.Column(db.Integer, primary_key=True)  # id号(独一无二的)
    name = db.Column(db.String(16), nullable=False)  # 标签名字
    status = db.Column(db.Boolean, nullable=False, default=True)  # 真假代表展示、不展示状态
    # index 设置的是什么 设置的是索引 索引就是帮助你更快地找到对应的数据
    create_time = db.Column(db.DateTime, index=True, default=datetime.now)  # 创建时间


# 多对多关系引入中间表
class BlogToTag(db.Model):
    __tablename__ = "blog_to_tag"
    id = db.Column(db.Integer, primary_key=True)  # id号(独一无二的)
    tag_id = db.Column(db.Integer, db.ForeignKey("tag.id"), nullable=False)  # 所属标签
    blog_id = db.Column(db.Integer, db.ForeignKey("blog.id"), nullable=False)  # 所属博客


# 博客表
class Blog(db.Model):
    __tablename__ = "blog"
    id = db.Column(db.Integer, primary_key=True)  # id号(独一无二的)
    title = db.Column(db.String(64), nullable=False)  # 标题
    summary = db.Column(db.String(64), nullable=False)  # 简介
    content = db.Column(db.Text, nullable=False)  # 详细内容
    logo = db.Column(db.String(256), nullable=False)  # 封面图
    # 枚举 设置 三种状态 "发布", "草稿", "删除"
    status = db.Column(db.Enum("发布", "草稿", "删除"), nullable=False, default="发布")  # 真假代表展示、不展示状态
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))  # 所属管理员
    page_views = db.Column(db.Integer, default=0)  # 浏览次数
    like_numbers = db.Column(db.Integer, default=0)  # 点赞次数
    comment_numbers = db.Column(db.Integer, default=0)  # 评论次数
    create_time = db.Column(db.DateTime, index=True, default=datetime.now)  # 创建时间
    # 关联
    tags = db.relationship("Tag", secondary="blog_to_tag", backref="blog")  # 关联标签
    comments = db.relationship("Comment", backref="blog")  # 关联评论表

    def to_dict(self):
        tag = []
        for t in self.tags:
            tag.append(t.name)
        data = {
            "title": self.title,
            "summary": self.summary,
            "content": self.content,
            "logo": self.logo,
            "page_views": self.page_views,
            "tags": tag,

        }
        return data


# 用户表
class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)  # id号(独一无二的)
    username = db.Column(db.String(64), nullable=False, unique=True)  # 账号用户名
    password = db.Column(db.String(64), nullable=False)  # 密码
    avatar = db.Column(db.String(256), nullable=False)  # 头像
    phone = db.Column(db.String(11), unique=True, nullable=False)  # 手机号
    status = db.Column(db.Boolean, nullable=False, default=True)  # 真假代表正常异常状态
    # index 设置的是什么 设置的是索引 索引就是帮助你更快地找到对应的数据
    create_time = db.Column(db.DateTime, index=True, default=datetime.now)  # 创建时间
    # onupdate 自动更新 每一次 增删查改这个表都会 自动更新一下时间
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)  # 最近一次登录时间
    # 认领 关联
    # 我的所有评论
    comment_sends = db.relationship("Comment", backref="sender")  # 关联评论表
    # 我的所有反馈
    message_sends = db.relationship("Message", backref="sender")  # 关联反馈表
    # 我所收藏的博客
    my_collects = db.relationship("Blog", secondary="collect_blog", backref="collector")  # 关联收藏博客表
    # 关联我的搜索表
    my_search_history = db.relationship("SearchHistory", backref="user")  # 关联搜索历史表


# 评论表
class Comment(db.Model):
    __tablename__ = "comment"
    id = db.Column(db.Integer, primary_key=True)  # id号(独一无二的)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 所属用户评论者
    blog_id = db.Column(db.Integer, db.ForeignKey('blog.id'))  # 所属博客
    content = db.Column(db.Text, nullable=False)  # 内容 Text存很多数据
    status = db.Column(db.Boolean, nullable=False, default=True)  # 真假代表展示、不展示状态
    # index 设置的是什么 设置的是索引 索引就是帮助你更快地找到对应的数据
    create_time = db.Column(db.DateTime, index=True, default=datetime.now)  # 创建时间


#  反馈表
class Message(db.Model):
    __tablename__ = "message"
    id = db.Column(db.Integer, primary_key=True)  # id号(独一无二的)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 所属用户发送者
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))  # 所属管理员
    content = db.Column(db.Text, nullable=False)  # 内容 Text存很多数据
    status = db.Column(db.Boolean, nullable=False, default=True)  # 真假代表展示、不展示状态
    # index 设置的是什么 设置的是索引 索引就是帮助你更快地找到对应的数据
    create_time = db.Column(db.DateTime, index=True, default=datetime.now)  # 创建时间


#  收藏表 中间表
class CollectBlog(db.Model):
    __tablename__ = "collect_blog"
    id = db.Column(db.Integer, primary_key=True)  # id号(独一无二的)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 所属用户
    blog_id = db.Column(db.Integer, db.ForeignKey('blog.id'))  # 所属博客
    status = db.Column(db.Boolean, nullable=False, default=True)  # 真代表收藏 假代表取消收藏
    # index 设置的是什么 设置的是索引 索引就是帮助你更快地找到对应的数据
    create_time = db.Column(db.DateTime, index=True, default=datetime.now)  # 创建时间


#  搜索表
class SearchHistory(db.Model):
    __tablename__ = "search_history"
    id = db.Column(db.Integer, primary_key=True)  # id号(独一无二的)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 所属用户
    keyword = db.Column(db.String(64), nullable=False)  # 关键字搜索
    # index 设置的是什么 设置的是索引 索引就是帮助你更快地找到对应的数据
    create_time = db.Column(db.DateTime, index=True, default=datetime.now)  # 创建时间
