from . import main


# 初始页面
@main.route("/index", methods=["GET"])
def index():
    return "hello 菜鸡音宫 普通页面"
