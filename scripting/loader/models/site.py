from sqlalchemy import Column, String
from MORE_JOBS.scripting.loader.base_model import BaseModel
from MORE_JOBS.scripting.loader.db_setup import Base


class Site(Base, BaseModel):
    __tablename__ = "site"

    name = Column(String, nullable=False)
    domain = Column(String, nullable=False)

    def __repr__(self):
        return f"<Site(id={self.id}, name='{self.name}', domain='{self.domain}')>"
