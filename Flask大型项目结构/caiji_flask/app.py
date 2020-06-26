from flask import Flask, session, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
import redis
import pymysql

app = Flask(__name__)

# 数据库的配置

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:jamkung@pukgai.com:3306/caiji_flask'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "sdfsdfsdf"

db = SQLAlchemy(app)  # 实例化的数据库


# 用户表
class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)  # 主键
    username = db.Column(db.String(64), nullable=False, unique=True)  # 账户
    password = db.Column(db.String(64), nullable=False)  # 密码
    phone = db.Column(db.String(11))  # 手机号 可以为空
    address = db.Column(db.String(11))  # 地址


try:
    db.create_all()
except:
    pass

#########################
#   session 存redis上   #
#########################
app.config["SESSION_TYPE"] = "redis"  # 存session进redis
app.config["SESSION_USE_SIGNER"] = True  # 对cookie中session_id进行隐藏处理 加密混淆
app.config["PERMANENT_SESSION_LIFETIME"] = 10  # session数据的有效期，单位秒
app.config['SESSION_REDIS'] = redis.Redis(host='pukgai.com', port=6379, password="jamkung", db=2)  # 操作的redis配置

# 利用flask-session，将session数据保存到redis中
Session(app)


# 成功响应
@app.route("/", methods=["GET"])
def hello_world():
    return "hello 音宫"


# 用户注册
@app.route("/user/register", methods=["POST"])
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
@app.route("/user/login", methods=["POST"])
def login():
    get_data = request.get_json()
    username = get_data.get("username")
    password = get_data.get("password")

    if not all([username, password]):
        return jsonify(msg="参数不完整", code=4000)

    user = User.query.filter_by(username=username).first()
    # 如果用户存在并且密码对
    if user and user.password == password:
        # 如果验证通过 保存登录状态在session中
        session["username"] = username
        return jsonify(msg="登录成功", code=200, username=username)
    else:
        return jsonify(msg="账号或密码错误", code=4001)


# 检查登录状态
@app.route("/user/session", methods=["GET"])
def check_session():
    username = session.get("username")
    if username is not None:
        # 操作逻辑 数据库什么的
        # 数据库里面 把你的头像 等级 金币数量 查询出来
        return jsonify(username=username, code=200)
    else:
        return jsonify(msg="出错了，没登录", code=4000)


# 登出
@app.route("/user/logout", methods=["DELETE"])
def logout():
    username = session.get("username")
    if username is None:
        return jsonify(msg="出错了，没登录!", code=4000)

    session.clear()
    return jsonify(msg="成功退出登录!", code=200)


if __name__ == '__main__':
    app.run()
