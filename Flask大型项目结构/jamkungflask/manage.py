from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
import redis
app = Flask(__name__)


# 数据库
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:jamkung@pukgai.com:3306/jamkungflaskdevelop'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'xxasdasdasdx'

# flask-session配置
SESSION_TYPE = "redis"
REDIS_HOST = "pukgai.com"
REDIS_PORT = "6379"
REDIS_PASSWORD = "jamkung"
SESSION_REDIS = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT,
                                  password=REDIS_PASSWORD, db=2)

SESSION_USE_SIGNER = True  # 对cookie中session_id进行隐藏处理、加密
PERMANENT_SESSION_LIFETIME = 86400  # session数据的有效期，单位秒
app.config["SESSION_TYPE"] = SESSION_TYPE
app.config["SESSION_REDIS"] = SESSION_REDIS
app.config["SESSION_USE_SIGNER"] = SESSION_USE_SIGNER
app.config["PERMANENT_SESSION_LIFETIME"] = PERMANENT_SESSION_LIFETIME
Session(app)
db = SQLAlchemy(app)


@app.route("/admin/login")
def admin_login():
    session["admin"] = "admin_login_success"
    return "管理员登录"


@app.route("/main/login")
def main_login():
    session["user"] = "user_login_success"
    return "主页登录"


if __name__ == '__main__':
    app.run()
