from sqlalchemy.ext.declarative import declarative_base
from scripting.loader.base_model import *
from sqlalchemy import TIMESTAMP
from sqlalchemy.sql import func

Base = declarative_base()

class ParserLog(Base, BaseModel):
    __tablename__ = 'parser_log'

    id = Column(Integer, primary_key=True, autoincrement=True) 
    url = Column(String, nullable=False)
    site = Column(String, nullable=False)
    file = Column(String, nullable=False)
    message = Column(Text)
    status = Column(String)
    create_date = Column(TIMESTAMP, default=func.now())
    update_date = Column(TIMESTAMP, default=func.now(), onupdate=func.now())
