from datetime import datetime
from scripting.loader.db_setup import Base, Session
from sqlalchemy import (
    Column, Integer, String, Boolean, DateTime, JSON, ForeignKey, Text, UniqueConstraint
)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import as_declarative, declared_attr


@as_declarative()
class BaseModel:
    id = Column(Integer, primary_key=True)
    create_date = Column(DateTime, default=datetime.utcnow)
    update_date = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    @classmethod
    def create(cls,session, **kwargs):
        # session = kwargs['session']
        existing_obj = cls.exists(**kwargs)
        if existing_obj:
            print(f"{cls.__name__} already exists!")
            return existing_obj
        
        instance = cls(**kwargs)
        session.add(instance)
        session.commit()
        session.refresh(instance)
        return instance

    @classmethod
    def update(cls, session, record_id, **kwargs):
        instance = session.query(cls).filter_by(id=record_id).first()
        if not instance:
            print(f"{cls.__name__} with id {record_id} not found.")
            return None
        for key, value in kwargs.items():
            setattr(instance, key, value)
        session.commit()
        session.refresh(instance)
        return instance

    @classmethod
    def exists(cls, **kwargs):
        session = Session()
        return session.query(cls).filter_by(**kwargs).first()
