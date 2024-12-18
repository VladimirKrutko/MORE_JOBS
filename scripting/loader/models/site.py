from scripting.loader.base_model import *


class Site(Base, BaseModel):
    __tablename__ = "site"

    name = Column(String, nullable=False)
    domain = Column(String, nullable=False)

    def __repr__(self):
        return f"<Site(id={self.id}, name='{self.name}', domain='{self.domain}')>"
