# 需要的配置
import redis
redis_store = redis.Redis(host='127.0.0.1', port=6379, db=1)  # 操作的redis配置


##### 常量
ADMIN_USERNAME = "好音宫"
ADMIN_PASSWORD = "caiji"
ADMIN_AVATAR = "https://mnp-1300173558.cos.ap-shanghai.myqcloud.com/default/20200708202410.jpg"
ADMIN_POWER = "超级管理员"
ADMIN_PHONE = "13525468134"



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
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@127.0.0.1:3306/caiji_dev'
    # SESSION_REDIS = redis.Redis(host='127.0.0.1', port=6379, password="jamkung", db=2)  # 操作的redis配置
    SESSION_REDIS = redis.Redis(host='127.0.0.1', port=6379, db=2)  # 操作的redis配置
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