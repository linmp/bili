import random
from . import main
from flask import request, jsonify, session, g
from ..models import User, db, Blog
from app import redis_store
from app.utils.sms.send import send_sms
from app.utils.tool import user_login_required
from app.utils.TXcos.upload import upload_file

""""
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


# 初始页面
@main.route("/index", methods=["GET"])
def index():
    return "hello 菜鸡音宫 普通页面"


# 获取验证码
@main.route("/sms", methods=["POST"])
def sms_code():
    req_json = request.get_json()
    phone = req_json.get("phone")
    if not all([phone]):
        # 表示参数不完整
        return jsonify(code=4000, msg="参数不完整")

    # 判断对于这个手机号的操作，在60秒内有没有之前的记录，如果有，则认为用户操作频繁，不接受处理
    try:
        send_flag = redis_store.get("send_sms_code_%s" % phone)
        if send_flag is not None:
            # 表示在60秒内之前有过发送的记录
            return jsonify(code=4001, msg="请求过于频繁，请60秒后重试")
    except Exception as e:
        print(e)

    # 判断手机号是否存在
    try:
        user = User.query.filter_by(phone=phone).first()
        if user:
            # 表示手机号已存在
            return jsonify(code=4002, msg="手机号已存在")
    except Exception as e:
        print(e)

    sms_code = random.randint(100000, 999999)  # 生成验证码

    minute = 10  # 验证码有效时间 分钟

    # 保存真实的短信验证码
    try:
        # sms_code_13634802934
        redis_store.setex("sms_code_%s" % phone, minute * 60, str(sms_code))

        # 保存发送给这个手机号的记录，防止用户在60s内再次出发发送短信的操作
        redis_store.setex("send_sms_code_%s" % phone, 60, 1)

    except Exception as e:
        print(e)
        return jsonify(code=4003, msg="保存短信验证码异常,请稍后在试")

    # 发送验证码
    try:
        code = send_sms(phone, sms_code, minute)
        if code == "Ok":
            return jsonify(code=200, msg="发送成功")
        else:
            return jsonify(code=4004, msg="发送失败")
    except Exception as e:
        print(e)
        return jsonify(code=4005, msg="发送异常")


# 注册用户数据
@main.route("/register", methods=["POST"])
def user_register():
    """
    密码
    手机号
    短信验证码
    :return:
    """
    """注册"""
    req_dict = request.get_json()
    phone = req_dict.get("phone")
    password = req_dict.get("password")
    password2 = req_dict.get("password2")
    sms_code = req_dict.get("sms_code")
    phone = str(phone)
    sms_code = str(sms_code)

    # 校验参数
    if not all([phone, password, password2, sms_code]):
        return jsonify(code=4000, msg="参数不完整"), 400

    if password != password2:
        return jsonify(code=4001, msg="两次密码不一致")

    # 从redis中取出短信验证码
    try:
        real_sms_code = redis_store.get("sms_code_%s" % phone)
    except Exception as e:
        print(e)
        return jsonify(code=4002, msg="读取真实短信验证码异常")

    # 判断短信验证码是否过期
    if real_sms_code is None:
        return jsonify(code=4003, msg="短信验证码失效")

    # 删除redis中的短信验证码，防止重复使用校验
    try:
        redis_store.delete("sms_code_%s" % phone)
    except Exception as e:
        print(e)

    # 判断用户填写短信验证码的正确性
    if str(real_sms_code.decode()) != str(sms_code):
        return jsonify(code=4004, msg="短信验证码错误")

    # 判断用户的手机是否注册过
    try:
        user = User.query.filter_by(phone=phone).first()
        if user:
            # 表示已被注册
            return jsonify(code=400, msg="手机已被注册")

    except Exception as e:
        print(e)
        return jsonify(code=400, msg="数据库异常")

    # 保存用户的注册数据到数据库中
    avatar = "http://baidu.com"  # 用户头像
    user = User(username=phone, phone=phone, password=password, avatar=avatar)
    try:
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(e)
        return jsonify(code=400, msg="查询数据库异常")

    # 保存登录状态到session中
    session["user_username"] = phone
    session["user_phone"] = phone
    session["user_id"] = user.id
    session["user_avatar"] = user.avatar

    # 返回结果
    return jsonify(code=200, msg="注册成功")


# 登录
@main.route("/login", methods=["POST"])
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
    user = User.query.filter_by(username=username).first()
    # 账号密码验证成功
    if user and user.password == password:
        session["user_username"] = username
        session["user_id"] = user.id
        session["user_avatar"] = user.avatar
        return jsonify(msg="登录成功", code=200), 200
    else:
        return jsonify(msg="账号或密码错误", code=4001), 400


# 检查登录状态
@main.route("/session", methods=["GET"])
def check_session():
    username = session.get("user_username")
    if username:
        return jsonify(username=username, code=200), 200
    else:
        return jsonify(msg="出错了，没登录", code=4000), 400


# 登出
@main.route("/logout", methods=["DELETE"])
@user_login_required
def logout():
    session.clear()
    return jsonify(msg="成功退出登录!", code=200), 200


# 修改密码 # 导入g对象
@main.route("/password", methods=["PUT"])
@user_login_required
def change_password():
    """ 修改密码 """
    # 获取参数
    uid = g.user_id
    req_dict = request.get_json()
    password = req_dict.get("password")
    new_password = req_dict.get("new_password")

    # 参数完整的校验
    if not all([new_password, password, uid]):
        return jsonify(code=4000, msg="参数不完整.")

    try:
        user = User.query.get(uid)
    except Exception as e:
        print(e)
        return jsonify(code=4001, msg="获取用户信息失败")

    # 用数据库的密码与用户填写的密码进行对比验证
    if user.status is False or user.password != password:
        return jsonify(code=4002, msg="原密码密码错误")

    # 修改密码
    user.password = new_password
    try:
        db.session.add(user)
        db.session.commit()
        return jsonify(code=200, msg="修改密码成功!")
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify(code=4003, msg="修改密码失败,请稍后重试!")


# 发送找回密码验证码
@main.route("/find/password/sms", methods=["POST"])
def send_find_password_sms():
    req_dict = request.get_json()
    phone = req_dict.get("phone")
    phone = str(phone)

    # 判断对于这个手机号的操作，在60秒内有没有之前的记录，如果有，则认为用户操作频繁，不接受处理
    try:
        send_flag = redis_store.get("send_sms_code_%s" % phone)
        if send_flag:
            # 表示在60秒内之前有过发送的记录
            return jsonify(code=4001, msg="请求过于频繁，请60秒后重试")
    except Exception as e:
        print(e)

    # 判断账号是否存在
    try:
        user = User.query.filter_by(phone=phone).first()
        if user is None or user.status is False:
            # 账号不存在
            return jsonify(code=4002, msg="账号不存在或账号异常!")
    except Exception as e:
        print(e)

    # 如果账号存在且正常 发送验证码
    sms_code = random.randint(100000, 999999)  # 生成验证码
    minute = 10  # 验证码有效时间 分钟

    # 保存真实的短信验证码
    try:
        # sms_code_13634802934
        redis_store.setex("sms_code_%s" % phone, minute * 60, str(sms_code))
        # 保存发送给这个手机号的记录，防止用户在60s内再次出发发送短信的操作
        redis_store.setex("send_sms_code_%s" % phone, 60, 1)

    except Exception as e:
        print(e)
        return jsonify(code=4003, msg="保存短信验证码异常,请稍后在试")

    # 发送验证码
    try:
        code = send_sms(phone, sms_code, minute)
        if code == "Ok":
            return jsonify(code=200, msg="发送成功")
        else:
            return jsonify(code=4004, msg="发送失败")
    except Exception as e:
        print(e)
        return jsonify(code=4005, msg="发送异常")


# 找回密码
@main.route("/password", methods=["POST"])
def find_password():
    """
    发送手机号验证码
    验证成功之后就能填写个新密码
    :return:
    """
    req_dict = request.get_json()
    phone = req_dict.get("phone")
    password = req_dict.get("password")
    password2 = req_dict.get("password2")
    sms_code = req_dict.get("sms_code")
    phone = str(phone)
    sms_code = str(sms_code)

    # 校验参数
    if not all([phone, password, password2, sms_code]):
        return jsonify(code=400, msg="参数不完整")

    if password != password2:
        return jsonify(code=400, msg="两次密码不一致")

    # 从redis中取出短信验证码
    try:
        real_sms_code = redis_store.get("sms_code_%s" % phone)
    except Exception as e:
        print(e)
        return jsonify(code=4001, msg="读取真实短信验证码异常")

    # 判断短信验证码是否过期
    if real_sms_code is None:
        return jsonify(code=4002, msg="短信验证码失效")

    # 删除redis中的短信验证码，防止重复使用校验
    try:
        redis_store.delete("sms_code_%s" % phone)
    except Exception as e:
        print(e)

    # 判断用户填写短信验证码的正确性
    if str(real_sms_code.decode()) != str(sms_code):
        return jsonify(code=4003, msg="短信验证码错误")

    # 判断用户是否存在
    try:
        user = User.query.filter_by(phone=phone).first()
        if user is None or user.status is False:
            # 不存在用户
            return jsonify(code=400, msg="用户不存在或账号异常,请注册")

    except Exception as e:
        print(e)
        return jsonify(code=400, msg="数据库异常")

    # 更改用户的密码到数据库中
    user.password = password
    try:
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(e)
        return jsonify(code=400, msg="更改数据库异常")

    # 返回结果
    return jsonify(code=200, msg="找回密码成功!")


# 获取个人信息
@main.route("/user/profile/<int:user_id>", methods=["GET"])
def get_profile(user_id):
    """
    id
    用户名
    头像
    注册时间
    最新上线时间
    :return:
    """
    if not user_id:
        return jsonify(code=400, msg="参数不完整")
    user = User.query.get(user_id)
    if not user or user.status is False:
        return jsonify(code=400, msg="查询不到用户")

    # 将数据转换为json字符串
    try:
        data = {
            "id": user.id,
            "username": user.username,
            "avatar": user.avatar,
            "create_time": user.create_time.strftime("%Y-%m-%d %H:%M:%S"),
            "update_time": user.update_time.strftime("%Y-%m-%d %H:%M:%S")
        }
        resp_dict = dict(code=200, msg="查询用户信息成功!", data=data)
        return jsonify(resp_dict)
    except Exception as e:
        print(e)
        return jsonify(code=4000, msg="出错了", data=[])


# 设置用户的头像
@main.route("/user/avatar", methods=["POST"])
@user_login_required
def update_user_avatar():
    """
    设置用户的头像
    参数： 图片(多媒体表单格式)
    用户id (g.user_id)
    """

    # 装饰器的代码中已经将user_id保存到g对象中，所以视图中可以直接读取
    user_id = g.user_id
    # 获取图片
    image_file = request.files.get("file")
    if image_file is None:
        return jsonify(code=400, msg="未上传图片")

    try:

        file_name = upload_file(image_file)

    except Exception as e:
        print(e)
        return jsonify(code=400, msg="上传图片失败")

    # 保存图片路由到数据库中
    try:
        User.query.filter_by(id=user_id).update({"avatar": file_name})

        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(e)
        return jsonify(code=400, msg="保存图片信息失败")

    avatar_url = file_name

    # 保存成功返回
    session["avatar"] = avatar_url
    return jsonify(code=200, msg="保存成功", data={"avatar": avatar_url})


# 修改用户的用户名 //
@main.route("/user/username", methods=["PUT"])
@user_login_required
def update_username():
    """
    设置用户的用户名
    参数：
    username 要更改的用户名
    用户id (g.user_id)
    """

    # 装饰器的代码中已经将user_id保存到g对象中，所以视图中可以直接读取
    user_id = g.user_id

    req_json = request.get_json()
    ip_addr = request.remote_addr
    username = req_json.get("username")

    if username is None:
        return jsonify(code=400, msg="用户名不可为空")

    # 查询数据库是否有这个用户
    find_user = User.query.filter_by(username=username).first()
    if find_user is not None:
        return jsonify(code=400, msg="用户名已被占用,无法执行本次修改")

    # 更新用户名到数据库中
    try:
        User.query.filter_by(id=user_id).update({"username": username})
    except Exception as e:
        db.session.rollback()
        print(e)
        return jsonify(code=400, msg="更改用户名失败")

    # 保存成功返回
    session["username"] = username
    return jsonify(code=200, msg="保存成功", data={"username": username})


# 搜索 # 分页 # 模糊查找
@main.route("/blog/search/<int:page>", methods=["POST"])
def blog_search(page):
    keyword = request.get_json().get("keyword")
    if not page:
        page = 1
    else:
        page = int(page)

    if keyword is None:
        return jsonify(code=400, msg="请输入搜索内容"), 400


    blogs = Blog.query.filter_by(status="发布").filter(Blog.title.like("%" + keyword + "%")).paginate(page,
                                                                                                       per_page=5,
                                                                                                       error_out=False).items
    payload = [blog.to_dict() for blog in blogs]
    return jsonify(code=200, msg="搜索结束", data=payload)


"""
# 反馈
@main.route("/message", methods=["POST"])
@user_login_required
def message():
    req_json = request.get_json()
    ip_addr = request.remote_addr
    sender_id = g.user_id
    recipient_id = req_json.get("recipient_id")
    content = req_json.get("content")
    if not all([sender_id, recipient_id, content, ip_addr]):
        return jsonify(code=4000, msg="参数不完整")
    msg = Message(sender_id=sender_id, recipient_id=recipient_id, content=content)
    try:
        db.session.add(msg)
        db.session.commit()
        return jsonify(code=200, msg="你的反馈发送成功,感谢你的反馈")
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify(code=400, msg="操作数据库失败,请稍后再试")


# 搜索 # 分页
@main.route("/blog/search/<int:page>", methods=["POST"])
def blog_search(page):
    keyword = request.get_json().get("keyword")
    if not page:
        page = 1
    else:
        page = int(page)

    if keyword is None:
        return jsonify(code=400, msg="请输入搜索内容"), 400

    key_remark = keyword
    blogs = Blog.query.filter_by(status=True).filter(Blog.title.like("%" + key_remark + "%")).paginate(page,
                                                                                                       per_page=5,
                                                                                                       error_out=False).items
    payload = [blog.to_dict() for blog in blogs]
    return jsonify(code=200, msg="搜索结束", data=payload)


# 获取博客详情
@main.route("/blog/article/detail/<int:blog_id>", methods=["GET", "POST"])
def get_article_detail(blog_id):
    blog = Blog.query.get(blog_id)
    if blog is None or blog.status != "正常":
        return jsonify(code=4001, msg="博客不存在")
    try:
        # 增加浏览次数
        blog.page_views += 1
        db.session.add(blog)
        db.session.commit()
    except Exception as e:
        print(e)
        db.session.rollback()

    try:
        data = blog.to_dict()
        return jsonify(code=200, data=data)
    except Exception as e:
        print(e)
        return jsonify(code=4002, msg="出错")


# 评论
@main.route("/comment", methods=["POST"])
@user_login_required
def comment():
    req_json = request.get_json()
    ip_addr = request.remote_addr
    sender_id = g.user_id
    blog_id = req_json.get("blog_id")
    content = req_json.get("content")
    if not all([sender_id, blog_id, content, ip_addr]):
        return jsonify(code=4000, msg="参数不完整")
    com = Comment(sender_id=sender_id, blog_id=blog_id, content=content)
    try:
        db.session.add(com)
        db.session.commit()
        return jsonify(code=200, msg="发布评论成功")
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify(code=400, msg="操作数据库失败,请稍后再试")


# 删自己评论
@main.route("/comment", methods=["DELETE"])
@user_login_required
def delete_comment():
    req_json = request.get_json()
    ip_addr = request.remote_addr
    sender_id = g.user_id
    comment_id = req_json.get("comment_id")
    if not all([sender_id, comment_id, ip_addr]):
        return jsonify(code=4000, msg="参数不完整")

    try:
        # 删除评论
        blog = Comment.query.filter(Comment.id == comment_id, Comment.sender_id == sender_id).delete()
        if blog != 1:
            return jsonify(code=400, msg="删除评论失败，评论不存在或者你不是评论主人")
        db.session.commit()
        return jsonify(code=200, msg="删除了评论成功")
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify(code=400, msg="删除评论失败，请稍后再试")


# 收藏博客
@main.route("/blog/collect", methods=["POST"])
@user_login_required
def blog_collect():
    req_json = request.get_json()
    ip_addr = request.remote_addr
    user_id = g.user_id
    blog_id = req_json.get("blog_id")
    if not all([user_id, blog_id, ip_addr]):
        return jsonify(code=4000, msg="参数不完整")

    blog = Blog.query.get(blog_id)
    if blog_id is None or blog.status != "正常":
        return jsonify(code=4001, msg="博客不存在")

    # 查询是否已经收藏
    try:
        bc_find = CollectBlogArticle.query.filter(CollectBlogArticle.user_id == user_id,
                                                  CollectBlogArticle.blog_id == blog_id).first()
        if bc_find is not None:
            return jsonify(code=4002, msg="你已经收藏")
    except Exception as e:
        print(e)
        return jsonify(code=400, msg="查询数据库失败,请稍后再试")

    # 添加收藏
    bc = CollectBlogArticle(user_id=user_id, blog_id=blog_id)
    try:
        db.session.add(bc)
        db.session.commit()
        return jsonify(code=200, msg="收藏文章成功")
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify(code=400, msg="操作数据库失败,请稍后再试")


# 取消收藏博客
@main.route("/blog/collect", methods=["DELETE"])
@user_login_required
def delete_blog_collect():
    req_json = request.get_json()
    ip_addr = request.remote_addr
    user_id = g.user_id
    collect_blog_article_id = req_json.get("collect_blog_article_id")
    if not all([user_id, collect_blog_article_id, ip_addr]):
        return jsonify(code=4000, msg="参数不完整")

    try:
        # 取消收藏
        delete_collect_blog_article = CollectBlogArticle.query.filter(CollectBlogArticle.id == collect_blog_article_id,
                                                                      CollectBlogArticle.user_id == user_id).delete()
        if delete_collect_blog_article != 1:
            return jsonify(code=400, msg="取消收藏博客失败,查不到相关收藏信息")
        db.session.commit()
        return jsonify(code=200, msg="取消收藏博客成功")
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify(code=400, msg="取消收藏博客失败，请稍后再试")
"""
