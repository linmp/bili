from flask import Flask

app = Flask(__name__)


# 数据库
# session


@app.route("/admin/login")
def admin_login():
    return "管理员登录"


@app.route("/admin/login")
def main_login():
    return "主页登录"


if __name__ == '__main__':
    app.run()
