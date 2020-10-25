import time
import json
import base64
import hashlib
import hmac


class YgToken:
    def __init__(self, salt="hao-yin-gong", exp=600):
        self.salt = salt
        self.exp = exp

    def create_token(self, payload=None):
        headers = self.__create_header(self.exp)
        payload = self.__create_payload(payload)

        headers = self.__encode_data(headers)
        payload = self.__encode_data(payload)
        sign = self.__encode_sign(headers, payload, self.salt)

        token = ".".join([headers, payload, sign])
        return token

    # 解析token
    def load_token(self, token):
        # 判断是否是基本的token结构
        try:
            headers = token.split(".")[0]
            payload = token.split(".")[1]
            sign = token.split(".")[2]

        except Exception as e:
            print(e)
            payload = None
            token_status = {
                "msg": "token错误",
                "ok": False
            }
            return payload, token_status

        # 验证签名
        new_sign = self.__encode_sign(headers=headers, payload=payload, salt=self.salt)
        if new_sign != sign:
            payload = None
            token_status = {
                "msg": "签名错误",
                "ok": False
            }
            return payload, token_status

        # 判断是否过期
        try:
            headers = self.__decode_data(headers)
            is_exp = headers.get("exp") < int(time.time())
            if is_exp:
                payload = None
                token_status = {
                    "msg": "已经过期",
                    "ok": False
                }
                return payload, token_status

        except Exception as e:
            print(e)
            payload = None
            token_status = {
                "msg": "headers错误",
                "ok": False
            }
            return payload, token_status

        # 返回payload
        payload = self.__decode_data(payload)

        token_status = {
            "msg": "解析token正确",
            "ok": True
        }
        return payload, token_status

    # 创建 头部
    def __create_header(self, exp):
        headers = {
            "typ": "ygt",
            "exp": int(time.time() + exp)  # 过期时间戳
        }
        return headers

    # 创建数据部分
    def __create_payload(self, payload):
        if payload is None:
            default_payload = {
                "uid": 1,
                "author": "好音宫",
                "role": "up"
            }
            payload = default_payload
        return payload

    def __encode_data(self, data):
        result_data = base64.urlsafe_b64encode(
            json.dumps(data, separators=(',', ':')).encode('utf-8').replace(b'=', b'')).decode(
            'utf-8').replace('=', '')
        return result_data

    def __encode_sign(self, headers, payload, salt):
        headers_payload = f"{headers}.{payload}"

        sign = base64.urlsafe_b64encode(
            hmac.new(salt.encode('utf-8'), headers_payload.encode('utf-8'), hashlib.sha256).digest()).decode(
            'utf-8').replace(
            '=',
            '')
        return sign

    def __decode_data(self, data):
        if isinstance(data, str):
            data = data.encode('ascii')
        rem = len(data) % 4
        if rem > 0:
            data += b'=' * (4 - rem)
        data = base64.urlsafe_b64decode(data)
        return json.loads(data)


if __name__ == '__main__':
    payload = {
        "say": "我爱你",
        "from": "音宫",
        "to": "小姐姐",
        "uid": 1,
        "role": "admin"
    }

    salt = "hyg"
    exp = 1000
    ygt = YgToken(salt=salt, exp=exp)
    token = ygt.create_token(payload)
    p, m = ygt.load_token(token=token)
    print(p)
    print(m)
