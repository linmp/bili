import oss2
from datetime import datetime
import random

from .config import OssAccessKeyID, OssAccessKeySecret, OssBucketName, OssEndpoint, OssHttps


# 上传图片到阿里云的接口
def upload_pic(path, img):
    """
    上传图片到阿里云的接口
    调用这个方法的时候
    1.from app.oss import upload
    2.upload.upload_pic(path,images)
    :param path: 这里是上传到oos里面的哪个文件夹,例如：path = "first/"
    :param img: 这里是接收的图片
    :return: 返回的是图片上传后的具体url
    """

    auth = oss2.Auth(OssAccessKeyID, OssAccessKeySecret)
    bucket = oss2.Bucket(auth, OssEndpoint, OssBucketName)

    # 修改文件名字为自定义的
    try:
        get_hz = img.filename.rsplit('.', 1)[1]  # 获取后缀
        randomNum = random.randint(0, 100)
        img.filename = datetime.now().strftime("%Y%m%d%H%M%S") + "_" + str(randomNum) + "." + get_hz
    except Exception as e:
        print(e)
        img.filename = datetime.now().strftime("%Y%m%d%H%M%S") + img.filename

    file_path = path + img.filename  # 拼接文件夹跟更改后的文件名
    bucket.put_object(file_path, img)  # 前一个是文件的名字，后一个是文件的数据
    url = OssHttps + file_path  # 具体外网可访问的路由
    return url
