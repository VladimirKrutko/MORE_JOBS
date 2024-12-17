from sqlalchemy import Column, String
from MORE_JOBS.scripting.loader.base_model import BaseModel
from MORE_JOBS.scripting.loader.db_setup import Base


class Technology(Base, BaseModel):
    __tablename__ = "technology"

    name = Column(String, unique=True, nullable=False)

    def __repr__(self):
        return f"<Technology(id={self.id}, name='{self.name}')>"
