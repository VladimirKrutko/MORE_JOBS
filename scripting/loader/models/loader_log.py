from sqlalchemy import Column, Integer, String, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class LoaderLog(Base):
    __tablename__ = 'loader_log'

    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String, nullable=False)
    site = Column(String, nullable=False)
    file = Column(String, nullable=False)
    status = Column(String)
    create_date = Column(TIMESTAMP, default=func.now())
    update_date = Column(TIMESTAMP, default=func.now(), onupdate=func.now())
