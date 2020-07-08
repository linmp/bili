from datetime import datetime
import random
from . import client, bucket, region
from werkzeug.utils import secure_filename


def upload_file(file, path="/default/"):
    """
    :param file: 字节流
    :param path: 上传到腾讯云里面的文件夹路径 比如目标是/mini/img/a.jpg
                    则上传 /mini/img/
    :return:
    """

    body = rename(file)
    key = path + file.filename

    response = client.put_object(
        Bucket=bucket,
        Body=body,
        Key=key,
        EnableMD5=False
    )
    # print(response['ETag'])
    url = "https://" + bucket + ".cos." + region + ".myqcloud.com" + key
    return url


def rename(file):
    """
    修改文件名字为 自定义的 不重复的
    :param file:文件数据
    :return:
    """
    filename = secure_filename(file.filename)

    try:
        get_hz = filename.rsplit('.', 1)[1]  # 获取后缀
        random_num = random.randint(0, 100)
        file.filename = datetime.now().strftime("%Y%m%d%H%M%S") + "_" + str(random_num) + "." + get_hz
    except Exception as e:
        print(e)
        file.filename = datetime.now().strftime("%Y%m%d%H%M%S.") + filename
    return file
