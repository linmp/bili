from flask import request, session, jsonify, g
from app.models import db, Admin, AdminLoginLog, Board, AdminOperateLog, Comment, User, Blog, Tag, Message
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
        db.session.rollback()
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


####
# 新增标签
@admin.route("/tag", methods=["POST"])
@admin_login_required
def add_tag():
    admin_id = g.admin_id
    json_data = request.get_json()
    ip_addr = request.remote_addr
    tag = json_data.get("tag")
    if not all([ip_addr, tag]):
        return jsonify(code=4000, msg="参数不完整"), 400

    try:
        # 添加标签
        t = Tag(name=tag)
        # 保存到操作日志
        detail = "添加了新标签: %s " % tag
        admin_operate_log = AdminOperateLog(admin_id=admin_id, ip=ip_addr, detail=detail)
        db.session.add(t)
        db.session.add(admin_operate_log)
        db.session.commit()
        return jsonify(code=200, msg="新增标签成功")
    except Exception as e:
        db.session.rollback()
        print(e)
        return jsonify(code=4001, msg="新增标签失败"), 400


# 删除标签
@admin.route("/tag", methods=["DELETE"])
@admin_login_required
def delete_tag():
    admin_id = g.admin_id
    json_data = request.get_json()
    ip_addr = request.remote_addr
    tag = json_data.get("tag")
    if not all([ip_addr, tag]):
        return jsonify(code=4001, msg="参数不完整"), 400

    # 删除标签 软删除
    # t = Tag.query.filter_by(name=tag).delete()
    t = Tag.query.filter_by(name=tag).first()
    if t and t.status is True:
        t.status = False
    else:
        return jsonify(code=4002, msg="标签不存在"), 400

    detail = "删除了旧标签: %s " % tag
    admin_operate_log = AdminOperateLog(admin_id=admin_id, ip=ip_addr, detail=detail)
    db.session.add(admin_operate_log)
    db.session.add(t)
    try:
        db.session.commit()
        return jsonify(code=200, msg="删除标签成功")
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify(code=4004, msg="删除标签失败")


# 发表博客
@admin.route("/blog/article", methods=["POST"])
@admin_login_required
def post_blog_article():
    """
    title
    content
    summary
    admin_id
    tags = []
    :return:
    """
    admin_id = g.admin_id  # 博主的id
    req_data = request.get_json()
    ip_addr = request.remote_addr
    title = req_data.get("title")  # 标题
    content = req_data.get("content")  # 内容
    summary = req_data.get("summary")  # 简介
    logo = req_data.get("logo")  # 封面
    status = req_data.get("status")  # 状态 "发布", "草稿"

    tags = req_data.get("tags")  # ["name","name"]

    if not all([title, content, summary, tags, logo]):
        return jsonify(code=4000, msg="参数不完整")

    if status not in ("发布", "草稿"):
        return jsonify(code=4001, msg="参数出错")

    try:
        blog = Blog(title=title, content=content, summary=summary, admin_id=admin_id, status=status,logo=logo)

        # 查询标签添加博客标签
        t = Tag.query.filter(Tag.name.in_(tags)).all()

        blog.tags = t

        if status == "草稿":
            detail = "添加草稿: %s " % title
        else:
            detail = "发布博客: %s " % title
        admin_operate_log = AdminOperateLog(admin_id=admin_id, ip=ip_addr, detail=detail)
        db.session.add(blog)
        db.session.add(admin_operate_log)
        db.session.commit()

    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify(code=4002, msg="操作出错,数据库出错")

    return jsonify(code=200, msg="操作成功", id=blog.id)


# 修改博客状态
@admin.route("/blog/article/status", methods=["PUT"])
@admin_login_required
def delete_blog_article():
    """
    status
    状态 正常 草稿
    :return:
    """
    req_data = request.get_json()
    ip_addr = request.remote_addr
    status = req_data.get("status")  # 博客状态 "发布", "草稿", "删除"
    bid = req_data.get("id")  # 博客id
    admin_id = g.admin_id  # 博主id

    if not all([ip_addr, status, bid, admin_id]):
        return jsonify(code=4000, msg="参数不完整")

    if status not in ["发布", "草稿", "删除"]:
        return jsonify(code=4001, msg="状态更改失败")

    blog = Blog.query.get(bid)
    if blog is None or blog.status == "删除":
        return jsonify(code=4002, msg="博客不存在")

    # 如果 不是超级管理员 也不是作者 那么出错
    if blog.admin_id != admin_id and admin_id != 1:
        return jsonify(code=4002, msg="你不是作者")

    if blog.status == status:
        return jsonify(code=200, msg="操作成功")

    detail = "修改了文章状态: %s --> %s " % (blog.status, status)
    try:
        blog.status = status
        # 添加操作日志
        admin_operate_log = AdminOperateLog(admin_id=admin_id, ip=ip_addr, detail=detail)
        db.session.add(admin_operate_log)

        db.session.add(blog)
        db.session.commit()
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify(code=4003, msg="修改出错,请稍后再试")

    return jsonify(code=200, msg="操作成功")


# 新增管理员
@admin.route("/manager", methods=["POST"])
@admin_login_required
def add_manager():
    """
    需要的用户信息
        管理员用户名
        管理员密码
        权限 管理员 超级管理员
    注意:
        管理员只能创建权限比自己小的子管理员
    :return:
    """
    admin_id = g.admin_id
    ip_addr = request.remote_addr  # 获取管理员登录的ip
    req_dict = request.get_json()
    new_admin_username = req_dict.get("username")
    new_admin_password = req_dict.get("password")

    # 参数完整的校验
    if not all([new_admin_username, new_admin_password, ip_addr]):
        return jsonify(code=400, msg="参数不完整")

    # 获取当前管理员的信息
    current_admin = Admin.query.get(admin_id)
    if not current_admin:
        return jsonify(code=400, msg="当前管理员出错")

    # 获取当前管理员的权限
    current_admin_power = current_admin.power

    # 判断管理员是否是超级管理员
    if current_admin_power == "超级管理员":
        avatar = "http://bilibili.com"
        new_admin = Admin(username=new_admin_username, password=new_admin_password, power="管理员",
                          avatar=avatar)
        try:
            db.session.add(new_admin)
            detail = "添加了新管理员: %s " % new_admin_username
            # 操作日志
            admin_operate_log = AdminOperateLog(admin_id=admin_id, ip=ip_addr, detail=detail)
            db.session.add(admin_operate_log)
            db.session.commit()
            return jsonify(code=200, msg="添加管理员成功")
        except Exception as e:
            print(e)
            db.session.rollback()
            return jsonify(code=400, msg="保存数据失败,或许用户名冲突,请稍后再试")
    else:
        return jsonify(code=400, msg="当前管理员无法添加此权限用户")


# 删除管理员
@admin.route("/manager", methods=["DELETE"])
@admin_login_required
def delete_manager():
    """
    需要的用户信息
        管理员用户名
    :return:
    """
    admin_id = g.admin_id
    admin_name = session.get("username")  # 获取管理员的名字
    ip_addr = request.remote_addr  # 获取管理员登录的ip
    req_dict = request.get_json()
    delete_admin_username = req_dict.get("username")

    # 参数完整的校验
    if not all([delete_admin_username, ip_addr]):
        return jsonify(code=400, msg="参数不完整")

    # 获取当前管理员的信息
    current_admin = Admin.query.get(admin_id)
    if not current_admin:
        return jsonify(code=400, msg="当前管理员出错")

    # 获取当前管理员的权限
    current_admin_power = current_admin.power
    if current_admin_power != "超级管理员":
        return jsonify(code=400, msg="当前管理员权利不够删除管理员")

    # 执行操作
    if current_admin_power == "超级管理员":
        delete_admin = Admin.query.filter_by(username=delete_admin_username).first()
        if not delete_admin:
            return jsonify(code=400, msg="查询不到将要删除的管理员")

        # 如果删除的是自己
        if delete_admin.username == admin_name:
            return jsonify(code=400, msg="不能删除自己信息")

        try:
            delete_admin.status = "删除"
            db.session.add(delete_admin)

            detail = "删除了管理员: %s " % delete_admin_username
            admin_operate_log = AdminOperateLog(admin_id=admin_id, ip=ip_addr, detail=detail)
            db.session.add(admin_operate_log)
            db.session.commit()
            return jsonify(code=200, msg="删除管理员成功!")

        except Exception as e:
            print(e)
            db.session.rollback()
            return jsonify(code=400, msg="执行操作失败")
    return jsonify(code=400, msg="未知错误")


####

# 删除用户
@admin.route("/user/status", methods=["DELETE"])
@admin_login_required
def delete_user():
    """
    用户的用户名
    :return:
    """
    admin_id = g.admin_id
    ip_addr = request.remote_addr  # 获取管理员登录的ip
    req_dict = request.get_json()
    delete_user_username = req_dict.get("username")

    # 参数完整的校验
    if not all([delete_user_username, ip_addr]):
        return jsonify(code=400, msg="参数不完整")

    user = User.query.filter(User.username == delete_user_username).first()
    if user is None:
        return jsonify(code=400, msg="查询不到用户")

    try:
        user.status = "删除"
        db.session.add(user)
        detail = "删除了用户: %s " % user
        admin_operate_log = AdminOperateLog(admin_id=admin_id, ip=ip_addr, detail=detail)
        db.session.add(admin_operate_log)
        db.session.commit()
        return jsonify(code=200, msg="删除用户成功!")

    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify(code=400, msg="执行操作失败")


# 删除评论
@admin.route("/comment", methods=["DELETE"])
@admin_login_required
def delete_comment():
    req_json = request.get_json()
    ip_addr = request.remote_addr
    admin_id = g.admin_id
    comment_id = req_json.get("comment_id")
    if not all([admin_id, comment_id, ip_addr]):
        return jsonify(code=4000, msg="参数不完整")

    try:
        # 删除评论
        blog = Comment.query.filter(Comment.id == comment_id).delete()
        if blog != 1:
            return jsonify(code=400, msg="删除评论失败，评论不存在")
        detail = "删除了评论 %d " % comment_id
        user_log = AdminOperateLog(admin_id=admin_id, ip=ip_addr, detail=detail)
        db.session.add(user_log)
        db.session.commit()
        return jsonify(code=200, msg="删除了评论成功")
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify(code=400, msg="删除评论失败，请稍后再试")


# 查看所有用户略情
@admin.route("/all/user/<int:page>", methods=["GET"])
@admin_login_required
def all_user_message(page):
    per_page = 20
    users = User.query.paginate(page=page, per_page=per_page)
    content = []
    for user in users.items:
        content.append(user.to_dict())
    total_page = users.pages
    return jsonify(code=200, msg="查询成功", data=content, total_page=total_page)


# 查看所有的反馈信息
@admin.route("/feedback/<int:page>", methods=["GET"])
@admin_login_required
def feed_back(page):
    """
    获取所有的反馈信息
    :return:
    """
    per_page = 20
    messages = Message.query.paginate(page, per_page, False)

    content = []
    for message in messages.items:
        content.append(message.to_dict())

    return jsonify(code=200, msg='查看反馈信息成功', data=content, total_page=messages.pages)


# 发博总数
@admin.route("/blog/numbers", methods=["POST"])
def blog_numbers():
    blog = Blog.query.filter_by(Blog.status == "正常").all()
    return jsonify(code=200, number=len(blog))


# 注册用户量
@admin.route("/register/numbers", methods=["GET"])
@admin_login_required
def register_number():
    user = User.query.all()
    number = len(user)
    return jsonify(code=200, msg="查询成功", register_numbers=number)
