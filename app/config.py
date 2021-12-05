IS_TEST = True

# ==============数据库信息==============
if IS_TEST:
    # test
    MONGO_INFO = {
        'host': '45.63.13.111',
        'port': 27017,
        'username': 'admin',
        'password': '4242587f*',
        'database': 'panda_auto'
    }
    MYSQL_INFO = {
        'host': '45.63.5.115',
        'port': 3306,
        'username': 'root',
        'password': '4242587f*',
        'database': 'SeoWeb'
    }
else:
    # produce
    MONGO_INFO = {
        'host': '3.23.234.28',
        'port': 27017,
        'username': 'admin',
        'password': '4242587f*',
        'database': 'panda_auto'
    }
    MYSQL_INFO = {
        'host': '3.23.234.28',
        'port': 3306,
        'username': 'root',
        'password': '!wBDqm:p(2q8+',
        'database': 'SeoWeb'
    }

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://%s:%s@%s:%s/%s' % (
    MYSQL_INFO['username'], MYSQL_INFO['password'], MYSQL_INFO['host'], MYSQL_INFO['port'], MYSQL_INFO['database'])
