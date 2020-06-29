from . import admin


# 初始页面
@admin.route("/index", methods=["GET"])
def index():
    return "hello 菜鸡音宫 管理员页面"

# 登录
@admin.route("/login", methods=["POST"])
def login():
    """用户的登录"""
    # 获取参数
    req_dict = request.get_json()
    username = req_dict.get("username")
    password = req_dict.get("password")

    # 参数完整的校验
    if not all([username, password]):
        return jsonify(code=4001, msg="参数不完整")

    # 查询用户
    try:
        admin_info = Admin.query.filter_by(username=username).first()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(code=4002, msg="获取用户信息失败")

    # 用户的状态是否可用
    if admin_info is None or admin_info.status != "正常":
        return jsonify(code=4003, msg="查无此用户 无法登录")

    # 用数据库的密码与用户填写的密码进行对比验证
    if admin_info is None or admin_info.password != password:
        return jsonify(code=4003, msg="用户名或密码错误")

    # 添加管理员登录日志
    ip_addr = request.remote_addr  # 获取管理员登录的ip
    admin_login_log = AdminLoginLog(admin_id=admin_info.id, ip=ip_addr)
    try:
        db.session.add(admin_login_log)
        db.session.commit()
    except Exception as e:
        print(e)
        db.session.rollback()

    # 如果验证相同成功，保存登录状态， 在session中
    session["username"] = admin_info.username
    session["admin_id"] = admin_info.id
    session["avatar"] = admin_info.avatar

    return jsonify(code=200, msg="登录成功")


# 检查登陆状态
@admin.route("/session", methods=["GET"])
def check_login():
    """检查登陆状态"""
    # 尝试从session中获取用户的名字
    username = session.get("username")
    admin_id = session.get('admin_id')
    avatar = session.get("avatar")
    # 如果session中数据username名字存在，则表示用户已登录，否则未登录
    if username is not None:
        return jsonify(code=200, msg="已登录", data={"username": username, "admin_id": admin_id, "avatar": avatar})
    else:
        return jsonify(code=4001, msg="管理员未登录")


# 登出
@admin.route("/session", methods=["DELETE"])
@admin_login_required
def logout():
    """登出"""
    # 清除session数据
    session.clear()
    return jsonify(code=200, msg="成功退出登录!")
