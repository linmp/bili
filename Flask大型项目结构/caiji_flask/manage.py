from app import create_app, db
from flask_script import Manager  # 管理项目的 额外制定一些命令
from flask_migrate import Migrate, MigrateCommand  # 管理数据库需要的脚本 追踪数据库变化的脚本

app = create_app("develop")  # 工厂函数模式选择
manager = Manager(app)  # 用manage进行项目管理 代管app
Migrate(app, db)  # 把app和db的信息绑定起来进行追踪

manager.add_command("db", MigrateCommand)  # 绑定额外的db命令

"""
python3 manage.py db init #初始化
python3 manage.py db migrate -m "init message" #提交变更
python3 manage.py db upgrade # 升级变更
python3 manage.py db downgrade # 降级变更
"""


# 初始化管理员账号数据,添加manager命令
@manager.command
def create_admin():
    from app.models import Admin
    from config import ADMIN_USERNAME, ADMIN_PASSWORD, ADMIN_POWER, ADMIN_AVATAR, ADMIN_PHONE
    try:
        admin_new = Admin(username=ADMIN_USERNAME, password=ADMIN_PASSWORD,
                          avatar=ADMIN_AVATAR,
                          power=ADMIN_POWER, phone=ADMIN_PHONE)
        db.session.add(admin_new)
        db.session.commit()
        print("初始化成功")
    except Exception as e:
        print(e)
        print("初始化失败")
        db.session.rollback()



if __name__ == '__main__':
    manager.run()

    """
    # 启动命令 gunicorn -w 4 -b 0.0.0.0:5050 manage:app
    Gunicorn 的常用运行参数说明：
    -w WORKERS, –workers: worker 进程的数量，通常每个 CPU 内核运行 2-4 个 worker 进程。
    -b BIND, –bind: 指定要绑定的服务器端口号或 socket
    -c CONFIG, –config: 指定 config 文件
    -k WORKERCLASS, –worker-class: worker 进程的类型，如 sync, eventlet, gevent, 默认为 sync
    -n APP_NAME, –name: 指定 Gunicorn 进程在进程查看列表里的显示名（比如 ps 和 htop 命令查看）
    """