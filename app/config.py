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
else:
    # produce
    MONGO_INFO = {
        'host': '3.23.234.28',
        'port': 27017,
        'username': 'admin',
        'password': '4242587f*',
        'database': 'panda_auto'
    }
