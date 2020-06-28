import os

OssAccessKeyID = os.environ.get("OssAccessKeyID") or "xxxx"
OssAccessKeySecret = os.environ.get("OssAccessKeySecret") or "xxxx"
OssBucketName = os.environ.get("OssBucketName") or "jamkung"

# 例如 "http://oss-cn-shanghai.aliyuncs.com"
OssEndpoint = os.environ.get("OssEndpoint") or "http://oss-cn-shanghai.aliyuncs.com"

# 例如 "https://xxxxxx.oss-cn-shanghai.aliyuncs.com/"
OssHttps = os.environ.get(("OssHttps"))
