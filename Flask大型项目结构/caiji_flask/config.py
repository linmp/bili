# 需要的配置
import redis

# # 数据库的配置
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:jamkung@pukgai.com:3306/caiji_flask'
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# app.config["SECRET_KEY"] = "sdfsdfsdf"
# db = SQLAlchemy(app)  # 实例化的数据库
#
# #########################
# #   session 存redis上   #
# #########################
# app.config["SESSION_TYPE"] = "redis"  # 存session进redis
# app.config["SESSION_USE_SIGNER"] = True  # 对cookie中session_id进行隐藏处理 加密混淆
# app.config["PERMANENT_SESSION_LIFETIME"] = 20  # session数据的有效期，单位秒
# app.config['SESSION_REDIS'] = redis.Redis(host='pukgai.com', port=6379, password="jamkung", db=2)  # 操作的redis配置


class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "sdfsdfsdf"
    # flask-session配置
    SESSION_TYPE = "redis"
    SESSION_USE_SIGNER = True  # 对cookie中session_id进行隐藏处理 加密混淆
    PERMANENT_SESSION_LIFETIME = 20  # session数据的有效期，单位秒

# 开发环境
class DevelopmentConfig(Config):
    """开发模式的配置信息"""
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:jamkung@pukgai.com:3306/caiji_dev'
    SESSION_REDIS = redis.Redis(host='pukgai.com', port=6379, password="jamkung", db=2)  # 操作的redis配置
    DEBUG = True

# 线上环境
class ProductionConfig(Config):
    """生产环境配置信息"""
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:jamkung@pukgai.com:3306/caiji_pro'
    SESSION_REDIS = redis.Redis(host='pukgai.com', port=6379, password="jamkung", db=3)  # 操作的redis配置



config_map = {
    "develop": DevelopmentConfig,
    "product": ProductionConfig
}