from datetime import datetime
from flask import Flask, request, jsonify
import os
import random
from werkzeug.utils import secure_filename

# # 获取当前位置的绝对路径
basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)


# 上传照片test接口
@app.route("/upload", methods=["POST"])
def upload():
    f = request.files.get('file')
    # 获取安全的文件名 正常的文件名
    filename = secure_filename(f.filename)
    print(filename)

    # 生成随机数
    random_num = random.randint(0, 100)

    # f.filename.rsplit('.', 1)[1] 获取文件的后缀
    # 把文件重命名
    filename = datetime.now().strftime("%Y%m%d%H%M%S") + "_" + str(random_num) + "." + filename.rsplit('.', 1)[1]

    # 保存的目标绝对地址
    file_path = basedir + "/static/file/"

    # 判断文件夹是否存在 不存在则创建
    if not os.path.exists(file_path):
        os.makedirs(file_path, 755)

    # 保存文件到目标文件夹
    f.save(file_path + filename)

    # 返回前端可调用的一个链接
    # 可以配置成对应的外网访问的链接
    my_host = "http://127.0.0.1:5000"
    new_path_file = my_host + "/static/file/" + filename
    data = {"msg": "success", "url": new_path_file}

    payload = jsonify(data)
    return payload, 200


if __name__ == '__main__':
    app.run()
