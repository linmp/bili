from app import create_app, db
from flask_script import Manager  # 管理项目的 额外制定一些命令
from flask_migrate import Migrate, MigrateCommand  # 管理数据库需要的脚本 追踪数据库变化的脚本

app = create_app("develop")  # 工厂函数模式选择
manager = Manager(app)  # 用manage进行项目管理 代管app
Migrate(app, db)  # 把app和db的信息绑定起来进行追踪

manager.add_command("db", MigrateCommand)  # 绑定额外的db命令

"""
python3 manage.py db init #初始化
python3 manage.py db migrate -m "message" #提交变更
python3 manage.py db upgrade # 升级变更
python3 manage.py db downgrade # 降级变更
"""


if __name__ == '__main__':
    manager.run()
