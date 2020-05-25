## Redis安装

### :one: 安装：更新源并下载redis服务

```
#进入 root用户下
#apt-get update
#apt-get install redis-server
Do you want to continue? [Y/n] 
Y
```



### :two: 测试是否能使用

```
#redis-cli

ping一下

redis 127.0.0.1:6379> ping
PONG
127.0.0.1:6379> exit


```



### :three: 设置登录密码

`#vi /etc/redis/redis.conf`

然后建议通过搜索来找到下面这行注释
`#requirepass foobared `

按一下英文键盘 i 字母进入编辑模式

把井号去掉，foobared 改为你想设置的redis的登录密码
比如:我想设置密码为jamkung
`requirepass jamkung`

保存退出
```
左上角Esc键
Shift 和 : 同时按下
输入 wq 并回车
```



###  :four: 允许远程登录

PS：注意如果你的是阿里云腾讯云这些主机，注意看你的服务器打开对应的6379端口没有，一般在安全组里面设置，根据你自己的主机百度或者谷歌一下怎么开呗,不然就算主机允许远程登录，端口不放行还是登录不了的



redis默认是只能本地登录不允许远程登录的，所以修改一下设置

```
修改文件
# vi /etc/redis/redis.conf
按一下英文键盘 i 字母进入编辑模式
找到下面这行 加上# 取消绑定本地
#bind 127.0.0.1
保存并退出
左上角Esc键
Shift 和 : 同时按下
输入 wq 并回车
```



### :five: 重启redis进行加载配置

`# service redis-server restart`



### :six: 远程访问命令

```
# redis-cli -h (空格) (redis的ip 地址，可以写域名)  -p (空格) (redis的端口号 如果默认是6379可以不用写这个端口) -a (空格) (密码，如果没有可以不用写这参数)
```