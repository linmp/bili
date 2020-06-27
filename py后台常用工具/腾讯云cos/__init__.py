# APPID 已在配置中移除,请在参数 Bucket 中带上 APPID。Bucket 由 BucketName-APPID 组成
# 1. 设置用户配置, 包括 secretId，secretKey 以及 Region
# -*- coding=utf-8

import os
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client

# 配置信息
bucket = os.environ.get("COS_bucket") or 'xxx-13001735'
secret_id = os.environ.get("COS_secret_id") or 'xxxx'  # 替换为用户的 secretId
secret_key = os.environ.get("COS_secret_key") or 'xxx'  # 替换为用户的 secretKey
region = os.environ.get("COS_region") or 'ap-shanghai'  # 替换为用户的 Region
token = None  # 使用临时密钥需要传入 Token，默认为空，可不填
scheme = 'https'  # 指定使用 http/https 协议来访问 COS，默认为 https，可不填

config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key, Token=token, Scheme=scheme)
# 2. 获取客户端对象
client = CosS3Client(config)
