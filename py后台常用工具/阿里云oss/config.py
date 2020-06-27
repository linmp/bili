import os

OssAccessKeyID = os.environ.get("OssAccessKeyID")
OssAccessKeySecret = os.environ.get("OssAccessKeySecret")
OssBucketName = os.environ.get("OssBucketName")
OssEndpoint = os.environ.get("OssEndpoint")  # 例如 "http://oss-cn-shanghai.aliyuncs.com"
OssHttps = os.environ.get(("OssHttps"))  # 例如 "https://xxxxxx.oss-cn-shanghai.aliyuncs.com/"
