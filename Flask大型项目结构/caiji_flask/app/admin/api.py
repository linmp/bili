from . import admin


# 初始页面
@admin.route("/index", methods=["GET"])
def index():
    return "hello 菜鸡音宫 管理员页面"
