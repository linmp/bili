## 1.初次认识Token

讲一下什么是token，这里的token默认说的是JWT(Json Web Token)

### 体验Json Web Token

[在线生成JWT](https://jwt.io/)



### token类型

**传统的token**

传统的token是某个用户登陆之后，服务器返回一个token给用户保存，这个token可能是随机几个字母的组合，并且服务器保留同一份token(比如用redis存储token)

当用户对其他的接口访问时，必须携带这个token，接着服务器判断这个token是否存在与redis中，来判断用户是否已经登陆或者是否有相应的权限



**JWT(json web token)**

与传统token不同的是，json web token是不用保留一份在服务器上的。

处理流程：

用户登陆之后，服务器通过计算，返回一个按照一定规则加密过的token，token里面包含用户的一些必要信息，比如用户的id、token过期时间

当用户访问其他的接口时，必须携带这个token，接着服务器通过密码来验证这个token

-   验证token是否是服务器发送的token
-   验证token过期时间

一切都正确之后，才认为用户是已经登陆、有相应权限的



### 什么地方会用到token？

在我们前后端分离的开发中，往往需要为多端服务提供认证，比如移动端、web端、小程序端，用户千千万个，接口千千万个

而我们后台怎么样才能保证每个接口只允许有权限的用户来访问呢？（比如只能管理员访问或者只允许登陆的用户访问）

处理办法就是可以返回一个JWT给用户了，然后再从这个token里面判断当前访问接口用户是否符合我们设定



## 2.Json Web Token的特点

### 优点

-   不用储存用户的登录状态信息到服务器上面（比如redis）
-   同一个Token在不同的服务器器、环境、甚至不同的业务服务都可以使用（只要配置好密钥之类的）
-   可以手机端、web端、小程序端等等使用

### 缺点

当然坏处也是有的

比如生成和解析token都需要时间，对比于传统的token验证方式，JWT的生成与解析花的时间会比较多

比如不能取消已经发布存在的token(如果token泄露，在token有效期内，即使用户已经改了密码，攻击者仍然可以拿该tokne为所欲为)



## 3.Token的原理

如果你已经进入过[在线生成JWT](https://jwt.io/)这个网站，那么你可以看到这个图

Json web token 包含三部分，头部、数据、签名

![JWT结构](https://cdn.hicaiji.com/halo/JWT_structure_1603373585781.png?image/auto-orient,1/resize,m_lfit,w_200/quality,q_90)



### 头部

头部可以放一些关于token的信息，比如加密算法的信息，创建token的时间，过期的时间，然后用base64进行加密

**注意**（base64加密后的数据是任何人都可以解密，相当于透明）

比如

```python
{
  "typ": "jwt", # token类型
  "iat": 1603426198, # 生成时间
  "exp": 1603426298 # 过期时间
}
```



### 数据

数据这里可以放一些用户的id、权限等级之类的，不过请不要放隐秘的数据，比如(用户的密码、用户的真实姓名)

**注意**（因为头部和数据这两部分是任何人都可以使用base64解密的）

```python
{
  "say": "我爱你",
  "from": "音宫",
  "to": "小姐姐",
  "uid": 1,
  "role": "admin"
}
```



### 签名

签名这部分才是JWT的精华之处，把头部和数据两段字符串进行哈希加密，而这个哈希加密跟base64加密不一样，哈希加密是需要密码的，这个密码不能透露给用户，也就是加密后的内容是不可逆的

比如加密方式如下

```python
HMACSHA256(
  base64UrlEncode(header) + "." +
  base64UrlEncode(payload),
  secret)
```



什么意思呢？

**比如**头部部分记录的是7点创建，8点过期，即有效期一个小时。

数据部分记录的是某个用户的id。

这个时候服务器通过密码加密之后，会形成一串字符串（只要头部和数据部分的数据不改变，那么每次加密都会形成一样的字符串）

你7-8点之间访问服务接口都可以正常使用

**然而**，9点钟的时候，黑客发现了你这个token，不过token已经过期，然后黑客改了头部的过期时间，然后再用这个token来访问服务接口

这时候就会出错，为什么呢？

**因为**头部的信息改动之后，签名就会改变，然而黑客没有生成token的密码，使用黑客不能构造正确的签名



后台验证token的时候，会把头部和数据部分进行用密码加密，生成一个签名，然后再与提交上来的token对比是否一致



## 4.生成token

这里使用python来演示生成token

首先我们要导入几个包

```
import time
import json
import base64
import hashlib
import hmac
```

分别是用于获取当前时间、生成和解析json格式、加密的工具



提前准备好两个参数

```python
exp=60 # token有效期 秒

salt="xxx" # 加密的密码 不能让用户知道
```



**处理头部header**

```python
    headers = {
        "typ": "ygt",
        "exp": int(time.time() + exp)  # 过期时间戳
    }
```

加密头部

```pyton
first = base64.urlsafe_b64encode(json.dumps(headers, separators=(',', ':')).encode('utf-8').replace(b'=', b'')).decode(
    'utf-8').replace('=', '')
```



**处理数据payload**

这里payload存储的是一些用户数据（uid、角色、之类的），注意：不要把隐私的数据放这里（比如用户的密码等等）

```python
payload = {
  "uid": 1,
  "author": "好音宫",
  "admin": 1
}
```

加密payload

```
second = base64.urlsafe_b64encode(json.dumps(payload, separators=(',', ':')).encode('utf-8').replace(b'=', b'')).decode(
    'utf-8').replace('=', '')
```



**加密签名**

第三部分是签名，签名需要用到salt，也就是加密的密码

把前两部分拼接之后，用哈希加密把签名两部分加密得到一个字符串，这个字符串就叫做签名啦

```python
# 拼接前两部分
first_second = f"{first}.{second}"

# 对前面两部分签名呀
third = base64.urlsafe_b64encode(
    hmac.new(salt.encode('utf-8'), first_second.encode('utf-8'), hashlib.sha256).digest()).decode('utf-8').replace('=',
                                                                                                                   '')

# 拼接签名和前两部分，就叫做token啦
token = ".".join([first, second, third])
print(token)
```



**去官网解析token信息**

打印我们的token，复制token

```
eyJ0eXAiOiJ5Z3QiLCJleHAiOjE2MDM0Mjk4MDd9.eyJ1aWQiOjEsImF1dGhvciI6Ilx1NTk3ZFx1OTdmM1x1NWJhYiIsImFkbWluIjoxfQ.XT6h40ghE6aLxCisrLMbJG8stcP_ujMt1IpxVOMrO0w
```



![去官网解析token信息](https://cdn.hicaiji.com/halo/jwt-check-new-token_1603429134453.png?image/auto-orient,1/resize,m_lfit,w_200/quality,q_90)



发现数据跟我们定义的都一样，证明前面两部分正常，接下来就是验证token了



**解析token提取数据**

尝试解析token的并且提取数据

参考JWT的代码

```python
# 提取出header、payload、sign
headers = token.split(".")[0]
payload = token.split(".")[1]
sign = token.split(".")[2]
```

判断这个token是不是有效的，用同样的方法对header和payload加密，看看得到的签名跟token附上来的sign是不是一样

```python
headers_payload = f"{headers}.{payload}"

new_sign = base64.urlsafe_b64encode(
  hmac.new(salt.encode('utf-8'), headers_payload.encode('utf-8'), hashlib.sha256).digest()).decode(
  'utf-8').replace(
  '=',
  '')
print(new_sign == sign)
# if new_sign == sign: 判断是否相等

```

如果是一样的，证明token有效，再去获取header或者payload信息



```python
if isinstance(payload, str):
  payload = payload.encode('ascii') 

rem = len(payload) % 4 
if rem > 0:
  payload += b'=' * (4 - rem)
# 上面这一部分是解密的部分数据补全格式

payload_data = base64.urlsafe_b64decode(payload) # 解码
data = json.loads(payload_data) # 加载payload信息为可以通过get方法获取里面的值
  
print(data.get("uid")) # 打印token里面的payload部分中的uid数据信息
print(data.get("author")) # 打印token里面的payload部分中的uid数据信息
```



到这一步

我们就成功创建了token并且可以从token里面提取出来值了

接下来就是根据我们自己的需求封装成一个类了





## 5.参考文章

[jwt.io官网说明文档](https://jwt.io/introduction/)

[Python JWT使用](https://www.jianshu.com/p/03ad32c1586c)，by dawsonenjoy

[JSON Web Token 入门教程](https://www.ruanyifeng.com/blog/2018/07/json_web_token-tutorial.html)，by  阮一峰

[欢迎来赞我的GitHub](https://github.com/BeyondLam)