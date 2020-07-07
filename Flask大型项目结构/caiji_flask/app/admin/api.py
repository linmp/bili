from flask import request, session, jsonify, g
from app.models import db, Admin, AdminLoginLog, Board, AdminOperateLog
from app.utils.tool import admin_login_required
from . import admin

"""

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

"""


# 初始页面
@admin.route("/index", methods=["GET"])
def index():
    return "hello 菜鸡音宫 管理员页面"


# 登录
@admin.route("/login", methods=["POST"])
def login():
    """
    账号 username
    密码 password
    :return:
    """
    get_data = request.get_json()
    username = get_data.get("username")
    password = get_data.get("password")

    if not all([username, password]):
        return jsonify(msg="参数不完整", code=4000), 400

    # 验证账号密码
    user = Admin.query.filter_by(username=username).first()
    # 账号密码验证成功
    if user and user.password == password:
        session["admin_username"] = username
        session["admin_id"] = user.id
        session["admin_avatar"] = user.avatar

        # 添加登录日志
        admin_id = user.id
        ip = request.remote_addr
        login_log = AdminLoginLog(admin_id=admin_id, ip=ip)
        try:
            db.session.add(login_log)
            db.session.commit()
        except Exception as e:
            print(e)

        return jsonify(msg="登录成功", code=200), 200

    else:
        return jsonify(msg="账号或密码错误", code=4001), 400


# 检查登录状态
@admin.route("/session", methods=["GET"])
def check_session():
    username = session.get("admin_username")
    if username:
        return jsonify(username=username, code=200), 200
    else:
        return jsonify(msg="出错了，没登录", code=4000), 400


# 登出
@admin.route("/logout", methods=["DELETE"])
@admin_login_required
def logout():
    session.clear()
    return jsonify(msg="成功退出登录!", code=200), 200


# 发布公告
@admin.route("/bulletin/board", methods=["POST"])
@admin_login_required
def bulletin_board():
    req_data = request.get_json()

    admin_id = g.admin_id

    title = req_data.get("title")
    content = req_data.get("content")
    if not all([admin_id, title, content]):
        return jsonify(msg="参数不完整", code=4000), 400

    # 存的是 公告
    board = Board(title=title, content=content, admin_id=admin_id)
    db.session.add(board)

    # 存操作日志
    ip = request.remote_addr
    detail = "添加了公告：" + title
    aol = AdminOperateLog(admin_id=admin_id, ip=ip, detail=detail)
    db.session.add(aol)

    try:
        db.session.commit()
    except Exception as e:
        print(e)
        db.session.rallback()
        return jsonify(msg="提交不成功", code=4001), 400
    return jsonify(msg="提交成功", code=200), 200


# 获取登录日志
@admin.route("/login/log", methods=["GET"])
@admin_login_required
def login_log():
    admin_id = g.admin_id
    admin_login_logs = AdminLoginLog.query.filter_by(admin_id=admin_id).order_by(AdminLoginLog.create_time.desc())
    admin_log_li = []
    for admin_login_log in admin_login_logs:
        data = {
            "admin_id": admin_login_log.admin_id,
            "ip": admin_login_log.ip,
            "create_time": admin_login_log.create_time.strftime("%Y-%m-%d %H:%M:%S")
        }
        admin_log_li.append(data)

    # 将数据转换为json字符串
    resp_dict = dict(code=200, msg="管理员登录日志", data=admin_log_li)
    return jsonify(resp_dict), 200
    # return resp_json, 200, {"Content-Type": "application/json"}


# 获取操作日志
@admin.route("/operate/log", methods=["GET"])
@admin_login_required
def operate_log():
    admin_id = g.admin_id
    admin_operate_logs = AdminOperateLog.query.filter_by(admin_id=admin_id).order_by(AdminOperateLog.create_time.desc())
    admin_operate_log_li = []
    for admin_operate_log in admin_operate_logs:
        data = {
            "id": admin_operate_log.id,
            "admin_id": admin_operate_log.admin_id,
            "ip": admin_operate_log.ip,
            "detail": admin_operate_log.detail,
            "create_time": admin_operate_log.create_time.strftime("%Y-%m-%d %H:%M:%S")
        }
        admin_operate_log_li.append(data)

    # 将数据转换为json字符串
    resp_dict = dict(code=200, msg="管理员操作日志", data=admin_operate_log_li)
    return jsonify(resp_dict), 200
    # return jsonify(resp_dict), 200, {"Content-Type": "application/json"}
