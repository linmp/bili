import time
import json
# pip install itchat
import itchat
# pip install requests
import requests

itchat.auto_login(enableCmdQR=2, hotReload=True)  # 登录


# 获取每日一句英语
def get_iciba():
    url = 'http://open.iciba.com/dsapi/'
    r = requests.get(url)
    content = json.loads(r.text)
    return u'每日一句：\n' + content['content'] + '\n' + content['note']


# 搜索用户
def people(nickname):
    username = itchat.search_friends(name=nickname)[0]['UserName']
    return username


# 搜索群名
def chat_room(roomname):
    c_r_name = itchat.search_chatrooms(name=roomname)[0]['UserName']
    return c_r_name


# 发送每日英语
def everyday_english(name):
    try:
        itchat.send(get_iciba(), toUserName=people(name))
    except Exception as e:
        print(e)
        itchat.send('发送每日一句英语失败', toUserName='filehelper')


# 发送课程表
def send_time_table(table, name):
    """
    发送课表
    :param name: 用户名,  filehelper是文件传输助手
    :param table: 课表 字符串
    :return:
    """
    try:
        itchat.send(table, toUserName=people(name))
    except Exception as e:
        print(e)
        itchat.send('发送课程表失败', toUserName='filehelper')


# 群发信息群名
def say_good_morning(name):
    """
    群消息
    :param name: 群名
    :return:
    """
    try:
        itchat.send('大家早上好^-^', toUserName=chat_room(name))
    except Exception as e:
        itchat.send(str(e), toUserName='filehelper')


name_list = ['小号']
time_table = {
    "1": "今天星期一\
           \n你共有5节课\
           \n10-12 A教学楼 202\
           \n14-16 B教学楼 404\
           \n16-18 C教学楼 606",
    "2": "今天星期二\
           \n你共有5节课\
           \n10-12 A教学楼 202\
           \n14-16 B教学楼 404\
           \n16-18 C教学楼 606",
    "3": "今天星期三\
           \n你共有5节课\
           \n10-12 A教学楼 202\
           \n14-16 B教学楼 404\
           \n16-18 C教学楼 606",
    "4": "今天星期四\
           \n你共有5节课\
           \n10-12 A教学楼 202\
           \n14-16 B教学楼 404\
           \n16-18 C教学楼 606",
    "5": "今天星期五\
           \n你共有5节课\
           \n10-12 A教学楼 202\
           \n14-16 B教学楼 404\
           \n16-18 C教学楼 606",
    "6": "今天没课上美滋滋!",
    "7": "今天没课上美滋滋!"
}


# 执行函数
def send_meg(namelist):
    for i in range(100):
        for name in namelist:
            everyday_english(name)
            today = time.strftime("%w")
            send_time_table(time_table.get(today), name)
            time.sleep(86400) # 休眠一天秒数


send_meg(name_list)

itchat.run()

# ps 有的用户登录不了，尽量不要涉及群的操作，操作频率不能太高
