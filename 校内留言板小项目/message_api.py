from flask import jsonify, request, session

from message_models import app, db, Admin, Tag, User, Message

"""
状态码 200 成功
状态码 400 失败
"""


@app.route("/index")
@app.route("/")
def hello_world():
    return "hello world"


# 管理员初始化 //
@app.route("/init/admin")
def init_admin():
    """
    账号：admin
    密码：default

    :return:
    """
    admin = Admin(username="admin", password="default")
    try:
        db.session.add(admin)
        db.session.commit()
        return jsonify(code=200, msg="初始化管理员成功")
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify(code=400, msg="初始化管理员失败")


# 管理员登录 //
@app.route("/admin/login", methods=["POST"])
def login_admin():
    """
    传 账号 和 密码
    :return:
    """
    req_data = request.get_json()
    username = req_data.get("username")  # 获取账号
    password = req_data.get("password")  # 获取密码
    if not all([username, password]):
        return jsonify(code=400, msg="参数不完整")

    admin = Admin.query.filter(Admin.username == username).first()

    # 查找数据库管理员 # 验证密码
    if admin is None or password != admin.password:
        return jsonify(code=400, msg="账号或密码错误")

    session["admin_name"] = username
    session["admin_id"] = admin.id

    return jsonify(msg="登录成功")


# 检查登录状态 //
@app.route("/admin/session", methods=["GET"])
def check_admin_session():
    username = session.get("admin_name")
    admin_id = session.get("admin_id")

    if username is not None:
        # 操作逻辑 数据库什么的
        # 数据库里面 把你的头像 等级 金币数量 查询出来
        return jsonify(username=username, admin_id=admin_id)
    else:
        return jsonify(msg="出错了，没登录")


# 管理员退出登录 //
@app.route("/admin/logout")
def logout_admin():
    session.clear()
    return jsonify(msg="成功退出登录!")


# 管理员增标签 //
@app.route("/admin/tag", methods=["POST"])
def add_tag():
    """
    tag_name
    :return:
    """

    req_data = request.get_json()
    tag_name = req_data.get("tag_name")  # 获取标签名
    admin_id = session.get("admin_id")  # 获取管理员的id

    # 参数不完整或者没登录
    if not all([tag_name, admin_id]):
        return jsonify(code=400, msg="参数不完整或未登录")

    tag = Tag(name=tag_name, admin_id=admin_id)
    try:
        db.session.add(tag)
        db.session.commit()
        return jsonify(code=200, msg="添加标签成功")
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify(code=400, msg="添加标签失败")


# 管理员删标签 //
@app.route("/admin/tag", methods=["DELETE"])
def delete_tag():
    req_data = request.get_json()
    tag_name = req_data.get("tag_name")  # 获取标签名
    admin_id = session.get("admin_id")  # 获取管理员的id

    # 参数不完整或者没登录
    if not all([tag_name, admin_id]):
        return jsonify(code=400, msg="参数不完整或未登录")

    try:
        tag = Tag.query.filter(Tag.name == tag_name).delete()

        db.session.commit()
        return jsonify(code=200, msg="删除标签成功")
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify(code=400, msg="删除标签失败")


# 管理员删留言  //
@app.route("/admin/message", methods=["DELETE"])
def admin_delete_message():
    req_data = request.get_json()
    message_id = req_data.get("message_id")
    admin_id = session.get("admin_id")

    if not all([message_id, admin_id]):
        return jsonify(code=400, msg="参数不完整")

    # 判断留言存在吗
    msg = Message.query.get(message_id)
    if msg is None:
        return jsonify(code=400, msg="留言不存在，无法删除操作")

    try:
        m = Message.query.filter(Message.id == message_id).delete()
        db.session.commit()
        return jsonify(code=200, msg="删除成功")
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify(code=400, msg="删除失败")


# 用户注册 //
@app.route("/user/register", methods=["POST"])
def user_register():
    """
    账号
    密码
    用户名
    :return:
    """
    req_data = request.get_json()
    username = req_data.get("username")
    password = req_data.get("password")

    user = User(username=username, password=password)
    try:
        db.session.add(user)
        db.session.commit()
        return jsonify(code=200, msg="注册用户成功")
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify(code=400, msg="注册失败")


# 用户登录 //
@app.route("/user/login", methods=["POST"])
def user_login():
    req_data = request.get_json()
    username = req_data.get("username")  # 获取账号
    password = req_data.get("password")  # 获取密码
    if not all([username, password]):
        return jsonify(code=400, msg="参数不完整")

    user = User.query.filter(User.username == username).first()

    # 查找数据库管理员 # 验证密码
    if user is None or password != user.password:
        return jsonify(code=400, msg="账号或密码错误")

    session["user_name"] = username
    session["user_id"] = user.id

    return jsonify(msg="登录成功")


# 检查登录状态 //
@app.route("/user/session", methods=["GET"])
def check_user_session():
    username = session.get("user_name")
    user_id = session.get("user_id")

    if username is not None:
        # 操作逻辑 数据库什么的
        return jsonify(username=username, user_id=user_id)
    else:
        return jsonify(msg="出错了，没登录")


# 用户退出登录 //
@app.route("/user/logout")
def user_logout():
    session.clear()
    return jsonify(msg="成功退出登录!")


# 用户发布留言 //
@app.route("/user/message", methods=["POST"])
def user_post_message():
    req_data = request.get_json()
    user_id = session.get("user_id")
    tags = req_data.get("tags")  # ["a","aa","aaa"]
    content = req_data.get("content")

    if not all([user_id, tags, content]):
        return jsonify(code=400, msg="参数不完整")

    try:
        tags = Tag.query.filter(Tag.name.in_(tags)).all()
        message = Message(content=content, user_id=user_id)
        message.tags = tags
        db.session.add(message)
        db.session.commit()
        return jsonify(code=200, msg="发布留言成功")

    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify(code=400, msg="发布留言失败")


# 用户删除留言 //
@app.route("/user/message", methods=["DELETE"])
def user_delete_message():
    """
    上传留言对应的id
    作者的user_id判断作者
   :return:
    """
    req_data = request.get_json()
    message_id = req_data.get("message_id")
    user_id = session.get("user_id")

    if not all([message_id, user_id]):
        return jsonify(code=400, msg="参数不完整")

    # 判断留言存在吗
    msg = Message.query.get(message_id)
    if msg is None:
        return jsonify(code=400, msg="留言不存在，无法删除操作")
    # 判断用户是不是作者
    if user_id != msg.user.id:
        return jsonify(code=400, msg="你不是作者，无法删除操作")

    try:
        m = Message.query.filter(Message.id == message_id).delete()
        db.session.commit()
        return jsonify(code=200, msg="删除成功")
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify(code=400, msg="删除失败")


# 用户查看自己留言记录 //
@app.route("/user/message/history", methods=["GET"])
def user_messages_history():
    user_id = session.get("user_id")
    if user_id is None:
        return jsonify(code=400, msg="请登录")
    user = User.query.get(user_id)
    if user is None:
        return jsonify(code=400, msg="用户不存在")

    # 获取留言 ////////////
    payload = []
    messages = user.messages
    for message in messages:
        content = message.content,
        # 获取tags
        tag_names = []
        tags = message.tags,
        for tag in tags:
            for t in tag:
                print(t.name, "a")
                tag_names.append(t.name)
        # 生成器
        # tag_names = [t.name for t in tag for tag in tags]

        create_time = message.create_time.strftime("%Y-%m-%d %H:%M:%S"),
        user_id = message.user_id
        data = {"content": content,
                "message_id": message.id,
                "tags": tag_names,
                "create_time": create_time,
                "user_id": user_id}
        print(data)
        payload.append(data)
    return jsonify(code=200, msg="查询成功", data=payload)


# 留言板留言区 //
@app.route("/user/message/board", methods=["GET"])
def user_messages_board():

    messages = Message.query.all()
    payload = []
    for message in messages:
        content = message.content,
        # 获取tags
        tag_names = []
        tags = message.messages,
        for tag in tags:
            for t in tag:
                print(t.name, "a")
                tag_names.append(t.name)
        # 生成器
        # tag_names = [t.name for t in tag for tag in tags]

        create_time = message.create_time.strftime("%Y-%m-%d %H:%M:%S"),
        user_id = message.user_id
        data = {"content": content,
                "message_id": message.id,
                "tags": tag_names,
                "create_time": create_time,
                "user_id": user_id}
        print(data)
        payload.append(data)
    return jsonify(code=200, msg="查询成功", data=payload)


if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5050)
