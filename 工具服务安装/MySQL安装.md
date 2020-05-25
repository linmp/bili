## MySQL安装

### :happy:安装

`sudo apt-get update`

`sudo apt-get install mysql-server`

然后输入y确认

##### 查看数据库运行状态

`systemctl status mysql.service`



### :ballot_box_with_check: 设置密码

`sudo mysql_secure_installation`

回车之后让你输入密码 这个密码就是以后你的数据库登录的密码

完成之后进入mysql

```shell
grant all privileges on *.* to 'root'@'%' identified by 'jamkung';
flush privileges;
```

:expressionless:注意的是


>>用户在本机root权限下还是能不用密码就能登录
>
>用pycharm打开数据库，看mysql数据库里面的user
>
>localhost root 对应的authentication_string是空的
>
>>命令:
>>
>>use mysql;
>>
>>update user set authentication_string=password("你的密码") where user='root';
>>
>>update user set password=password('你的密码') where user='root';
>>
>>update user set plugin="mysql_native_password"; 
>>
>>flush privileges;
>>
>>重启mysql服务
>>
>> systemctl restart mysql.service



### :old_key: 设置远程登录

mysql5.7配置文件路径：

`/etc/mysql/mysql.conf.d/mysqld.cnf`

```bash
#找到将bind-address = 127.0.0.1注销
```



### :face_with_thermometer: 将字符编码修改为能存表情的

将Mysql的编码从utf8转换成utf8mb4

查看当前数据库的编码

` show variables like '%char%';`

- character_set_client为客户端编码方式；

- character_set_connection为建立连接使用的编码；

- character_set_database数据库的编码；

- character_set_results结果集的编码；

- character_set_server数据库服务器的编码；



修改`/etc/mysql/mysql.conf.d/mysqld.cnf` 文件

[mysqld] Basic Settings下面加上

```text
character-set-server = utf8mb4
collation-server = utf8mb4_unicode_ci
init_connect='SET NAMES utf8mb4'
```

修改` /etc/mysql/conf.d/mysql.cnf`文件

在[mysql]下方加入

```text
default-character-set = utf8mb4
```

重启数据库再查看当前数据库的编码



### :outbox_tray: 导出备份数据库

```
CREATE TABLE student (
	student_id VARCHAR (10) PRIMARY KEY NOT NULL,
	student_name VARCHAR (20) NOT NULL,
	student_sex VARCHAR (2),
	student_age INTEGER (3),
	dept_id VARCHAR (2),
	class_id VARCHAR (8)
);
```

`mysqldump -uroot -ppassword 数据库名 > 导出到的文件夹的路径（默认为当前所在的文件夹）`

例如：

`mysqldump -uroot -pjamkung blog > /root/backup/blog.sql`



### :put_litter_in_its_place: 导入恢复数据库

先进Mysql创建一个空的数据库名字

`create database blog;`

退出Mysql并在终端恢复数据

进入到相应sql文件的目录

`mysql -uroot -ppassword blog <  blog.sql`




### :writing_hand: 常用命令
```
systemctl restart mysql.service #重启
systemctl stop mysql.service # 停止
systemctl start mysql.service # 运行
systemctl status mysql.service # 状态
```

