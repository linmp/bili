from yg_token.yg_token import YgToken

print(YgToken().create_token())

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

print(p, p.get("say"))
print(m, m.get("ok"))
