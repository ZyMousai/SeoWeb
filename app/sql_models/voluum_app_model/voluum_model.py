from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Session
from sql_models.db_config import Base, engine

from pydantic import BaseModel


# 数据模型
class CampaignMapping(BaseModel):
    m_id: str
    m_name: str
    s_id: str
    s_name: str

    class Config:
        orm_mode = True


# 数据库
class DBCampaignMapping(Base):
    # 对应的数据库的表的名称
    __tablename__ = 'campaign_mapping'
    id = Column(Integer, primary_key=True, autoincrement=True)

    m_id = Column(String(188))
    m_name = Column(String(588))
    s_id = Column(String(188))
    s_name = Column(String(588))

    @staticmethod
    async def get_all(db: Session):
        return db.query(DBCampaignMapping).all()

    @staticmethod
    async def add(db: Session, info: CampaignMapping):
        user = DBCampaignMapping(**info.dict())
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    async def delete(db: Session, cam_map_id: int):
        db.query(DBCampaignMapping).filter(DBCampaignMapping.id == cam_map_id).delete()
        db.commit()
        return {'id': cam_map_id}

    @staticmethod
    async def get_one(db: Session, m_id: str, s_id: str):
        return db.query(DBCampaignMapping).filter(DBCampaignMapping.m_id == m_id, DBCampaignMapping.s_id == s_id).one()


if __name__ == '__main__':
    Base.metadata.create_all(bind=engine)
