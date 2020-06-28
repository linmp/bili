安装 SDK

    使用 pip 安装（推荐）
    pip install -U cos-python-sdk-v5

### 配置信息
```python
bucket = os.environ.get("COS_bucket") or 'mnp-1300173558'
secret_id = os.environ.get("TENCENT_APP_ID") or 'xxxx'  # 替换为用户的 secretId
secret_key = os.environ.get("TENCENT_APP_KEY") or 'xxxx'  # 替换为用户的 secretKey
region = os.environ.get("COS_region") or 'ap-shanghai'  # 替换为用户的 Region
token = None  # 使用临时密钥需要传入 Token，默认为空，可不填
scheme = 'https'  # 指定使用 http/https 协议来访问 COS，默认为 https，可不填


```

