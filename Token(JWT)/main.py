import time
import json
import base64
import hashlib
import hmac

salt = "hao-yin-gong"
exp = 1000


headers = {
    "typ": "ygt",
    "exp": int(time.time() + exp)  # 过期时间戳
}

payload = {
    "uid": 1,
    "author": "好音宫",
    "admin": 1
}


# 生产header
first = base64.urlsafe_b64encode(json.dumps(headers, separators=(',', ':')).encode('utf-8').replace(b'=', b'')).decode(
    'utf-8').replace('=', '')
# 生成payload
second = base64.urlsafe_b64encode(json.dumps(payload, separators=(',', ':')).encode('utf-8').replace(b'=', b'')).decode(
    'utf-8').replace('=', '')
first_second = f"{first}.{second}"
# 生成签名
third = base64.urlsafe_b64encode(
    hmac.new(salt.encode('utf-8'), first_second.encode('utf-8'), hashlib.sha256).digest()).decode('utf-8').replace('=',
                                                                                                                   '')

# 拼接成token
token = ".".join([first, second, third])
print(token)


# 解析token
headers = token.split(".")[0]
payload = token.split(".")[1]
sign = token.split(".")[2]


# 对数据签名、判断token上对签名是否是合规对
headers_payload = f"{headers}.{payload}"
new_sign = base64.urlsafe_b64encode(
    hmac.new(salt.encode('utf-8'), headers_payload.encode('utf-8'), hashlib.sha256).digest()).decode(
    'utf-8').replace(
    '=',
    '')


print(new_sign == sign)


################################
if isinstance(payload, str):
    payload = payload.encode('ascii')
rem = len(payload) % 4
if rem > 0:
    payload += b'=' * (4 - rem)
# 上面这一部分是解密的部分数据补全格式


payload_data = base64.urlsafe_b64decode(payload)  # 解码
data = json.loads(payload_data)  # 将已编码的JSON字符串解码为Python对象，即将payload转为可以通过get方法获取里面的值

print(data.get("author"))  # 打印token里面的payload部分中的uid数据信息
