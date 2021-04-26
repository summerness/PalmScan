from sqlalchemy import create_engine, Column, String, DateTime, func, Integer, Boolean, JSON
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os

os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'
engine = create_engine('postgresql://postgres:652684328@127.0.0.1/palm', pool_size=20, max_overflow=20)
DBSession = sessionmaker(bind=engine)
Base = declarative_base()


def to_dict(self):
    return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}


Base.to_dict = to_dict


class User(Base):
    __tablename__ = "user"

    open_id = Column(String(255), primary_key=True)
    create_time = Column(DateTime, server_default=func.now())


class PInfo(Base):
    __tablename__ = "p_info"
    id = Column(Integer, primary_key=True)
    open_id = Column(String(255))
    create_time = Column(DateTime, server_default=func.now())
    img_path = Column(String(255))
    img_name = Column(String(255))
    img_full_path = Column(String(255))
    is_complete = Column(Boolean)
    is_expire = Column(Boolean)
    complete_time = Column(DateTime)
    expire_time = Column(DateTime)
    roi_main = Column(JSON)
    roi_5 = Column(JSON)
    s_thenar = Column(JSON)
    thenar = Column(JSON)
