from scripting.loader.base_model import *


class Technology(Base, BaseModel):
    __tablename__ = "technology"

    name = Column(String, unique=True, nullable=False)

    def __repr__(self):
        return f"<Technology(id={self.id}, name='{self.name}')>"
