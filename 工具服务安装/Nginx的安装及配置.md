## Nginx的安装及配置[待完成]

安装

```
apt-get update
apt-get install nginx
y
## 浏览输入对应的ip或者域名看到默认的欢迎界面
```



修改默认配置

`cd /etc/nginx/sites-available/`

进入到这目录之后，下面的default 就是配置文件了，可以进行配置访问规则，代理规则或者静态网页规则

配置HTTPS

	域名的私钥公钥配置
	http转跳https

端口转发设置

`upstream的使用`

静态网页/文件配置

在`/var/www/html`目录下的index.nginx-debian.html就是nginx官方的默认欢迎界面了，可以进行自己的更改

