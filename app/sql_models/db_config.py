import sqlalchemy

from sqlalchemy.orm import declarative_base, sessionmaker
from config import SQLALCHEMY_DATABASE_URI

# 创建引擎
engine = sqlalchemy.create_engine(SQLALCHEMY_DATABASE_URI)
# 创建基类
Base = declarative_base()

# 数据库的会滴对象
SessionLocal = sessionmaker(bind=engine)


