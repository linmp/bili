from flask import Flask, request, jsonify
# from app.腾讯云cos import upload
from app.阿里云oss import upload

app = Flask(__name__)


# 上传文件
@app.route("/upload", methods=["POST"])
def upload_pic():
    file = request.files.get('file')
    # 保存图片到对象存储
    try:
        # file_url = upload.upload_file(file)
        file_url = upload.upload_file(file)
    except Exception as e:
        print(e)
        return jsonify(code=400, msg="上传失败"), 400
    return jsonify(code=200, msg="保存图片数据成功", file_url=file_url), 200


if __name__ == '__main__':
    app.run()
