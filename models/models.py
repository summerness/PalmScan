from sqlalchemy import create_engine, Column, String, Text, Float, DateTime, Integer, Boolean, JSON
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


class Image(Base):
    __tablename__ = "image"

    id = Column(Integer, primary_key=True)
    open_id = Column(String)
    create_time = Column(DateTime)
    img_path = Column(String)
    img_name = Column(String)
    img_save_path = Column(String)
    is_complete = Column(Boolean)
    is_expire = Column(Boolean)
    complete_time = Column(DateTime)
    expire_time = Column(DateTime)
    report_code = Column(String)


class Report(Base):
    __tablename__ = "report"

    code = Column(String, primary_key=True)
    hand_success = Column(JSON)
    score = Column(Float)
    roi_main = Column(String)
    roi_main_hsv = Column(String)
    roi_main_color = Column(String)
    roi_main_info = Column(Text)
    roi_5 = Column(String)
    roi_5_line = Column(String)
    roi_5_exist = Column(Boolean)
    roi_5_info = Column(Text)
    roi_thenar = Column(String)
    roi_thenar_threshold = Column(String)
    roi_thenar_cross_count = Column(Integer)
    roi_thenar_cross = Column(String)
    roi_thenar_info = Column(Text)
    roi_sthenar = Column(String)
    roi_sthenar_threshold = Column(String)
    roi_sthenar_line = Column(String)
    roi_sthenar_line_info = Column(String)
    roi_sthenar_line_exist = Column(Boolean)
