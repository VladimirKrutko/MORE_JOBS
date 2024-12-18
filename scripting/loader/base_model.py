from datetime import datetime
from scripting.loader.db_setup import Base, Session
from db_setup import Session as SessionLocal
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
    def create(cls, **kwargs):
        session = SessionLocal()
        if cls.exists(**kwargs):
            print(f"{cls.__name__} already exists!")
            return None
        instance = cls(**kwargs)
        session.add(instance)
        session.commit()
        session.refresh(instance)
        return instance

    @classmethod
    def update(cls, record_id, **kwargs):
        session = SessionLocal()
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
        session = SessionLocal()
        return session.query(cls).filter_by(**kwargs).first() is not None
