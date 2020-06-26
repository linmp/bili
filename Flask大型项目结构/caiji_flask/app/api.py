from flask import session, jsonify, request, Blueprint
from .models import User, Admin, db

# 创建蓝图对象
user = Blueprint("user", __name__)  # 用户蓝图对象
admin = Blueprint("admin", __name__)  # 管理员蓝图对象


# 用户初始页面
@user.route("/index", methods=["GET"])
def hello_world():
    return "hello 音宫 这里是用户初始页面"


# 用户注册
@user.route("/register", methods=["POST"])
def user_register():
    try:
        my_json = request.get_json()
        print(my_json)
        username = my_json.get("username")
        password = my_json.get("password")
        if not all([username, password]):
            return jsonify(msg="参数不完整", code=4000)

        user = User(username=username, password=password)

        # 添加到数据库
        try:
            db.session.add(user)
            db.session.commit()
            return jsonify(code=200, msg="注册成功", username=username)  # 成功
        except Exception as e:
            print(e)
            return jsonify(msg="存数据库失败", code=4001)

    except Exception as e:
        print(e)
        return jsonify(msg="出错了哦，请查看是否正确访问", code=4002)


# 登录
@user.route("/login", methods=["POST"])
def user_login():
    get_data = request.get_json()
    username = get_data.get("username")
    password = get_data.get("password")

    if not all([username, password]):
        return jsonify(msg="参数不完整", code=4000)

    user = User.query.filter_by(username=username).first()
    # 如果用户存在并且密码对
    if user and user.password == password:
        # 如果验证通过 保存登录状态在session中
        session["user_username"] = username
        return jsonify(msg="登录成功", code=200, username=username)
    else:
        return jsonify(msg="账号或密码错误", code=4001)


# 检查登录状态
@user.route("/session", methods=["GET"])
def user_check_session():
    username = session.get("user_username")
    if username is not None:
        # 操作逻辑 数据库什么的
        # 数据库里面 把你的头像 等级 金币数量 查询出来
        return jsonify(username=username, code=200)
    else:
        return jsonify(msg="出错了，没登录", code=4000)


# 登出
@user.route("/logout", methods=["DELETE"])
def user_logout():
    username = session.get("user_username")
    if username is None:
        return jsonify(msg="出错了，没登录!", code=4000)

    session.clear()  # 留个坑
    return jsonify(msg="成功退出登录!", code=200)


# 管理员初始页面
@admin.route("/index", methods=["GET"])
def hello_world():
    return "hello 音宫 这里是管理员初始页面"


# 管理员注册
@admin.route("/register", methods=["POST"])
def admin_register():
    try:
        my_json = request.get_json()
        print(my_json)
        username = my_json.get("username")
        password = my_json.get("password")
        if not all([username, password]):
            return jsonify(msg="参数不完整", code=4000)

        admin = Admin(username=username, password=password)

        # 添加到数据库
        try:
            db.session.add(admin)
            db.session.commit()
            return jsonify(code=200, msg="注册成功", username=username)  # 成功
        except Exception as e:
            print(e)
            return jsonify(msg="存数据库失败", code=4001)

    except Exception as e:
        print(e)
        return jsonify(msg="出错了哦，请查看是否正确访问", code=4002)


# 管理员登录
@admin.route("/login", methods=["POST"])
def admin_login():
    get_data = request.get_json()
    username = get_data.get("username")
    password = get_data.get("password")

    if not all([username, password]):
        return jsonify(msg="参数不完整", code=4000)

    admin = Admin.query.filter_by(username=username).first()
    # 如果用户存在并且密码对
    if admin and admin.password == password:
        # 如果验证通过 保存登录状态在session中
        session["admin_username"] = username
        return jsonify(msg="登录成功", code=200, username=username)
    else:
        return jsonify(msg="账号或密码错误", code=4001)


# 检查管理员登录状态
@admin.route("/session", methods=["GET"])
def admin_check_session():
    username = session.get("admin_username")
    if username is not None:
        # 操作逻辑 数据库什么的
        # 数据库里面 把你的头像 等级 金币数量 查询出来
        return jsonify(username=username, code=200)
    else:
        return jsonify(msg="出错了，没登录", code=4000)


# 管理员登出
@admin.route("/logout", methods=["DELETE"])
def admin_logout():
    username = session.get("admin_username")
    if username is None:
        return jsonify(msg="出错了，没登录!", code=4000)

    session.clear()
    return jsonify(msg="成功退出登录!", code=200)
