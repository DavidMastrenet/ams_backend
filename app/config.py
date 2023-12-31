# 数据库
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://username:password@server:port/database'
SQLALCHEMY_TRACK_MODIFICATIONS = False

# 密钥
SECRET_KEY = ''
SALT = ''

# 接口地址
CAS_URL = "https://cas.shnu.edu.cn/cas/login?service=http%3A%2F%2Fcourse.shnu.edu.cn%2Feams%2Flogin.action"
EAM_URL = "https://course.shnu.edu.cn/eams/home.action"
EAM_STD_URL = "https://course.shnu.edu.cn/eams/stdDetail.action"

# 环境配置
ENV_NAME = "上海师范大学"
